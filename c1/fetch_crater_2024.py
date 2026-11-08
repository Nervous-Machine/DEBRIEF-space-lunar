"""
Fetch LRO CRaTER L2 SEC daily files (PDS4 bundle lro.crater) and reduce each
day to daily + hourly summaries. Raw files are hashed, reduced, then deleted.

Quality rule: prereg-c1-mars-sir-crosscheck.yaml, erratum 1.

Outputs (results/):
  crater_daily.jsonl    one row per day
  crater_hourly.jsonl   one row per hour (GOOD, SINGLE 1-6 means)
  crater_manifest.tsv   date, url, bytes, sha256

Run: python3 -I fetch_crater_2024.py 2024-01-10 2024-07-20
     (resumable: days already in crater_daily.jsonl are skipped)
"""

import hashlib
import json
import sys
import time
import urllib.request
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).parent
RES = HERE / "results"
RAW = HERE / "raw"
BASE = "https://pds-ppi.igpp.ucla.edu/data/lro-crater/data-der-sec"
FILL = 4294967295
MOON_R_KM = 1737.4

# column indices (label CRAT_L2_SEC_*_V01.xml)
I_BIAS, I_PROC = 3, range(8, 14)
I_DTHIN, I_DTHICK, I_MASK1, I_MASK2 = 16, 17, 18, 19
I_SINGLE, I_GOOD = range(20, 26), 26
I_MOON = range(29, 32)


def reduce_day(path):
    n_rows = n_valid = 0
    sums = [0.0] * 7  # SINGLE1..6, GOOD
    hourly = {}
    settings = Counter()
    alt_sum = 0.0
    with path.open() as f:
        for line in f:
            p = line.split(",")
            if len(p) < 32:
                continue
            n_rows += 1
            try:
                singles = [int(p[i]) for i in I_SINGLE]
                good = int(p[I_GOOD])
                bias = int(p[I_BIAS])
                procd = [int(p[i]) for i in I_PROC]
            except ValueError:
                continue
            vals = singles + [good]
            if any(v >= FILL or v < 0 for v in vals) or bias != 1 or any(x != 1 for x in procd):
                continue
            n_valid += 1
            settings[(p[I_DTHIN].strip(), p[I_DTHICK].strip(), p[I_MASK1].strip(), p[I_MASK2].strip())] += 1
            for k, v in enumerate(vals):
                sums[k] += v
            hr = p[2].strip().strip('"')[11:13]
            h = hourly.setdefault(hr, [0, [0.0] * 7])
            h[0] += 1
            for k, v in enumerate(vals):
                h[1][k] += v
            try:
                mv = [float(p[i]) for i in I_MOON]
                alt_sum += (mv[0] ** 2 + mv[1] ** 2 + mv[2] ** 2) ** 0.5 - MOON_R_KM
            except ValueError:
                pass
    mean = [s / n_valid for s in sums] if n_valid else [None] * 7
    modal = settings.most_common(1)[0][0] if settings else None
    return {
        "n_rows": n_rows, "n_valid": n_valid,
        "single_mean": mean[:6], "good_mean": mean[6],
        "settings_modal": modal, "settings_n_distinct": len(settings),
        "alt_km_mean": alt_sum / n_valid if n_valid else None,
    }, {hr: {"n": h[0], "single_mean": [x / h[0] for x in h[1][:6]], "good_mean": h[1][6] / h[0]}
        for hr, h in sorted(hourly.items())}


def fetch(url, dest, tries=4):
    for t in range(tries):
        try:
            h = hashlib.sha256()
            with urllib.request.urlopen(url, timeout=300) as r, dest.open("wb") as f:
                while chunk := r.read(1 << 20):
                    h.update(chunk)
                    f.write(chunk)
            return dest.stat().st_size, h.hexdigest()
        except Exception as e:  # noqa: BLE001
            print(f"  retry {t + 1}: {e}", flush=True)
            time.sleep(5 * (t + 1))
    raise RuntimeError(f"failed {url}")


def main(d0, d1):
    RES.mkdir(exist_ok=True)
    RAW.mkdir(exist_ok=True)
    daily_p, hourly_p = RES / "crater_daily.jsonl", RES / "crater_hourly.jsonl"
    manifest_p = RES / "crater_manifest.tsv"
    done = set()
    if daily_p.exists():
        done = {json.loads(l)["date"] for l in daily_p.read_text().splitlines() if l.strip()}
    d = date.fromisoformat(d0)
    end = date.fromisoformat(d1)
    while d <= end:
        ds = d.isoformat()
        if ds not in done:
            doy = d.timetuple().tm_yday
            name = f"CRAT_L2_SEC_{d.year}{doy:03d}_V01.TAB"
            url = f"{BASE}/{d.year}/{name}"
            dest = RAW / name
            try:
                size, sha = fetch(url, dest)
            except RuntimeError as e:
                print(f"{ds} MISSING ({e})", flush=True)
                with daily_p.open("a") as f:
                    f.write(json.dumps({"date": ds, "missing": True}) + "\n")
                d += timedelta(days=1)
                continue
            day, hours = reduce_day(dest)
            dest.unlink()
            with manifest_p.open("a") as f:
                f.write(f"{ds}\t{url}\t{size}\t{sha}\n")
            with daily_p.open("a") as f:
                f.write(json.dumps({"date": ds, **day}) + "\n")
            with hourly_p.open("a") as f:
                for hr, v in hours.items():
                    f.write(json.dumps({"hour": f"{ds}T{hr}", **v}) + "\n")
            print(f"{ds} valid={day['n_valid']} good={day['good_mean']:.3f}" if day["good_mean"] is not None
                  else f"{ds} valid=0", flush=True)
        d += timedelta(days=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

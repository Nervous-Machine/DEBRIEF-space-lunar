"""
Score lunar cross-check c1 exactly as pre-registered
(prereg-c1-mars-sir-crosscheck.yaml, errata 1-2).

  Test A — OMNI at Earth: stream-interface signature near each meeting
  Test B — CRaTER at the Moon: cosmic-ray (GOOD rate) dip near each meeting

Run: python3 -I analyze_c1.py [A|B|AB]     -> results/c1_scored.json
"""

import json
import statistics as st
import sys
from datetime import datetime, timedelta, timezone, date
from pathlib import Path

HERE = Path(__file__).parent
RES = HERE / "results"
OMNI = HERE / "raw" / "omni" / "omni2_2024.dat"
UTC = timezone.utc

MEETINGS = {
    "M1": ("feb_2024", "2024-02-03T04:00"),
    "M2": ("feb_2024", "2024-03-01T13:00"),
    "M3": ("jun_2024", "2024-06-04T04:00"),
    "M4": ("jun_2024", "2024-07-01T10:00"),
}


def ts(s):
    return datetime.fromisoformat(s).replace(tzinfo=UTC)


def pct_rank(x, dist):
    return 100.0 * sum(1 for d in dist if d <= x) / len(dist)


def quantile(dist, q):
    s = sorted(dist)
    k = (len(s) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


# ── Test A ──────────────────────────────────────────────────────────────────
def load_omni():
    rows = {}
    for line in OMNI.read_text().splitlines():
        w = line.split()
        y, doy, hr = int(w[0]), int(w[1]), int(w[2])
        t = datetime(y, 1, 1, hr, tzinfo=UTC) + timedelta(days=doy - 1)
        b, v, p = float(w[8]), float(w[24]), float(w[28])
        rows[t] = {"B": None if b >= 999.9 else b,
                   "V": None if v >= 9999.0 else v,
                   "P": None if p >= 99.99 else p}
    return rows


def med6(om, t, key):
    vals = [om.get(t - timedelta(hours=k), {}).get(key) for k in range(6)]
    vals = [x for x in vals if x is not None]
    return st.median(vals) if len(vals) >= 4 else None


def base(om, t0, t1, key):
    vals, t = [], t0
    while t <= t1:
        x = om.get(t, {}).get(key)
        if x is not None:
            vals.append(x)
        t += timedelta(hours=1)
    return st.median(vals) if vals else None


def test_a_at(om, T):
    bV = base(om, T - timedelta(days=5), T - timedelta(days=2), "V")
    bB = base(om, T - timedelta(days=5), T - timedelta(days=2), "B")
    bP = base(om, T - timedelta(days=5), T - timedelta(days=2), "P")
    out = {"baseline": {"V": bV, "B": bB, "P": bP}, "fires": False,
           "speed_cross_utc": None, "companion_utc": None, "companion": None,
           "max_V6": None, "max_B6_ratio": None, "max_P6_ratio": None}
    if bV is None:
        return out
    t, end = T - timedelta(days=2), T + timedelta(days=2)
    mv = mb = mp = None
    while t <= end:
        v6, b6, p6 = med6(om, t, "V"), med6(om, t, "B"), med6(om, t, "P")
        if v6 is not None:
            mv = v6 if mv is None else max(mv, v6)
        if b6 is not None and bB:
            mb = b6 / bB if mb is None else max(mb, b6 / bB)
        if p6 is not None and bP:
            mp = p6 / bP if mp is None else max(mp, p6 / bP)
        if out["speed_cross_utc"] is None and v6 is not None and v6 >= bV + 80:
            out["speed_cross_utc"] = t.strftime("%Y-%m-%dT%H")
        t += timedelta(hours=1)
    out.update(max_V6=mv, max_B6_ratio=mb, max_P6_ratio=mp)
    if out["speed_cross_utc"]:
        tc = ts(out["speed_cross_utc"] + ":00")
        for k in range(-24, 25):
            u = tc + timedelta(hours=k)
            b6, p6 = med6(om, u, "B"), med6(om, u, "P")
            hit = ("B" if (b6 and bB and b6 >= 2 * bB) else
                   "P" if (p6 and bP and p6 >= 2 * bP) else None)
            if hit:
                out.update(fires=True, companion_utc=u.strftime("%Y-%m-%dT%H"), companion=hit)
                break
    return out


def run_a():
    om = load_omni()
    meet = {m: {"arrival": a, "utc": u, **test_a_at(om, ts(u))} for m, (a, u) in MEETINGS.items()}
    pseudo, d = [], date(2024, 1, 15)
    while d <= date(2024, 7, 15):
        pseudo.append(test_a_at(om, datetime(d.year, d.month, d.day, tzinfo=UTC))["fires"])
        d += timedelta(days=1)
    base_rate = sum(pseudo) / len(pseudo)
    preds = {
        "PA1_feb_reached_earth": meet["M1"]["fires"] or meet["M2"]["fires"],
        "PA2_jun_reached_earth": meet["M3"]["fires"] or meet["M4"]["fires"],
    }
    return {"meetings": meet, "base_rate_fire_fraction": round(base_rate, 3),
            "n_pseudo": len(pseudo), "predictions": preds}


# ── Test B ──────────────────────────────────────────────────────────────────
def load_crater():
    rows = [json.loads(l) for l in (RES / "crater_daily.jsonl").read_text().splitlines() if l.strip()]
    rows = [r for r in rows if not r.get("missing")]
    modal = st.mode([tuple(r["settings_modal"]) for r in rows if r.get("settings_modal")])
    s1_med = st.median([r["single_mean"][0] for r in rows if r["n_valid"]])
    days, drops = {}, []
    for r in rows:
        d = r["date"]
        why = None
        if r["n_valid"] < 70000:
            why = f"coverage {r['n_valid']}"
        elif tuple(r["settings_modal"]) != modal or r["settings_n_distinct"] != 1:
            why = f"settings {r['settings_modal']} x{r['settings_n_distinct']}"
        sep = r["n_valid"] > 0 and r["single_mean"][0] >= 1.5 * s1_med
        days[d] = {"good": r["good_mean"], "thick": sum(r["single_mean"][i] for i in (1, 3, 5)) if r["n_valid"] else None,
                   "usable": why is None and not sep, "sep": sep, "drop": why, "alt": r.get("alt_km_mean")}
        if why:
            drops.append({"date": d, "why": why})
    return days, drops, s1_med, modal


def test_b_at(days, T, key="good"):
    def span(a, b):
        d0, d1 = (T + timedelta(days=a)).date(), (T + timedelta(days=b)).date()
        out, d = [], d0
        while d <= d1:
            out.append(d.isoformat())
            d += timedelta(days=1)
        return out
    dip = [days[d][key] for d in span(-1, 3) if d in days and days[d]["usable"]]
    bas = [days[d][key] for d in span(-9, -3) if d in days and days[d]["usable"]]
    if len(dip) < 3 or len(bas) < 4:
        return {"indeterminate": True, "n_dip": len(dip), "n_base": len(bas)}
    b = st.median(bas)
    return {"indeterminate": False, "baseline": b, "min_dip": min(dip),
            "D": (min(dip) - b) / b, "n_dip": len(dip), "n_base": len(bas)}


def run_b(a_result):
    days, drops, s1_med, modal = load_crater()
    out = {"sep_threshold_single1": 1.5 * s1_med, "modal_settings": modal,
           "n_days": len(days), "n_sep_flagged": sum(d["sep"] for d in days.values()),
           "sep_days": sorted(k for k, v in days.items() if v["sep"]),
           "dropped_days": drops}
    for key in ("good", "thick"):
        pseudo, d = [], date(2024, 1, 20)
        while d <= date(2024, 7, 15):
            r = test_b_at(days, datetime(d.year, d.month, d.day, tzinfo=UTC), key)
            if not r["indeterminate"]:
                pseudo.append(r["D"])
            d += timedelta(days=1)
        p10 = quantile(pseudo, 0.10)
        meet = {}
        for m, (a, u) in MEETINGS.items():
            r = test_b_at(days, ts(u), key)
            if not r["indeterminate"]:
                r["pct_rank"] = round(pct_rank(r["D"], pseudo), 1)
                r["dip"] = r["D"] <= p10
            meet[m] = r
        out[key] = {"null_p10_D": p10, "null_median_D": st.median(pseudo),
                    "n_pseudo": len(pseudo), "meetings": meet}
    if a_result:
        fired = [m for m, v in a_result["meetings"].items() if v["fires"]]
        g = out["good"]["meetings"]
        out["predictions"] = {
            "PB1_dip_where_A_fires": {m: g[m].get("dip") for m in fired} or "no meeting fired in A",
            "PB2_size_0p5_to_5pct": {m: (0.005 <= -g[m]["D"] <= 0.05) if not g[m]["indeterminate"] else None
                                     for m in fired} or "no meeting fired in A",
        }
    return out


def main(which):
    path = RES / "c1_scored.json"
    res = json.loads(path.read_text()) if path.exists() else {}
    res["scored_utc"] = datetime.now(UTC).isoformat(timespec="seconds")
    if "A" in which:
        res["test_a_omni"] = run_a()
    if "B" in which:
        res["test_b_crater"] = run_b(res.get("test_a_omni"))
    path.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps({k: v for k, v in res.items()}, indent=2, default=str)[:6000])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "AB")

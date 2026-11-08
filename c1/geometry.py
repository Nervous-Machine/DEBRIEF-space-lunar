"""
Corotation mapping: when should the Moon (Earth's longitude, ~1 AU) have met
the two stream interfaces confirmed at Mars (MAVEN, cycles 13 and 15)?

Uses JPL Horizons for heliocentric ecliptic positions of Earth and Mars, and
a simple ballistic corotation model: plasma leaves a source longitude on the
Sun radially at constant speed V while the Sun turns at the sidereal rate.
An observer at (r, phi) sees that source at  t = (phi - lambda0)/Omega + r/V.

No CRaTER data is read here. Output: results/geometry.json

Run: python3 -I geometry.py
"""

import json
import math
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "results" / "geometry.json"
AU_KM = 1.495978707e8
OMEGA = 360.0 / 25.38  # deg/day, sidereal (Carrington) rotation

# Arrivals at Mars, from the run ledger (cycles 13 and 15)
ARRIVALS = {
    "feb_2024": "2024-02-16T00:00:00",  # pdyn front; MAG compression 01:00
    "jun_2024": "2024-06-13T10:00:00",  # speed crossing; MAG compression 11:00
}
SPEEDS = [300.0, 360.0, 450.0]  # km/s; 360 ~ measured Feb peak at Mars


def horizons(body, start, stop):
    q = {
        "format": "json", "COMMAND": f"'{body}'", "CENTER": "'500@10'",
        "EPHEM_TYPE": "'VECTORS'", "REF_PLANE": "'ECLIPTIC'",
        "START_TIME": f"'{start}'", "STOP_TIME": f"'{stop}'",
        "STEP_SIZE": "'6 h'", "VEC_TABLE": "'2'", "CSV_FORMAT": "'YES'",
        "OUT_UNITS": "'KM-S'",
    }
    url = "https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q)
    with urllib.request.urlopen(url, timeout=120) as r:
        txt = json.load(r)["result"]
    rows = txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()
    out = []
    for line in rows:
        p = [s.strip() for s in line.split(",")]
        jd, x, y, z = float(p[0]), float(p[2]), float(p[3]), float(p[4])
        out.append((jd, math.hypot(x, y) / AU_KM, math.degrees(math.atan2(y, x)) % 360))
    return out


def jd_to_dt(jd):
    return datetime(2000, 1, 1, 12, tzinfo=timezone.utc) + timedelta(days=jd - 2451545.0)


def dt_to_jd(dt):
    return 2451545.0 + (dt - datetime(2000, 1, 1, 12, tzinfo=timezone.utc)).total_seconds() / 86400


def interp(table, jd):
    for (j0, r0, l0), (j1, r1, l1) in zip(table, table[1:]):
        if j0 <= jd <= j1:
            f = (jd - j0) / (j1 - j0)
            dl = ((l1 - l0 + 180) % 360) - 180
            return r0 + f * (r1 - r0), (l0 + f * dl) % 360
    raise ValueError("jd outside table")


def wrap(a):
    return ((a + 180) % 360) - 180


def main():
    earth = horizons("399", "2023-12-15", "2024-08-15")
    mars = horizons("499", "2023-12-15", "2024-08-15")
    result = {"model": "ballistic corotation, sidereal 25.38 d, radial constant V",
              "source": "JPL Horizons vectors, heliocentric ecliptic J2000",
              "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "arrivals": {}}
    for key, ts in ARRIVALS.items():
        tM = datetime.fromisoformat(ts).replace(tzinfo=timezone.utc)
        jM = dt_to_jd(tM)
        rM, phM = interp(mars, jM)
        rE, phE = interp(earth, jM)
        entry = {"mars_arrival_utc": ts, "mars_r_au": round(rM, 3),
                 "earth_r_au": round(rE, 3),
                 "mars_minus_earth_longitude_deg": round(wrap(phM - phE), 1),
                 "earth_meetings": {}}
        for V in SPEEDS:
            v_au_d = V * 86400 / AU_KM
            lam0 = phM - OMEGA * (jM - rM / v_au_d)
            hits, prev = [], None
            j = jM - 35
            while j <= jM + 35:
                r, ph = interp(earth, j)
                f = wrap(lam0 + OMEGA * (j - r / v_au_d) - ph)
                if prev is not None and prev < 0 <= f and abs(f - prev) < 90:
                    hits.append(j)
                prev = f
                j += 1 / 24
            entry["earth_meetings"][f"{int(V)}_km_s"] = [
                {"utc": jd_to_dt(h).strftime("%Y-%m-%dT%H:00"),
                 "days_from_mars_arrival": round(h - jM, 1)} for h in hits]
        result["arrivals"][key] = entry
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

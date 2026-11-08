# Cycle 1 — Mars stream interfaces at the Moon (scored 2026-10-18)

Pre-registration: `prereg-c1-mars-sir-crosscheck.yaml`, written before any 2024 OMNI or CRaTER value was read, with
two pre-scoring errata appended before scoring. Hashes and times: `prereg-c1-mars-sir-crosscheck.sha256` (the
sidecar was named `prereg.sha256` in the working folder; its content is unchanged). The hash listed after erratum 2
is the current file's hash.

Inputs: the two 2024 arrivals at Mars (February 16 to 17 and June 13; Mars finding F9, confirmed in MAVEN plasma and
magnetometer data) and JPL Horizons positions (`geometry.py` → `results/geometry.json`). Data: OMNI2 hourly from
NASA SPDF (`low_res_omni/omni2_2024.dat`, not vendored; 2.9 MB) and LRO CRaTER L2 SEC daily files from PDS PPI
(`fetch_crater_2024.py`; `results/crater_manifest.tsv` lists every file with its sha256; two days, 2024-06-19 and
06-20, were missing at PDS).

Result: `results/c1_report.md` and `results/c1_scored.json`. Verdict mixed; suggestive, not strong, at the June
meeting; February not seen at Earth's longitude. Lessons for a c2 are at the end of the report.

To rerun: `python3 geometry.py` (needs network for Horizons), `python3 fetch_crater_2024.py` (about 3 GB of daily
files), download `omni2_2024.dat` into `raw/omni/`, then `python3 analyze_c1.py`.

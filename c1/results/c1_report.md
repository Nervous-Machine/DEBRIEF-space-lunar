# Lunar c1 — Mars stream interfaces at the Moon: scored 2026-10-18

Pre-registration: `prereg-c1-mars-sir-crosscheck.yaml` (errata 1–2), hashes and
times in `prereg-c1-mars-sir-crosscheck.sha256`. Scores: `results/c1_scored.json`.

## Geometry (before data)
Moon meetings predicted by ballistic corotation (360 km/s; speed spread ≤ 0.5 d):
M1 Feb 3 and M2 Mar 1 (Feb 16 Mars arrival); M3 Jun 4 and M4 Jul 1 (Jun 13 Mars arrival).

## Test A — OMNI at Earth
| Meeting | Fires | Detail |
|---|---|---|
| M1 Feb 3 | no | baseline already fast (449 km/s); max 423 |
| M2 Mar 1 | no | pressure 5.4×, field 2.4×, but speed +27 km/s only (compression without speed-up) |
| M3 Jun 4 | **yes** | speed crossing Jun 4 17 UT (13 h after prediction); pressure 2× at Jun 3 19 UT |
| M4 Jul 1 | yes (weak) | crossing Jun 29 10 UT (window edge); companion Jun 28 13 UT is outside the search window; baseline disturbed |

Base rate: **36%** of random dates fire. PA1 (Feb reached Earth) fails. PA2 (Jun) passes.

## Test B — CRaTER at the Moon (GOOD coincidence rate)
Null: 79 usable pseudo-meetings; 10th percentile D = −4.6%.

| Meeting | D | Percentile | Call |
|---|---|---|---|
| M1 | — | — | INDETERMINATE (early Feb SEP-flagged) |
| M2 | −1.9% | 39 | no dip |
| M3 | **−9.4%** | **1.3** | dip |
| M4 | −1.6% | 44 | no dip |

Thick-detector channel (secondary): M3 −9.0%, percentile 10.1 (just inside p10).
PB1: M3 yes, M4 no. PB2 (size 0.5–5%): **M3 fails** (too large), M4 passes.

## Ruling
- **February:** not seen at Earth's longitude at either meeting. The Earth-blind
  reading stands for it. M2 shows a strong compression with no speed-up, which
  the registered rule does not count.
- **June:** the claims rule is met at M3 (A fires and B dips at the same meeting;
  base rates 36% and 10%). If the two were independent, a random meeting would
  pass both about 4% of the time, and at least one of three scorable meetings
  about 10% of the time. That makes M3 suggestive, not strong.
- **Confound on M3, carried with the result:** the baseline days (May 29–Jun 1)
  sit in the decaying tail of the late-May solar particle event. The 1.5× SEP flag
  did not catch them (thin-detector rate 1.6–1.9 vs a quiet 1.1). An inflated
  baseline makes D too negative, which is also why PB2 fails.
- **Post-hoc check (flagged; computed after scoring):** against quiet levels
  (April 28.3, Jun 16–Jul 8 28.1), early June (Jun 2–7) sits at 27.0, with the
  minimum 26.6 on Jun 6 (≈ −4 to −6%). A modest cosmic-ray low 1–3 days after
  the Jun 4 interface remains, near the top of the registered size range. Slow
  recovery from the May 10 Forbush decrease cannot be ruled out with this data.
- **M4 bound:** any cosmic-ray suppression at the Moon from the Jul 1 passage was
  smaller than about 4.6%.

## Lessons for c2
- The SEP flag (1.5× window median of the thin detector) misses decay tails.
  A c2 rule should flag days until the thin rate returns within about 20% of quiet.
- CRaTER changes acceptance settings within a day during SEP days; 13 of 14
  dropped days were setting changes, almost all in SEP periods.
- Data gap: 2024-06-19 and 06-20 are missing from PDS (404).

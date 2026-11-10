# Lunar radiation campaign (lunar orbit), built on the Mars structure

In August 2026 the system took the structure it had learned at Mars and pointed it at the Moon. It did not start from nothing: it carried over which drivers matter, and it wrote down in advance one thing it expected to flip. At Mars the atmosphere soaks up solar particle events and surface dose goes down. The Moon has no atmosphere, so the prediction was that the same events would push dose up. That is what the lunar data showed. Same Sun, opposite signs, ordered by shielding.

The data is dose in lunar orbit from the CRaTER instrument on the Lunar Reconnaissance Orbiter, seventeen years of it.

The headline finding is about warnings. In the first half of 2024 the system found three episodes where dose at the Moon rose by large factors while Earth's official solar-event catalog had nothing. Each was missed in a different way, and each was confirmed by an independent spacecraft in lunar orbit.

What is open: the Earth's magnetotail seems to affect lunar dose in the opposite direction to the textbook, and that is unexplained. And nothing here comes from the surface.

What is needed: access to the one surface dataset that exists, and monitoring near the Moon instead of relying on Earth-side alerts.

_Rendered from the briefing record. Items marked internal in the ledger (how the framework works, the state of the record) stay in `ledger.json` and are not shown here._

Record quality: reconstructed. The cycle-by-cycle run reports for this campaign were lost with a laptop. This debrief is rebuilt from what survives: the campaign's published summaries, two published figures with their data, and the stored model records from August 2026. The stored model records hold more than numbers: each relationship carries the cycle it was admitted in, the admission statistic, the prediction registered for it, and what was learned. So for this mission you can say which hypotheses were tried, which cycle admitted or refuted each one, and with what numbers. What you cannot give is the reasoning text of each cycle. If someone asks for that, say the run reports are not available for this mission.

**Standing.** Certified 0. Accepted 6. Refuted 0. Open gaps 5. An open gap is an input or question nobody has settled; it is not a finding and has no standing.

## Findings

| id | kind | standing | basis | cycles |
|---|---|---|---|---|
| F1 | learned | **accepted** | sign flip registered before the lunar data was used; learned weight positive in both regions (stored model record) | v1 seed |
| F2 | discovery | **accepted** | each episode confirmed by an independent spacecraft in lunar orbit | run reports not available; figure data |
| F3 | learned | **accepted** | admitted under the standing rule in version one: loop cycle two in the magnetotail, loop cycle six in the solar wind; admission statistics stored | v1 c2 (magnetotail), v1 c6 (solar_wind) |
| F4 | learned | **accepted** | registered as a blind-recovery target; admitted under the standing rule in loop cycle six of version one | v1 c6, v2 c4 |
| F5 | learned | **accepted** | the flux-linear form confirmed its ceiling prediction and failed its fit-gain prediction in loop cycle five of version one; the storm-and-quiet split in version three re-admitted the same drivers | v1 c5, v3 seed |
| F6 | learned | **accepted** | admitted under the standing rule in loop cycle seven of version one, at the margin | v1 c7 |

## Cycles, in order

| cycle | dated | by | kind | written first | verdict |
|---|---|---|---|---|---|
| 1 | 2026-10-18 | Nervous Machine (Heidi Bennett; Claude Code as the operating agent) | learning | yes | mixed |

## Gaps, in the order that would settle things fastest

| priority | gap | status | closes with | who could act | signal expected | resolution by |
|---|---|---|---|---|---|---|
| 1 | Nothing is measured at the lunar surface | immovable | the Chang'e-4 lander's dosimeter series from the far side, as a data cycle under the instrument team's name and terms; a dosimeter at the surface, read hourly | the instrument team that holds the data; the first rover or lander team | an hourly surface dose series over at least one solar rotation, from the Chang'e-4 lander's dosimeter or a new lander | none registered |
| 2 | Earth-side alerts miss events at the Moon | in cycle | a dose monitor in the lunar vicinity whose alerts do not wait on Earth's catalog | an operator with a lunar-orbit or surface asset | a lunar-vicinity dose monitor whose alert times can be set against Earth's catalog over one season | none registered |
| 3 | The magnetotail effect runs opposite to the textbook | in cycle | more days that are both in the magnetotail and stormy, which in practice means a surface or far-side stream | a lunar surface or far-side instrument team | enough days that are both inside the magnetotail and geomagnetically stormy, from a surface or far-side instrument, to re-test the sign | none registered |
| 4 | Crew transit dose to Mars has never been measured continuously | immovable | a small hosted dosimeter on any Mars-bound flight, read hourly | a rideshare provider | a continuous hourly dose series from a spacecraft on a Mars-bound trajectory | none registered |
| 5 | Do solar-wind structures seen at Mars reach the Moon? | in cycle | a second cycle (c2) under the amended particle flag written in the c1 report, on the public CRaTER and OMNI data, pre-registered first | anyone; the data is public at PDS and SPDF and the rule is written | a c2 whose both base rates and the M3 statistic are printed; agreement with c1 at M3 under a clean baseline, or not | none registered |

_Generated by DEBRIEF tools/render.py from ledger.json; protocol 0.1.0._

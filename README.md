# DEBRIEF-space-lunar

A DEBRIEF mission record (protocol https://github.com/Nervous-Machine/DEBRIEF): a radiation learning campaign on
seventeen years of lunar-orbit dose data, seeded in August 2026 from the structure learned at Mars, plus the first
pre-registered cross-check that followed it. The ledger is `ledger/lunar.json`; everything else is rendered from it
or is the material of a cycle.

**Standing.** Certified 0. Accepted 6. Refuted 0 in the briefing record (one control refuted, kept internal). Open
gaps 5. Certainty is set aside for this mission; nothing is certified, and the record says so.

**Record quality: reconstructed.** The cycle-by-cycle run reports of the August campaign are not available. The
findings are rebuilt from the campaign's published summaries, two published figures with their data, and the
stored model records, which carry for each relationship the cycle that admitted it, the admission statistic and the
prediction registered for it. Cycle 1 in this repository (October 2026) is a full-record cycle.

## What is in the record

- **Six accepted findings** from the campaign, among them: solar particle events raise dose at the Moon and lower
  it at the surface of Mars (sign flip registered in advance); Earth's catalog missed three dose episodes at the
  Moon in the first half of 2024; deeper in the magnetotail means higher dose, a lunar-native hypothesis admitted
  under the standing rule.
- **Cycle 1 (2026-10-18).** Did the two 2024 solar-wind stream interfaces found at Mars reach the Moon? Rule written
  first, base rates printed. February: not seen at Earth's longitude. June: the rule was met at one meeting, with a
  solar-particle tail in the baseline. Suggestive, not strong. Files in `c1/`.
- **Five open gaps**, in `ASKS.md`, each with the kind of contribution that would close it. The first is the lunar
  surface: nothing in this record is measured there.

## Where contributions land

- **Surface dose data.** The Chang'e-4 lander's LND dosimeter is the one long-running surface measurement. A
  `data` cycle from whoever can supply it moves the surface gap from immovable to in cycle, under the supplier's
  name and terms. Use the **Data contribution** issue form.
- **Cycle 2.** The c1 report ends with the rule fix a second cycle needs (a particle flag that catches decay
  tails). The CRaTER and OMNI data are public. Pre-register, run, submit a **Rerun report**.
- **A lunar-vicinity dose monitor** whose alerts do not wait on Earth's catalog, from any operator with an asset.

Every contribution is one dated cycle in the ledger under the contributor's own name, listed in `CITATION.cff` and
in each release. Rules and templates: https://github.com/Nervous-Machine/DEBRIEF/blob/main/CONTRIBUTING.md.

## Layout

```
ledger/lunar.json     the ledger (protocol 0.1.0)
SCORECARD.md          findings, cycles, gaps (generated)
ASKS.md               open gaps and what closes each (generated)
c1/                   cycle 1: pre-registration + hashes, code, results, report
cycles/               contributed cycles, one file each
CITATION.cff          how to cite; contributors of record
LICENSE               Apache-2.0 (code); LICENSE-CONTENT: CC-BY-4.0 (ledger text, reports)
```

## Sources

Published page "Atlas of Useful Space: Moon and Mars"; figures "Three Ways to Miss the Moon" and "Two Channels,
Three Worlds"; stored model records (August 2026); LRO CRaTER L2 SEC (PDS PPI); OMNI2 (NASA SPDF); JPL Horizons.

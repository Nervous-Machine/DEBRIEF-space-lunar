# Contributed cycles

One file per contribution, written from the issue forms or by hand from the templates in
https://github.com/Nervous-Machine/DEBRIEF/tree/main/templates. The validation workflow merges these into the
ledger before checking it. Files here are never edited after merge; a correction or withdrawal is a new file.

Maintainer step after a cycle's pull request is merged: run `merge_cycles.py ledger/lunar.json cycles` in place, re-render
`SCORECARD.md` and `ASKS.md`, add the contributor to `CITATION.cff`, and commit. Until then the merged cycle is checked
by CI on every run but is not yet written into the committed ledger.

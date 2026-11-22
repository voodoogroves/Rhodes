# Decisions

Append-only. One line per real choice: date, decision, why.

- 2026-11-22: Hub repo is **Rhodes** (the harbor, Colossus at the entrance). Naming draws on the Seven Wonders; names are picked only when something needs a home.
- 2026-11-22: **Alexandria** (the Pharos) holds knowledge: curated topical memory and generated output, in separate subdirectories (`memory/`, `output/`) so generated material is never mistaken for a source of truth.
- 2026-11-22: Both repos private. Claude connects through the Claude GitHub App rather than a personal access token (least privilege, nothing to leak).
- 2026-11-22: Rhodes is the base for the personal work surface. Issues vs a Project board is undecided.
- 2026-11-22: **No commits to main.** Work happens on a `draft` branch and merges by PR, even when the merge is immediate. Rhodes may later grow a richer branch model.

# Decisions

Append-only. One line per real choice: date, decision, why.

- 2026-11-22: Hub repo is **Rhodes** (the harbor, Colossus at the entrance). Naming draws on the Seven Wonders; names are picked only when something needs a home.
- 2026-11-22: **Alexandria** (the Pharos) holds knowledge: curated topical memory and generated output, in separate subdirectories (`memory/`, `output/`) so generated material is never mistaken for a source of truth.
- 2026-11-22: Repos are **public but private-information-free**: nothing sensitive is ever committed. Only Chris commits to and changes them; outside PRs against project repos may be entertained, never expected. Claude chat connects through the Claude GitHub App; local git/gh use OAuth (device flow, token in the keyring), never a hand-made personal access token.
- 2026-11-22: Rhodes is the base for the personal work surface. Issues vs a Project board is undecided.
- 2026-11-22: **Never commit to main**, in any repo. Work happens on a working branch and merges by PR, even when the merge is immediate. Working branches are named for the repo's function: `dev` in Rhodes (development), `draft` in Alexandria (content). Project repos use typed branches (`bug/`, `feature/`, etc.). Keep the working branch fast-forwarded to `main` between pieces of work.
- 2026-11-22: The workspace-level `CLAUDE.md` lives in Rhodes (`workspace/CLAUDE.md`) so it is versioned, and `~/Repos/CLAUDE.md` is a symlink to it. It imports `Rhodes/CLAUDE.md` by absolute path so Rhodes's relative paths resolve correctly.
- 2026-11-22: **Work-surface flow.** Rhodes is the real work space (drafts and speculation in `scratch/`). Project repos hold only verified, true specs; when testing shows a spec is wrong, update the spec. Alexandria archives shelved or superseded work under `historical/<project>/` and keeps finished knowledge in `memory/`. Retired Rhodes scratch is archived to Alexandria, not just deleted.

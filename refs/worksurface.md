# Work surface

Orientation for any assistant starting cold, on any machine (chat, iPad, Mac, Steam Deck). Everything here was stated by the owner or is in `decisions.md`. Open questions are listed at the bottom, not guessed at.

## Naming

The personal side draws on the Seven Wonders of the Ancient World. A name is picked only when something needs a home, and it needs a story. This is separate from the Sumerian naming used at work.

## Where things live

| Place | Role |
|---|---|
| **Rhodes** (this repo) | The harbor. Hub and base for the work surface. Common scripts and anything that applies across projects live here. Brainstorming lives here too, in `scratch/`. |
| **Alexandria** | Knowledge. Curated, topical (not general) memory plus generated output. Kept in separate subdirectories (`memory/`, `output/`) so generated material is never mistaken for a source of truth. |
| **Project repos** | One repo per produced project. They dock to Rhodes and hold the work itself. Current: `fo4-pax`, `fo4-regalia-of-mystery`. |

All repos are under the GitHub account `voodoogroves`.

## Brainstorming

Ideas start as `scratch/<idea>/` in Rhodes, one folder or file per idea. It is not known up front whether an idea is one project, so don't promote it to its own repo until it needs one. Current scratch folders: `pax`, `regalia-of-mystery`.

## Branches

- Never commit to `main`.
- Work on the repo's working branch and merge by PR, even when the merge is immediate.
- Working branch is named for the repo's function: `dev` in Rhodes, `draft` in Alexandria.
- Keep the working branch fast-forwarded to `main` between pieces of work.
- This is a shared habit, not enforced by GitHub. Nothing blocks a push to `main`, so check the branch before committing.
- Project repos: typed working branches (`bug/`, `feature/`, etc.).

## How assistants reach the repos

- Chat (claude.ai, mobile): through the Claude GitHub App, not a personal access token. Empty repos (public, no private information) are created on GitHub and added to the app; the assistant attaches and pushes.
- Steam Deck: Claude Code via the VS Code extension. Install VS Code (Flatpak) and the extension from the Microsoft marketplace. Avoid Open VSX: a compromise of the Claude Code extension there (v2.1.313) was reported on 2026-10-30. The report is unverified.

## Steam Deck

Role: local Fallout 4 dev and testing, with Mod Organizer 2 (MO2). Setup is in progress. The owner may want help with MO2.

## Projects

- **fo4-pax**: personal Fallout 4 mod project.
- **fo4-regalia-of-mystery**: another Fallout 4 idea.

Where each project's plans and specs live (project repo vs Rhodes) is undecided.

## Open questions

- Issues vs a Project board for tracking (undecided, see `decisions.md`).
- Ground rules: still being defined. Do not invent more.
- Alexandria's exact structure beyond `memory/` and `output/`.
- Branch convention in project repos.
- Where the repos are cloned on the Steam Deck.

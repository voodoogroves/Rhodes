# Work surface

Orientation for any assistant starting cold, on any machine (chat, iPad, Mac, Steam Deck). Everything here was stated by the owner or is in `docs/decisions.md`. Open questions are listed at the bottom, not guessed at.

## Naming

The personal side draws on the Seven Wonders of the Ancient World. A name is picked only when something needs a home, and it needs a story. This is separate from the Sumerian naming used at work.

## Where things live

| Place | Role |
|---|---|
| **Rhodes** (this repo) | The harbor. Hub and base for the work surface. Common scripts and anything that applies across projects live here. Brainstorming lives here too, in `scratch/`. |
| **Alexandria** | Knowledge and the archive. Curated, topical (not general) memory, generated output, and archived ideas, kept in separate subdirectories (`memory/`, `output/`, `historical/`) so generated or old material is never mistaken for a source of truth. |
| **Project repos** | One repo per produced project. They dock to Rhodes and hold the work itself. They hold specs and work that are ready to build from, kept true as we learn. Current: `fo4-pax`, `fo4-regalia-of-mystery`. |

All repos are under the GitHub account `voodoogroves`.

## Brainstorming

Ideas start as `scratch/<idea>/` in Rhodes, one folder or file per idea. It is not known up front whether an idea is one project, so don't promote it to its own repo until it needs one. Current scratch folders: `pax`, `regalia-of-mystery`.

## How work flows

Organised by confidence:

1. **Brainstorming and fleshing out a concept: Rhodes** (`scratch/`).
2. **Ready to the point we might write code: the project repo.** The spec lives there, open items allowed. If we drift or learn something, update the spec in the project so it stays true.
3. **Old or no longer relevant: Alexandria** (`historical/<project>/`; finished knowledge in `memory/`). We may purge from Alexandria later. Retired scratch is archived there, not just deleted.

This keeps the work surface and the working projects clean.

## Repo layout

`README.md` and `CLAUDE.md` at the root; specs, decisions, notes and working docs in `docs/`. Details: `docs/memory-system.md`.

## Branches

- Never commit to `main`.
- Work on the repo's working branch and merge by PR, even when the merge is immediate.
- Working branch is named for the repo's function: `dev` in Rhodes, `draft` in Alexandria.
- Keep the working branch fast-forwarded to `main` between pieces of work.
- This is a shared habit, not enforced by GitHub. Nothing blocks a push to `main`, so check the branch before committing.
- Project repos: typed working branches (`bug/`, `feature/`, etc.).
- Across devices (Rhodes): `dev` is the one meeting point. Phone and tablet sessions branch from `dev` and open PRs into `dev`; only `dev` merges to `main`. Commit each change on one branch only. Start a session by reading the idea's `handoff.md` ([convention](../scratch/README.md)) and end it by rewriting it.

## How assistants reach the repos

- Chat (claude.ai, mobile): through the Claude GitHub App, not a personal access token. Empty repos (public, no private information) are created on GitHub and added to the app; the assistant attaches and pushes.
- Steam Deck: Claude Code via the VS Code extension. Install VS Code (Flatpak) and the extension from the Microsoft marketplace. Avoid Open VSX: a compromise of the Claude Code extension there (v2.1.313) was reported on 2026-10-30. The report is unverified.

## Steam Deck

Role: local Fallout 4 dev and testing, with Mod Organizer 2 (MO2). Setup is in progress. The owner may want help with MO2.

## Working habits

- One session builds a mod. Research sessions stay read-only and pass notes or a handoff to it.
- Put all open questions in one place; do not split them between a document and chat.
- `gh` is at `~/.local/bin/gh`, which is not on PATH in an assistant's shell.

## Projects

- **fo4-pax**: personal Fallout 4 mod project.
- **fo4-regalia-of-mystery**: another Fallout 4 idea.

A project's specs live in its repo, in `docs/`.

## Open questions

- Issues vs a Project board for tracking (undecided, see `docs/decisions.md`).
- Ground rules: still being defined. Do not invent more.
- Alexandria's exact structure beyond `memory/`, `output/` and `historical/`.
- Branch convention in project repos.
- Where the repos are cloned on the Steam Deck.

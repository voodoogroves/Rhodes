# Concept spec: tiered, topical memory with context prep (2026-11-25)

Status: **concept, not built.** Drafted from a brainstorm with Chris. Open items are at the bottom; nothing here is logged in `decisions.md`.

## Problem

Claude's built-in memory and `CLAUDE.md` load every session. Some knowledge should not: FO4-mod gotchas matter only on FO4 work; lookup material (tool usage, record layouts) matters only when a task touches it. We want that knowledge kept, kept current, and loaded **when we know what we are working on**.

## Principles

1. **Lightweight.** A memory is one markdown file with frontmatter. No database, no embeddings, no service.
2. **Match on frontmatter, load the whole doc.** Selection reads only `name`, `description` and `applies-to`. A matched doc is read in full. Never load part of one.
3. **Loading is a step, not a hope.** At session start there is a "context prep" step that resolves the project and loads matches.
4. **Scoped by what it governs.** Work-surface, type, project (see tiers).
5. **Short docs.** If a doc needs a page of explanation, split it; the gotcha doc points to the lookup doc.
6. **Public and clean.** Nothing private; no game assets (see `decisions.md`, 2026-11-22 and 2026-11-24). Describe how to make things, never hold them.

## Tiers

| Tier | Holds | Loaded | Lives in |
|---|---|---|---|
| 0 Always | Working style, git rules, how the work surface works | Automatically, every session | `~/Repos/CLAUDE.md`, Rhodes `CLAUDE.md`, Claude's own memory index |
| 1 Type | Gotchas and lookups for a *kind* of project (e.g. `fo4-mod`) | By prep, on frontmatter match | Alexandria `memory/<type>/` |
| 2 Project | State, specs and decisions of one repo | By prep, when working in it | The project repo (`NOTES.md`, `decisions.md`, spec) |

Decisions are scoped the same way: work-surface decisions stay in `Rhodes/decisions.md`; project decisions go in the project repo; rules for a whole type (e.g. never commit game assets) go in that type's gotchas.

## The doc format

```markdown
---
name: fo4-mswp-swaps
description: One line saying what this is and when to use it.
applies-to: [fo4-mod]          # type tags and/or project names
kind: gotcha | lookup          # gotcha = read at project start; lookup = read when a task touches it
verified: 2026-11-24           # date last confirmed
confidence: verified | decoded | unverified
---
Body. Short. Facts first; "Why" and "How to apply" where useful.
```

- `kind: gotcha` docs load at project start (whole doc). `kind: lookup` docs load only when their `description` matches the task.
- `verified` and `confidence` let prep flag stale or unproven entries.
- This mirrors the frontmatter Claude's own memory files already use, so one habit covers both.

## Layout

```
Alexandria/memory/
  index.md                  # optional; generated or hand-kept one line per doc
  fo4-mod/
    <name>.md ...           # gotchas and lookups, each with frontmatter
  papyrus/ ...
<project-repo>/
  CLAUDE.md                 # carries the project header (below)
  NOTES.md, decisions.md    # tier 2, same frontmatter
```

Project header, in each repo's `CLAUDE.md`:

```
project: fo4-regalia-of-mystery
types: [fo4-mod]            # a list; a repo can have more than one type
prep: run context prep before starting work
```

## Context prep (the retrieval step)

1. Tier 0 is already loaded.
2. Read the project header; get `project` and `types`.
3. List frontmatter (only) of `Alexandria/memory/<type>/*.md` and of the repo's own docs.
4. Load whole: every doc with `kind: gotcha` whose `applies-to` includes the project or a type; the project's `NOTES.md` and `decisions.md`.
5. Do **not** load `kind: lookup` docs yet. Keep their name and description in view.
6. Say in two lines what was loaded and which lookups exist. Chris can add or correct.
7. **Mid-session:** when a task touches a lookup's description, or the work type changes, repeat steps 3 to 6 for the new match.

Selection is done by the model reading the frontmatter lines. A small helper script (`scripts/memory/memindex.py`: print `name | kind | applies-to | verified | description` for given directories) is optional and is only for speed and clean output.

## Write-back

At wrap-up (or when Chris says "log this"), propose where each new fact belongs and wait for approval: gotcha or lookup to Alexandria `memory/<type>/`; a project fact to the repo; a work-surface decision to `decisions.md`. Update an existing doc rather than adding a duplicate; refresh `verified`.

## Starting content (proposed seed)

Move or write, then add frontmatter:
- From Rhodes `refs/`: `fo4-archives.md` (lookup), `steam-deck-mo2.md` (lookup or gotcha; to be sorted).
- New `fo4-mod` gotchas, mined from `scratch/regalia-of-mystery/*` and the build session transcript (`~/.claude/projects/-home-deck-Repos/162a0f18-a17d-4d77-a39f-bff301f7c662.jsonl`): copy/paste block, MSWP ADD-not-REM, colour remap index on the OMOD, `.esl` constraints, MO2 on the Deck, never commit game assets.
- Lookups: ENCH to MGEF to PERK chain, magazine anatomy, hazard/gas mechanism, disease system.

## Non-goals

No vector search, no auto-capture, no cross-repo sync tooling. No enforcement hooks at first.

## Build order (suggested)

1. Settle the open items below.
2. Create `Alexandria/memory/fo4-mod/` and move `fo4-archives.md` there with frontmatter.
3. Write the project header in `fo4-regalia-of-mystery/CLAUDE.md`.
4. Write 3 to 5 gotcha docs; try prep on a fresh session; adjust.
5. Add `/prep` (skill or command) or `memindex.py` only if the plain rule gets skipped or is slow.
6. Log the settled choices in `decisions.md` when Chris says so.

## Open items

- Does `steam-deck-mo2.md` stay in Rhodes `refs/` (work surface) or move to Alexandria (type knowledge)? (Memories go to Alexandria per Chris; this one is not yet sorted.)
- Settled by Chris (2026-11-25): memories live in Alexandria. Alexandria is new, so there is no strong convention to follow; this spec sets it.
- Rule vs `/prep` skill as the trigger; start with the rule.
- Tag vocabulary: keep type names flat and few (`fo4-mod`, `papyrus`, `steam-deck`); decide whether tags like `xedit` are allowed.
- How `CLAUDE.md` `@imports` and Claude's own memory interact with this; avoid duplicating tier 0 content into tier 1.
- Alexandria branch is `draft`; Rhodes is `dev`; both merge by PR.

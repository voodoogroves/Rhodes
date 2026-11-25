# Build spec: tiered, topical memory with context prep

State as of **2026-11-25**. Replaces the concept spec (Alexandria `historical/memory-system/`).

## 1. Purpose

Keep knowledge that should not load every session, keep it current, and load it when we know what we are working on. Lightweight: markdown files with frontmatter, one small script, no database, embeddings or service.

## 2. Tiers

| Tier | Holds | Loaded | Lives in |
|---|---|---|---|
| 0 Always | Working style, git rules, how the work surface works | Automatically | `CLAUDE.md` files, Rhodes `refs/`, Claude's own memory |
| 1 Type | Gotchas and lookups for a kind of project | By prep | Alexandria `memory/<type>/` |
| 2 Project | State, specs and decisions of one repo | By prep | The project repo |

A fact lives in one tier. Tier 1 and 2 content is not copied into `CLAUDE.md` or Claude's memory. No `@imports` of tier 1 docs.

Decisions are scoped the same way: work surface in Rhodes `docs/decisions.md`; one project in its repo; a rule for a whole type in that type's gotchas.

## 3. Memory doc

```markdown
---
name: fo4-example
description: One line: what this is and when to read it.
applies-to: [fo4-mod]
kind: gotcha
verified: 2026-11-25
---
Body.
```

| Field | Rule |
|---|---|
| `name` | Equals the file name without `.md`; unique across `memory/` |
| `description` | One line. For a lookup it is the whole basis for selection |
| `applies-to` | One or more known types |
| `kind` | `gotcha` (read at prep) or `lookup` (read when a task matches) |
| `verified` | `YYYY-MM-DD` the content was last confirmed |

- All five are required. How each fact is known stays inline: *(in game)*, *(xEdit)*, *(inferred)*, *(upstream)*.
- A doc is read whole or not at all.
- Size limits: a gotcha is at most 60 body lines and 5,000 characters; a lookup at most 20,000 characters. Over the limit, split it.
- A gotcha states the rule briefly and names the lookup that explains it.
- Facts only: nothing private, no game assets (Rhodes `docs/decisions.md`).

**Types:** `fo4-mod` only. Add a type to `TYPES` in the script when a second project type needs it. Folders under `memory/` are for tidiness; matching uses `applies-to`.

## 4. Project header

One line in the project's `CLAUDE.md`:

```
types: [fo4-mod]
```

The project name is the directory name.

## Repo layout

Every repo, Rhodes included:

| Where | Holds |
|---|---|
| Root | `README.md` (what it is, what to read first) and `CLAUDE.md` |
| `docs/` | Specs, `decisions.md`, `notes.md`, working docs. No file or subfolder is required |

The README says what is in `docs/`. Folders with their own job (`scripts/`, `build/`, Rhodes `refs/` and `scratch/`) stay.

## 5. Context prep

**Trigger:** the first time a project is named or one of its files is touched in a session, before acting on it. Also when the work moves to another project or type. The starting folder is not relied on. The rule is in Rhodes `CLAUDE.md`; each project `CLAUDE.md` repeats it.

**Steps:**
1. Run `python3 ~/Repos/Rhodes/scripts/memory/memindex.py ~/Repos/<project>`.
2. Read every doc under **Read now**, whole.
3. Read the project's `README.md` and what it says to start with, plus `docs/decisions.md` and `docs/notes.md` if present. Neither file is required.
4. Keep the lookup list in view. Read a lookup, whole, when a task matches its description.
5. Report in two lines: what was read, which lookups exist. The owner corrects or adds.

With no known project yet, `--type fo4-mod` lists a type's docs.

## 6. Script: `scripts/memory/memindex.py`

Standard-library Python, read only. Prints paths and descriptions, never bodies (long shell output is truncated).

| Call | Does |
|---|---|
| `memindex.py <project-dir>` | Types from the project header; lists gotchas, lookups, project files |
| `memindex.py --type <t> [--type <t>]` | Same, without a project |
| `memindex.py --check` | Validates every doc; prints only problems and a count |
| `--memory <dir>` | Overrides the default, `Alexandria/memory` beside Rhodes |

Exit 1 on any problem: missing or malformed field, name mismatch, duplicate name, unknown type, over size, missing header, missing memory directory. Valid docs are still listed. A `verified` date over 90 days old is marked `STALE` and is not an error.

Tests: `python3 scripts/memory/test_memindex.py`.

## 7. Write-back

At wrap-up, or on "log this", propose where each new fact goes and wait for approval: gotcha or lookup in Alexandria; project fact in its repo; work-surface decision in `docs/decisions.md`. Update an existing doc before adding one, refresh `verified`, then run `--check`. Alexandria changes go on `draft` and merge by PR.

### Mine (find new learnings)

On "mine" (e.g. "let's mine for new learnings"):
1. Read the last line of Alexandria `memory/mined.log`. If there is none, ask how far back to go.
2. Read what changed since then: session transcripts in `~/.claude/projects/` (search them; they are large), project docs and Rhodes `scratch/`.
3. Compare with the existing docs.
4. Propose each finding with its target doc, source and evidence tag. Write only what is approved.
5. Copy nothing private into a repo; they are public.
6. Append the pass date and what was covered to `mined.log`.

### Curate (tend the library)

On "curate" (e.g. "let's curate the library"):
1. Run `memindex.py --check`.
2. Look for duplicates, contradictions, stale or oversized docs, and gotchas that should be lookups or the reverse.
3. Propose merges, splits and removals; apply what is approved. Retired docs go to Alexandria `historical/`.
4. Refresh `verified` only for facts rechecked, not merely reread.
5. Run `--check` again.

## 8. What catches drift

| Drift | Caught by |
|---|---|
| Bad frontmatter, oversized doc, unknown type | The script, at every prep |
| Old facts | The `STALE` mark |
| Prep skipped | **Nothing mechanical.** The two-line report is missing; the owner notices. If this happens, add a hook |

## 9. Seed content (moves)

| Was | Now in Alexandria `memory/fo4-mod/` |
|---|---|
| Alexandria `memory/fo4-modding-mechanics.md` | `fo4-perks-and-damage`, `fo4-weapon-mods-and-names`, `fo4-guns-sound-and-impact`, `fo4-materials-and-models`; testing notes into `fo4-testing` |
| Alexandria `memory/fo4-xedit-reference.md` | `fo4-xedit-scripting`, `fo4-xedit-lookup`, `fo4-vanilla-records`, and the perk and material docs above |
| Its Blade armor-penetration test results | `fo4-regalia-of-mystery/docs/history-armor-penetration-tests.md` |
| Rhodes `refs/fo4-archives.md` | `fo4-archives` |
| Rhodes `refs/steam-deck-mo2.md` | `fo4-deck-mo2-setup`, `fo4-xedit-install`, `fo4-deck-workflow`, `fo4-testing` |

New gotchas, distilled from the above: `fo4-gotchas-build`, `fo4-gotchas-records`, `fo4-gotchas-testing`. Scripts stay in Rhodes `scripts/`. Older notes in `scratch/` and `historical/` keep their old paths; use this table.

## 10. Acceptance

In a fresh session started in `~/Repos`, say "let's work on the Voice of Set". Pass:
1. Prep runs before any file is written.
2. All three gotchas are read.
3. No lookup unrelated to the task is read.
4. The two-line report appears.

## 11. Not doing

Vector search, auto-capture, cross-repo sync, a `/prep` skill, hooks, one skill per memory.

## 12. Open

- A `CLAUDE.md` header for `fo4-pax` when work starts there.

# How the memory system works

As built, 2026-11-25. The short version; exact rules are in [`memory-system.md`](memory-system.md).

**The idea:** keep what we learn, and load it only when we are working on something it applies to. It is markdown files and one small script.

## Where things live

| What | Where | When it is read |
|---|---|---|
| How we work | `CLAUDE.md`, Rhodes `refs/`, Rhodes [`decisions.md`](decisions.md) | At the start |
| What we know about a kind of project | Alexandria `memory/<type>/` | When a project of that type comes up |
| What is true of one project | That repo: `README.md` and `docs/` | When working on it |
| Old or retired material | Alexandria `historical/` | Only if asked; never a source of truth |

There is one type so far, `fo4-mod`.

## Two kinds of memory doc

- **Gotcha:** a short rule that avoids a known mistake. All of them are read for the project's type.
- **Lookup:** reference detail. Read only when the task matches its description.

Each doc starts with a header, and is always read whole:

```markdown
---
name: fo4-example
description: One line saying what this is and when to read it.
applies-to: [fo4-mod]
kind: lookup
verified: 2026-11-25
---
```

## What happens in a session

1. You name a project ("let's work on the Voice of Set").
2. The assistant runs the prep script on that repo. The repo's `CLAUDE.md` says its type (`types: [fo4-mod]`).
3. The script lists the matching docs and the project's files.
4. The assistant reads the gotchas and the project README, picks up lookups as the task needs them, and says what it read.

```
python3 ~/Repos/Rhodes/scripts/memory/memindex.py ~/Repos/fo4-regalia-of-mystery
```

## What you say

| You say | What happens |
|---|---|
| A project name | Context prep, as above |
| "Log this" | A proposal for where it belongs; written once you approve |
| "Mine" | New learnings are gathered from sessions and docs since the last pass, proposed, then written once you approve. The pass is recorded in `memory/mined.log` |
| "Curate" | The library is checked for duplicates, contradictions and stale docs; changes are proposed first |

## Keeping it healthy

| Command | Does |
|---|---|
| `python3 ~/Repos/Rhodes/scripts/memory/memindex.py --check` | Checks every doc's header and size |
| `python3 ~/Repos/Rhodes/scripts/memory/test_memindex.py` | Tests the script |

- A gotcha is at most 60 lines and 5,000 characters; a lookup at most 20,000 characters.
- A doc not verified for 90 days is marked `STALE`.
- Memory is public: nothing private and no game assets.

## Adding things

- **A doc:** add it under `memory/<type>/` with the header, then run `--check`. Prefer updating an existing doc.
- **A project:** put `types: [fo4-mod]` and the prep instruction in its `CLAUDE.md` (copy Regalia's).
- **A type:** add it to `TYPES` in `memindex.py`, then write its docs.

## Limits

- Nothing forces prep to run. If the report is missing, ask for it.
- Prep was tested once, in a fresh session on 2026-11-25: the right docs were read before any change, but the report did not list the unread lookups.
- "Curate" has not been run yet.
- Only if these cause real trouble do we add more (a hook or a checking script).

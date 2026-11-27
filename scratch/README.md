# Scratch

Brainstorming and fleshing out concepts, one folder per idea. Not a source of truth; ideas that are ready to build from move to their project repo. Flow: [`refs/worksurface.md`](../refs/worksurface.md).

## Handoffs (phone and chat to any machine, and back)

Each idea may have one `handoff.md` at `scratch/<idea>/handoff.md`. It is the in-flight state a session leaves for the next one, from any client (claude.ai, mobile, VS Code on Linux, Steam Deck, Mac).

- **Overwrite, don't append.** It describes now, not history.
- **Start a session by reading it; end a session by rewriting it.**
- **Read it on `dev`.** `dev` is the one meeting point: phone and tablet sessions branch from `dev` and open PRs into `dev`; only `dev` merges to `main`. Commit each change on one branch only.
- **Open questions live here, in one place**, not split with chat.
- It is a note, not a spec. Anything settled moves to the idea's `concept-spec.md`, and then to the project repo once ready to build from.
- Issues may later take over as the queue for this work (the dark factory). Undecided; see `docs/decisions.md`.

Template:

```markdown
# Handoff: <idea>
Updated: <date>, from <client>

## State
Where things stand, in a few lines.

## Next
The one thing the next session should do.

## Open questions
All of them, here.
```

## Index

Add a line when an idea gets a folder or its first handoff.

| Idea | Files | Handoff |
|---|---|---|
| `pax` | `concept-spec.md`, `modules.md`, `power-armor-durability.md` (Gemini, unvalidated), `notes-future-ideas.md` (parked ideas) | `handoff.md` |
| `regalia-of-mystery` | `concept-spec.md`, `checkpoint.md`, `notes-future-ideas-regalia.md` (parked ideas) | `checkpoint.md` predates this convention |
| `outfits` | `handoff.md` (scripts in `scripts/nif/`) | `handoff.md` |

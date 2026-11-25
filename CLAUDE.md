# Rhodes: instructions for assistants

Start cold. Read `docs/decisions.md` and `refs/` before acting.

- **Context prep:** the first time a project is named or touched, before acting on it, run `python3 ~/Repos/Rhodes/scripts/memory/memindex.py ~/Repos/<project>`. Read each "Read now" doc whole, then the project README and what it points to; read a lookup whole only when the task matches it. Report in two lines. Spec: `docs/memory-system.md`.
- New knowledge: propose where it belongs (Alexandria memory, the project repo, or `docs/decisions.md`) and wait for approval.
- On "mine" or "curate" (memory maintenance), follow section 7 of `docs/memory-system.md`.
- Never commit to `main`. Work on `dev`, open a PR, merge by PR.
- Durable choices go in `docs/decisions.md` as one line (only when the owner says "log this" or a real decision lands).
- Ground rules are still being defined; do not invent more.
- `refs/working-with-chris.md` is a strong prior on working style, not a rulebook.

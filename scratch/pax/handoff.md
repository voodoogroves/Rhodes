# Handoff: pax
Updated: 2026-11-26, from Steam Deck (VS Code)

**Any other device (phone, iPad):** branch from `dev` and open the PR into `dev`.

## State
- Design notes: [`modules.md`](modules.md) (start there; later sections replace earlier ones where they say so). [`concept-spec.md`](concept-spec.md) is the unverified starting draft. `fo4-pax` has only a README and `CLAUDE.md`.
- Left arm shield: shows and "blocking looks great" on the T-60 (in game, owner). Position accepted for now. Other suits checked offline only.
- **Not on `dev` at the time of writing:** uncommitted notes and scripts on the Deck, covering round 2 of the test plugin (all four tests reported passing in game), attachment cost and unlock, other suits, and fist weapons. If `modules.md` has no "Other suits and round 2" section, they are still only on the Deck.
- [`power-armor-durability.md`](power-armor-durability.md): Gemini note, nothing in it checked.

## Next
On the Deck: commit and push the uncommitted PAX work, so other devices can see it.

From phone or iPad: design only. Settle how attachments are unlocked (question 1).

## Open questions
1. Attachment unlock: use up the item as an ingredient, or learn it on finding it? Also a SPECIAL cost with an offset or drawback (owner leaning, not settled)?
2. How many attachments should PAX have, beside the skills that cost SPECIAL?
3. Which SPECIAL stat each augment costs (proposed table in `modules.md`, unconfirmed).
4. Prerequisites: Crushing Blows, Servo Control, Fire Suppression (on hold). Rank 2 requirements and the guard stance name.
5. v1 scope.
6. Creation Kit on the Deck, or another compiler (Caprica)?
7. Needs the game or xEdit: does `WornHasKeyword` see a vanilla mod on a worn suit; shield across re-entry, save and reload; shield fit on other suits; stat trade effects on owned perks, health and reload; durability note items 1 to 3.

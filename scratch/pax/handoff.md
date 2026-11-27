# Handoff: pax
Updated: 2026-11-26, from Steam Deck (VS Code)

**Any other device (phone, iPad):** branch from `dev` and open the PR into `dev`.

## State
- Design notes: [`modules.md`](modules.md) (start there; later sections replace earlier ones where they say so). [`concept-spec.md`](concept-spec.md) is the unverified starting draft. `fo4-pax` has only a README and `CLAUDE.md` (`types: [fo4-mod]`).
- Left arm shield: shows and "blocking looks great" on the T-60 (in game, owner). Position accepted for now. One model looks usable on all five suits (offline only).
- Round 2 proofs, no scripts, all passed in game: worn stat effects, suit-only perk (free sprint), suit-only lock prompt, crafting the shield from the super mutant gauntlet.
- Test plugin: `scratch/pax/test1/build_test1.py`, installed on the Deck as MO2 mod "PAX Test 1". Latest change, a one-gauntlet preview and dropped model (`scripts/nif/trimparts.py`), is installed and **not yet seen in game**.
- [`power-armor-durability.md`](power-armor-durability.md): Gemini note, partly checked; two setting or keyword names were wrong.
- Owner has an idea for a new power armor weapon, not yet described.

## Next
On the Deck, owner tests: the one-gauntlet preview and drop (pick-up, resting position), and `getgs fPowerArmorPCArmorDamageMultiplier`.

From phone or iPad: design only. Describe the weapon idea, or settle how attachments are unlocked (question 1).

## Open questions
1. Attachment unlock: use up the item as an ingredient, or learn it on finding it? Also a SPECIAL cost with an offset or drawback (owner leaning, not settled)?
2. How many attachments should PAX have, beside the skills that cost SPECIAL?
3. Which SPECIAL stat each augment costs (proposed table in `modules.md`, unconfirmed).
4. Prerequisites: Crushing Blows, Servo Control, Fire Suppression (on hold). Rank 2 requirements and the guard stance name.
5. v1 scope.
6. The new power armor weapon: what is it?
7. Slower armor wear: wanted in PAX? Which cost or drawback?
8. Creation Kit on the Deck, or another compiler (Caprica)?
9. Needs the game or xEdit: does `WornHasKeyword` see a vanilla mod on a worn suit; shield across re-entry, save and reload; shield fit on other suits; stat trade effects on owned perks, health and reload; durability note items 2 and 4.

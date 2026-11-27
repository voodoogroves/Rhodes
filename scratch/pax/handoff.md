# Handoff: pax
Updated: 2026-11-27, from Steam Deck (VS Code)

**Any other device (phone, iPad):** branch from `dev` and open the PR into `dev`.

## State
- Design notes: [`modules.md`](modules.md) (start there; later sections replace earlier ones where they say so). [`concept-spec.md`](concept-spec.md) is the unverified starting draft. `fo4-pax` has only a README and `CLAUDE.md` (`types: [fo4-mod]`).
- Left arm shield: shows and "blocking looks great" on the T-60 (in game, owner). Position accepted for now. One model looks usable on all five suits (offline only).
- Round 2 proofs, no scripts, all passed in game: worn stat effects, suit-only perk (free sprint), suit-only lock prompt, crafting the shield from the super mutant gauntlet.
- Test plugin: `scratch/pax/test1/build_test1.py`, installed on the Deck as MO2 mod "PAX Test 1". Latest change, a one-gauntlet preview and dropped model (`scripts/nif/trimparts.py`), looks good in game.
- [`power-armor-durability.md`](power-armor-durability.md): Gemini note, partly checked; two setting or keyword names were wrong. Slower wear is now a SPECIAL-cost augment, floor about 25% (see `modules.md`); method untested.
- Claw gauntlets on the right arm (`modules.md`, "Claw gauntlets" and later sections): worn attachment raising punch and bash damage. Ritual claw (two blades, Angled strapped to the block), officer (flat, four batteries) and Assaultron (three blades) are installed in "PAX Test 1": they equip without crashing and the owner approves the placement (in game, 2026-11-27). Ritual In and Out are an older layout. Damage, first person, gun poses and recipe are untested; no on-hit effects yet. Laser pistol officer claw is a mockup; Shishkebab is a preview only. Cost decided: items plus research bought with a SPECIAL point; some craftable once.

## Next
On the Deck: claw crash fixed and placement approved (`modules.md`, "Claw looks, second pass"). Next in game: punch and bash damage, perk removal on unequip and exit, first person, gun poses, recipe. Then on-hit effects, the laser pistol officer claw (mockup only), housings. Test mods Addictol, its crash logger and Address Library are installed in MO2; PAX does not depend on them. Still queued: a test perk to see whether `Mod Incoming Limb Damage` slows power armor wear (not yet built).

From phone or iPad: design only. Settle the claw research cost (SPECIAL stat, one research or per claw) and whether the shield follows the same rule (question 1).

## Open questions
1. Attachment unlock: claws use up items and need research bought with a SPECIAL point. Does the shield follow the same rule, and is there an offset or drawback?
2. How many attachments should PAX have, beside the skills that cost SPECIAL?
3. Which SPECIAL stat each augment costs (proposed table in `modules.md`, unconfirmed).
4. Prerequisites: Crushing Blows, Servo Control, Fire Suppression (on hold). Rank 2 requirements and the guard stance name.
5. v1 scope.
6. Claws: which variant, damage amounts, drawback, SPECIAL stat for research, one-off ingredient items, whether bash triggers fire or shock.
7. Slower armor wear: which SPECIAL stat, how many ranks (suggested 75/50/25%), and what method?
8. Creation Kit on the Deck, or another compiler (Caprica)?
9. Needs the game or xEdit: does `WornHasKeyword` see a vanilla mod on a worn suit; shield across re-entry, save and reload; shield fit on other suits; stat trade effects on owned perks, health and reload; durability note items 2 and 4.

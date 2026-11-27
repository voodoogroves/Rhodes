# Handoff: pax
Updated: 2026-11-27, from Steam Deck (VS Code)

**Any other device (phone, iPad):** branch from `dev` and open the PR into `dev`.

Work on one area per session: read this file, [`common.md`](common.md), then that area's notes. Rewrite only that area's parts here. A final packaging session brings the areas together.

| Area | Notes |
|---|---|
| Perks, augments, SPECIAL costs | [`perks/notes.md`](perks/notes.md), [`perks/power-armor-durability.md`](perks/power-armor-durability.md) |
| Overclocks and overcharges | [`overclocks/notes.md`](overclocks/notes.md) |
| Attachments: shields, claws, blades | [`attachments/notes.md`](attachments/notes.md) |
| Secondary weapons (grenade key, jetpack slot) | [`secondary-weapons/notes.md`](secondary-weapons/notes.md) |
| Repair bot (BARB1E) | [`repair-bot/notes.md`](repair-bot/notes.md) |

Shared: [`concept-spec.md`](concept-spec.md) is the unverified starting draft. `fo4-pax` has only a README and `CLAUDE.md` (`types: [fo4-mod]`). Test plugin for all areas: `test1/build_test1.py`, installed on the Deck as MO2 mod "PAX Test 1" (it holds attachment items and two perk proofs).

## Shared
- Round 2 proofs, no scripts, all passed in game: worn stat effects, suit-only perk (free sprint), suit-only lock prompt, crafting the shield from the super mutant gauntlet.
- Test mods Addictol, its crash logger and Address Library are installed in MO2; PAX does not depend on them.
- A game exit on entering Sanctuary (2026-11-27) with no crash report was SteamOS's low-memory guard (`earlyoom` in the system journal: swap full, other apps open). Restart the Deck and close the browser before testing.
- Open: v1 scope. Creation Kit on the Deck, or another compiler (Caprica)?

## Attachments
State:
- Left arm shield: shows and "blocking looks great" on the T-60 (in game, owner). Position accepted for now. One model looks usable on all five suits (offline only). The one-gauntlet preview and dropped model (`scripts/nif/trimparts.py`) looks good in game.
- Claws on the right arm: worn attachment raising punch and bash damage. Ritual Angled, officer and Assaultron are in "PAX Test 1". Passed in game (2026-11-27): equip, placement, double punch and bash damage, perk removal on unequip and suit exit, gun poses. Recipe gate seen, crafting not tried. No on-hit effects, no first-person model. Ritual In and Out are an older layout. Laser pistol officer claw is a mockup; Shishkebab is a preview only. Cost decided: items plus research bought with a SPECIAL point; some craftable once.
- Unexplained glitch: claws stopped drawing and stacked in one slot; a game restart cleared it, not reproduced ("Claw tests, third pass").
- Under discussion: claws built into a per-suit arm model ("Clawed arm and per-suit attachments").

Next: decide on the clawed arm; if yes, spike T-60 with the Angled blades as a right arm model mod and check first person. Then crafting, on-hit effects, the laser pistol officer claw, housings. Away from the Deck: which suits get which claw, and the research cost.

Open:
1. Unlock: claws use up items and need research bought with a SPECIAL point. Does the shield follow the same rule (a shield types idea says each costs a point), and is there an offset or drawback?
2. How many attachments should PAX have, beside the skills that cost SPECIAL?
3. Claws: worn item or built into the arm, which suits get which, damage amounts, drawback, SPECIAL stat for research, one-off ingredient items, whether bash triggers fire or shock.
4. Shield types: which, their bonuses, which SPECIAL stat.
5. In game: shield across re-entry, save and reload; shield fit on other suits.

## Perks
State: design notes only, plus the shared proofs. Slower armor wear is a SPECIAL-cost augment, floor about 25%; method untested. The durability note is Gemini, partly checked; two setting or keyword names were wrong.

Next: a test perk to see whether `Mod Incoming Limb Damage` slows power armor wear (not yet built).

Open:
1. Which SPECIAL stat each augment costs (proposed table, unconfirmed).
2. Prerequisites: Crushing Blows, Servo Control, Fire Suppression (on hold). Rank 2 requirements and the guard stance name.
3. Slower armor wear: which SPECIAL stat, how many ranks (suggested 75/50/25%), and what method?
4. In game: stat trade effects on owned perks, health and reload; durability note items 2 and 4.

## Overclocks
State: design notes only, nothing tested.

Open: does `WornHasKeyword` see a vanilla mod on a worn suit (in game)?

## Secondary weapons
State: idea only; the launcher takes the jetpack's slot (owner).

## Repair bot
State: idea only (BARB1E, a repair follower).

Open: repair threshold, material costs, how it is obtained, method.

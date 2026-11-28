# Handoff: pax
Updated: 2026-11-27, from Steam Deck (VS Code)

**Any other device (phone, iPad):** branch from `dev` and open the PR into `dev`.

## Next session
Continue the **Raider** set (owner). Start at [`attachments/notes.md`](attachments/notes.md), "Raider set as it stands"; shared rules, balance and suit themes are in [`common.md`](common.md). Mockup scripts in `scripts/nif/`: `placeram.py` (both arms), `placerack.py` (shotgun rack), `placeharness.py` (scrap harness), `placeset.py` (all of it); pictures are on the Deck in `~/Downloads/PAX-claw-previews/raider/`.

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
- Test mods Addictol (keep unticked, see Attachments), its crash logger and Address Library are installed in MO2; PAX does not depend on them.
- A game exit on entering Sanctuary (2026-11-27) with no crash report was SteamOS's low-memory guard (`earlyoom` in the system journal: swap full, other apps open). Close the browser before testing; restarting the Deck is very slow (owner), so only suggest it if swap is nearly full.
- Open: v1 scope. Creation Kit on the Deck, or another compiler (Caprica)?

## Attachments
State:
- Raider set (2026-11-27): claw, brick ram, shotgun rack (offline mockups the owner likes) and a scrap harness (offline mockups the owner has been shaping). The shield goes to T-45 (owner). Arm swap spike in "PAX Test 1": not offered at the station.
- Left arm shield: shows and "blocking looks great" on the T-60 (in game, owner). Position accepted for now. One model looks usable on all five suits (offline only). The one-gauntlet preview and dropped model (`scripts/nif/trimparts.py`) looks good in game.
- Claws on the right arm: worn attachment raising punch and bash damage. Ritual Angled, officer and Assaultron are in "PAX Test 1". Passed in game (2026-11-27): equip, placement, double punch and bash damage, perk removal on unequip and suit exit, gun poses. Recipe gate seen, crafting not tried. No on-hit effects, no first-person model. Ritual In and Out are an older layout. Laser pistol officer claw is a mockup; Shishkebab is a preview only. Cost decided: items plus research bought with a SPECIAL point; some craftable once. Officer and Assaultron claw recipes noted. Ambient effects wanted. Tesla shield and arcing blades idea for T-60. Suit themes are in `common.md`.
- Unexplained glitch: claws stopped drawing and stacked in one slot; a game restart cleared it, not reproduced ("Claw tests, third pass").
- Under discussion: claws built into a per-suit arm model ("Clawed arm and per-suit attachments").

The scrap harness is delivered as crafted torso and leg pieces with the junk on them (owner; split and details in the notes). The arms are crafted pieces too (owner): minor melee damage boost plus the same durability and protection; this supersedes the upgrade-any-arm idea below. The raider items are named "Scrappy" (owner). The crafted left leg passed in game (2026-11-27): craft, welded stats 160/150/150, name, Overboss test shape, teddy bear ingredient, upgrade lining. The backup junk recipes and the new name passed in game too. Merged junk models work (`scripts/nif/writeleg.py`): the left leg with the "First St" sign and teddy bear passed in game (2026-11-27). Step 3 passed too: the left leg model is complete (chain-link cage and bolts). Next (assistant proposal): the right leg, frying pan and chained hubcap. Keep Addictol unticked: saves crashed with it on, and worked with it off. The station swap failed (2026-11-27: no arm model slot offered). The upgrade was to apply to any Raider arm with Tessa's Fist keeping its ability, never taking a misc or lining slot (owner); a new crafted arm item would drop "any arm" and is not yet agreed. Claw ingredient: Kremvh's Tooth blade mod (strip tested in game). The shotgun rack takes the jetpack slot; its firing is untested.

Open:
1. Shields follow the claw research and cost rule (decided). Is there an offset or drawback?
2. How many attachments should PAX have, beside the skills that cost SPECIAL?
3. Claws: worn item or built into the arm, which suits get which, damage amounts, drawback, SPECIAL stat for research, one-off ingredient items, whether bash triggers fire or shock, ambient effects always on or only when drawn.
6. Tesla shield: how it differs from the legendary reflect effect.
4. Shield types: which, their bonuses, which SPECIAL stat.
5. In game: shield across re-entry, save and reload; shield fit on other suits.

## Perks
State: design notes only, plus the shared proofs. Suit Lockpick: any suit. Suit Intrusion: now a T-60 / X-01 helmet module. Slower armor wear is a SPECIAL-cost augment, floor about 25%; method untested. The durability note is Gemini, partly checked; two setting or keyword names were wrong.

Next: a test perk to see whether `Mod Incoming Limb Damage` slows power armor wear (not yet built).

Open:
1. Which SPECIAL stat each augment costs (proposed table, unconfirmed).
2. Prerequisites: Crushing Blows, Servo Control, Fire Suppression (on hold). Rank 2 requirements and the guard stance name.
3. Slower armor wear: which SPECIAL stat, how many ranks (suggested 75/50/25%), and what method?
4. In game: stat trade effects on owned perks, health and reload; durability note items 2 and 4.

## Overclocks
State: design notes only, nothing tested.

Next: build the detection test.

Open: does `WornHasKeyword` see a vanilla mod on a worn suit, and can both bracer arms be counted (in game)?

## Secondary weapons
State: idea only; the launcher takes the jetpack's slot (owner), themed to X-01 with sentry and Nuka launchers. Untested: firing it as a grenade type.

## Repair bot
State: design notes only (BARB1E, a repair follower). A repair option is wanted, including out of combat through dialogue (owner, 2026-11-27); repair kit and perk ideas recorded. Obtained by find and repair (owner). Dialogue tree with a Repair slot proposed. Player voice: reuse stock lines, to be picked later. Voice: Automatron bleep sets A, B or C. Follower and eyebot mods compared offline.

Next: test whether a script can read and repair a worn power armor piece's condition.

Open: can it repair in combat, threshold, kit restock rate and cap, bot or perk does the repair, where the wreck goes and what the repair costs, whether Repair shows while not active, player voice lines, which bleep set, whether it repairs while not active, whether the plain Automatron eyebot works as the body.

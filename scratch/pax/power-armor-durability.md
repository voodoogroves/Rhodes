# Power armor durability: ways to slow it (Gemini, unvalidated)

> **Unverified, Gemini-generated.** Pasted 2026-11-26 from the owner's phone as a starting idea, not a source of truth. Gemini brainstorming has proven full of hallucinations (see `concept-spec.md`): treat every setting name, keyword, record field and engine effect below as unconfirmed until read in xEdit or the script sources, or tested in game.

Question put to Gemini: if I wanted to slow power armor durability loss, would that be a script?

Its answer, in short: no script needed. Record edits are lighter than scripts, don't bloat saves, and don't lag in combat. A script (and probably F4SE) is only needed for runtime behaviour such as an MCM slider, scaling on save load, or auto-repair on an event.

## The three approaches it gave

### 1. Game Settings (GMST): global slowdown
- Claim: GMSTs for power armor damage multipliers exist, named `fPowerArmorArmorDamageMultiplier` (player) and `fPowerArmorNPCArmorDamageMultiplier` (NPCs).
- Claim: lowering the float (example 1.0 to 0.25) cuts durability loss 75% for every suit, modded ones included, with no compatibility patches.
- Trade-off it gave: lowering the NPC value also makes enemy suits last longer.

### 2. Armor Health (ARMO / OMOD records): specific suits
- Claim: raise the Health field on each ARMO piece (helmet, torso, arms, legs), or add bonus health in the OMOD records for the upgrade ranks (Model A to F).
- Trade-off it gave: no global change, plays well with overhauls, but every piece and every custom armor mod must be edited by hand.
- Its text said "ARMA / ARMO"; ARMA is the Armor Addon record, which holds meshes, so likely a slip.

### 3. Perks and keywords: player-only or zero loss
- Claim: the vanilla keyword `PowerArmorPreventArmorDamage`, added to the player or a quest alias, disables durability loss with no script.
- Claim: a hidden perk with a Mod Incoming Armor Damage (or similar) entry point, conditioned on the wearer having the power armor keyword, gives a scaled slowdown.

## Open items

| # | Claim | State | How to check |
|---|---|---|---|
| 1 | Both `fPowerArmor...Multiplier` GMST names exist | Unchecked | Search GMSTs in xEdit |
| 2 | Keyword `PowerArmorPreventArmorDamage` exists and does what it says | Unchecked | Search KYWD in xEdit, then test in game |
| 3 | A perk entry point can scale armor damage for power armor | Unchecked | Look at perk entry points in the Creation Kit |
| 4 | Item 1 with GMSTs affects only the stated damage path, not the frame's own health | Unchecked | In game |

## Next
Read-only check in xEdit of open items 1 to 3 before anything is built. Fits the PAX concept (`concept-spec.md`); if it holds up, it becomes a module in `modules.md`.

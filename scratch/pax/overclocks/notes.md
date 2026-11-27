# Overclocks and overcharges

Later sections replace earlier ones where they say so. Shared goal and rules: [`../common.md`](../common.md).

Effect and cost columns in the tables are from the Gemini draft and **unverified**. **Keep?** and **My notes** are the owner's to edit.

## Overclocks (stack on a vanilla mod)

| Module | Needs | Effect (from draft) | Draft cost or fuel | Check notes | Keep? | My notes |
|---|---|---|---|---|---|---|
| Heavy Actuator Overdrive | Motion-Assist Servos (torso) | Strength +2 to +4, melee speed +15% | 1 perk point, gears, oil | Owner example: +1 STR per perk, capped. Swing speed unconfirmed |  |  |
| Tactical Co-Processor | Internal Database (helmet) | Awareness and Concentrated Fire | 1 perk point, circuitry, crystal |  |  |  |
| Ballistic Trajectory Predictor | VATS Matrix Overlay (helmet) | Ricochet chance, +15% VATS crit damage | 1 perk point, fiber optics, silver | No Raider version of the vanilla mod |  |  |
| Gyro-Stabilized Weapon Mounts | Optimized or Hydraulic Bracers (arms) | No scope sway, hip-fire spread -25% | 1 perk point, springs, aluminum |  |  |  |

## Movement and stance

| Module | Needs | Effect (from draft) | Draft cost or fuel | Check notes | Keep? | My notes |
|---|---|---|---|---|---|---|
| Assaultron Optical Overclock | Stealth Boy (torso) | Invisible while sprinting | AP drains at 2x | Likely needs script. No Raider version |  |  |
| Ballistic Deflector Guard | Hydraulic Bracers | -40% damage while blocking, shield plates | 5 AP per heavy hit | Plate visuals may not render; AP cost likely script |  |  |
| Mr. Handy Thrusters | Explosive Vent (legs) | Forward dash that staggers | 25 AP, 8 s cooldown | Likely script; dash unconfirmed |  |  |
| Ground-Anchor Clamps | Calibrated Shocks (legs) | Standing still: -30% damage taken, +25% melee | None | No cost: breaks the cost rule |  |  |
| Ramming Speed | Overdrive Servos (legs) | Sprint knockdown, +20% sprint speed | 2x core drain while sprinting | Knockdown and drain unconfirmed |  |  |

## Automatic failsafes

| Module | Needs | Effect (from draft) | Draft cost or fuel | Check notes | Keep? | My notes |
|---|---|---|---|---|---|---|
| Triage Nanite Emitter | Medic Pump (torso) | Heals companions after combat | 1 stimpak or antiseptic per pulse | Needs script |  |  |
| Overdrive Capacitor Surge | Core Assembly (torso) | Below 15% AP: knockback, +100 AP | 1 nuclear material, 45 s | Needs script |  |  |
| Shrapnel Counter-Detonation | Reactive Plates (torso) | Blast when hit in melee | 2 steel or 1 frag grenade, 12 s | Needs script for the cost |  |  |
| Cryo-Coolant Dump | None | Below 20% health: freezing nova | Cryo cell or coolant, 60 s | Needs script for the cost |  |  |

## Sensor toggles (holotape)

| Module | Needs | Effect (from draft) | Draft cost or fuel | Check notes | Keep? | My notes |
|---|---|---|---|---|---|---|
| Low-Light Optics | Targeting HUD (helmet) | Night vision toggle | Not stated | Toggle likely script |  |  |
| Deep-Scan Penetrator | Sensor Array (helmet) | VATS through cover, tag enemies | Not stated |  |  |  |

## Actuator Overclock (owner, 2026-11-25; working name)

**LOCKED:** raw Strength is the only gate, no level requirements (owner: plenty of mods already add Strength on top of the suit's 11).

Trained; needs Motion-Assist Servos installed (torso, keyword `dn_HasMisc_Str`; detection untested). One perk point per rank; +1 Strength per rank, in power armor only.

| Rank | Requires base (raw) Strength | Total bonus |
|---|---|---|
| 1 | 1 | +1 |
| 2 | 4 | +2 |
| 3 | 7 | +3 |
| 4 | 11 | +4 |

- `EnchPA_Abilities`: `PowerArmorStrengthEffect` adds 10..1 conditioned on `GetBaseValue(Strength)` = 1..10, so every suit wearer lands on 11 before other bonuses. Base 11 matches none and needs none.
- To check: base 11 is reachable (bobblehead raising base value): `player.getbaseav strength`.

- Owner, 2026-11-25: no Intelligence overclock (Strength is the one that makes sense: a character at 11 or 12 loses Strength entering the suit). Review the non-stat overclock ideas instead.

## Roll with the Punches: now an overclock (owner, 2026-11-25; replaces its earlier trained design where they differ)

- Needs Hydraulic Bracers installed (arms, keyword `dn_HasMisc_Unarmed`; detection untested). Up to 2 perk points; less damage when blocking.
- Owner: Hydraulic Bracers on **both arms** required; Moving Target dropped (it is a suit overclock). Ranks: +15 / +30 block, 1 perk point each, no other perk requirement.
- Detection must confirm both arms; checking for one keyword may not distinguish two pieces (untested).

## Open questions

- Whether `WornHasKeyword` detects a vanilla mod on a worn suit (in game).

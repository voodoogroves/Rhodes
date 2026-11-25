# PAX modules (working table)

Edit freely: **Keep?** (yes / no / maybe) and **My notes**, or change any cell. Everything in the effect and cost columns is from the Gemini draft and **unverified**. The draft itself is in `concept-spec.md`.

## Rules so far (owner, 2026-11-25)

- Every upgrade has a cost or a drawback.
- Perk upgrades must spend a real perk point (firm). Without that it is free power with a small build barrier.
- Upgrades **stack** on top of vanilla mods.
- Do not change existing records, so other power armor mods don't conflict.
- Example: a perk that overclocks Motion-Assist Servos, +1 Strength per perk spent up to a maximum, only in power armor.

## Always-on frame firmware (any power armor)

| Module | Needs | Effect (from draft) | Draft cost or fuel | Check notes | Keep? | My notes |
|---|---|---|---|---|---|---|
| Locksmith sub-routine | In PA | Pick all lock levels | 1 perk point, circuitry, bobby pins |  |  |  |
| Intrusion sub-routine | In PA | Hack all terminal levels | 1 perk point, circuitry, fiber optics |  |  |  |
| Ablative Plate Reinforcement | In PA | Armor wear -25/50/75% (3 ranks) | 1 perk point per rank, steel, aluminum | Wear effect unconfirmed |  |  |
| Closed-Loop Rad Scrubbers | In PA | +150 rad resist, slow rad purge out of combat | 1 perk point, nuclear material, rubber | Overlaps vanilla Rad Scrubbers |  |  |
| Servo-Assisted Load Bearing | In PA | Carry +50/+100, walk normally when over-encumbered | 1 perk point, gears, springs |  |  |  |

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

## Shoulder weapons (hotkey)

| Module | Needs | Effect (from draft) | Draft cost or fuel | Check notes | Keep? | My notes |
|---|---|---|---|---|---|---|
| Sentry Cluster Mortar | Shoulder mount | Micro-missile salvo | 2 missiles or 5mm rounds, 15 s | All four: script, F4SE for the hotkey, new meshes that may not render |  |  |
| Assaultron Focus Beam | Shoulder mount | Sustained laser | 3 fusion cells, 20 s | As above |  |  |
| Voltaic Arc Discharge | Tesla Coils (torso) | Chain lightning, up to 4 targets | 2 fusion cells, 20 s | As above, mesh not stated |  |  |
| Corrosive Acid Sprayer | Shoulder mount | Armor-stripping cone | 1 acid, 12 s | As above |  |  |

## Sensor toggles (holotape)

| Module | Needs | Effect (from draft) | Draft cost or fuel | Check notes | Keep? | My notes |
|---|---|---|---|---|---|---|
| Low-Light Optics | Targeting HUD (helmet) | Night vision toggle | Not stated | Toggle likely script |  |  |
| Deep-Scan Penetrator | Sensor Array (helmet) | VATS through cover, tag enemies | Not stated |  |  |  |

## Companions

| Module | Needs | Effect (from draft) | Draft cost or fuel | Check notes | Keep? | My notes |
|---|---|---|---|---|---|---|
| Squad Ballistic Sync | Perk | Companions in PA: no armor wear, infinite ammo | Not stated | Unconfirmed; no drawback |  |  |
| Point-Defense Tesla | Companion mod on a misc slot | Not stated | Not stated | Takes the misc slot, so it would not stack |  |  |
| Self-Sealing Plating | Companion mod on a misc slot | Not stated | Not stated | As above |  |  |
| Auto-Stim Triage Core | Companion mod on a misc slot | Not stated | Not stated | As above |  |  |

## Locksmith and Hacker (owner: yes, 2026-11-25)

Vanilla, read from `Fallout4.esm`:

| Rank | Locksmith (PER 4) | Level | Hacker (INT 4) | Level |
|---|---|---|---|---|
| 1 | Advanced locks | - | Advanced terminals | - |
| 2 | Expert locks | 7 | Expert terminals | 9 |
| 3 | Master locks | 18 | Master terminals | 21 |
| 4 | Pins never break | 41 | No lockout | 33 |

- Proposed, not yet confirmed: no SPECIAL requirement, same levels, one point per rank, ranks 1-3 first.
- Unlocks are perk entry points `Set Player Gate Lockpick` / `Set Player Gate Hacking` (values 1-3). To test: an in-power-armor condition works on them, and our lower rank never overrides a higher vanilla rank.

## Spending a perk point (research 2026-11-25, not settled)

- `Game.AddPerkPoints(int)` is in the installed sources. Seen there: no function that reads unspent points. Negative values: undocumented in what was found.
- The perk chart is `interface/levelupmenu.swf`. No source found for adding a perk to it without replacing that file. LevelUpMenuEx (F4SE) replaces the menu to allow new perks.
- The Creation Kit wiki refused automated reads (403); ask the owner to paste pages if needed.
- Offline CK wiki (Alexandria `reference/fo4-ck-wiki/`, 2021 snapshot): a **Playable** perk "can be chosen by the player when leveling up", and has **Level-Up Menu Conditions**. It does not say a new perk appears in the vanilla chart. `AddPerkPoints` documents only adding (clamped at 255). No point-reading function found in the pages searched. Perk entries have **Priority** and **Conditions**.
- Test 1: does a new playable perk appear in the vanilla chart? (no script)
- Test 2: `cgf "Game.AddPerkPoints" -1` with points and with none (console).

## Open questions

- Spending a real perk point: how does a new perk get offered? Adding to the vanilla perk chart may not be possible without changing the interface; a holotape or terminal would need script.
- Whether `WornHasKeyword` detects a vanilla mod on a worn suit (in game).

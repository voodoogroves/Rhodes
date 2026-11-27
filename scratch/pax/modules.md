# PAX modules (working table)

Edit freely: **Keep?** (yes / no / maybe) and **My notes**, or change any cell. Everything in the effect and cost columns is from the Gemini draft and **unverified**. The draft itself is in `concept-spec.md`.

## Goal (owner, 2026-11-25)

A framework that lets someone who plays in power armor keep investing in it and turn it into a walking tank. Not tuned to one character.

So far: Locksmith and Hacker yes; carry weight is a low priority (other equipment mods cover it); Action Boy/Girl style perk of interest.

## Vision and framework (owner, 2026-11-25)

- Mostly expertise and engineering capabilities that let a player who leans into power armor turn it into a Swiss Army knife.
- A few are add-ons; be careful with those, as they may conflict with other mods.
- **Built** augments cost a perk point and materials (locks). **Trained** augments cost a perk point only.

## Categories (owner, 2026-11-25)

1. Perk replacers: skip the SPECIAL requirement, power armor only. **Working on now.**
2. New suit-only abilities bought with a perk point (e.g. Stagger Dampeners). **Working on now.**
3. Overclocks: make existing pieces stronger.
4. Grenade replacers: mounted system fired with the grenade key (parked).
5. Condition triggers: passive, fire on low health and similar.

Draft sensor toggles and companion support are not in these.

## Category 1 rules (owner, 2026-11-25)

- The SPECIAL requirement is replaced by one or two **perk** requirements. Examples floated, not final: Armorer + Robotics Expert for Locksmith; Science! + Robotics Expert for Hacker.
- No stacking with the vanilla twin: the higher rank applies, they never add.
- Power armor only; each rank costs a real perk point.
- Proposed, not confirmed: keep the vanilla level gates.
- Check each pairing: a prerequisite needing the same SPECIAL at an equal or higher value defeats the bypass (Science! INT 6 and Robotics Expert INT 8, against Hacker INT 4).

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

## Current focus (owner, 2026-11-25): perks that bypass a SPECIAL requirement, usable in power armor

Overclocks and the rest come next.

| Perk | SPECIAL | Rank levels | Built as (read from `Fallout4.esm`) | Suggestion | Keep? | My notes |
|---|---|---|---|---|---|---|
| Pain Train | STR 10 | 1, 24, 50 | ability | core |  |  |
| Rooted | STR 9 | 1, 22, 43 | ability + entry | core |  |  |
| Adamantium Skeleton | END 7 | 1, 13, 26 | entry | core | yes |  |
| Action Boy/Girl | AGI 5 | 1, 18 | ability | core | yes |  |
| Nuclear Physicist | INT 9 | 1, 14, 26 | ability + entry | core |  |  |
| Moving Target | AGI 6 | 1, 24, 44 | ability | good |  |  |
| Steady Aim | STR 7 | 1, 28 | entry | good |  |  |
| Heavy Gunner | STR 5 | 1, 11, 21, 35, 47 | entry | good |  |  |
| Locksmith | PER 4 | 1, 7, 18, 41 | entry | good | yes |  |
| Hacker | INT 4 | 1, 9, 21, 33 | entry | good | yes |  |
| Refractor | PER 7 | 1, 11, 21, 35, 42 | ability | maybe |  |  |
| Demolition Expert | PER 5 | 1, 10, 22, 34 | entry | maybe |  |  |

Level 1 means no level requirement. Armorer, Science! and Gun Nut are left out: crafting recipes check those exact perks, so a copy would likely not unlock them.

Cheat Terminal (installed third-party mod, script strings read 2026-11-25): grants and removes perks with `AddPerk` / `RemovePerk` from terminal fragments; its perk point menu only adds (`AddPerkPoints`). No point removal or point reading seen.

## Limb damage and stagger (read from `Fallout4.esm`, 2026-11-25)

- `PowerArmorPerk` `0001F8A9` entry points: incoming weapon damage, armor weight, drawn weapon weight, falling damage. No limb damage or stagger entry in it.
- `EnchPA_Abilities` includes `AbNoExplosionKnockdown` and `AbReduceConditionRate` (effects not examined).
- No power armor mod description mentions limb damage, stagger, knockdown or disarm.
- Ordinary armor: Pneumatic (perk `mod_armor_LessStagger`, incoming stagger entry), Strengthened (`ReduceLimbDamageMod`; amount not read), Cushioned (falling).
- Adamantium Skeleton incoming limb damage multipliers: 0.7, 0.4, 0.0.

## Locks and terminals: roadmap (2026-11-25)

Owner, 2026-11-25: modules first.

| Stage | Feature | Script |
|---|---|---|
| v1 | Installing the module adds a prompt on locked targets; a robot-style roll decides. Scaled by INT (intrusion) and STR (lockpick) | Required |
| v2 | Visuals on use: the robots' blue scan for hacking, a punch animation for lockpick | Required |
| Later | Literally punching the lock (`RegisterForHitEvent` per target; unproven on doors and containers) | Required |

- The earlier no-script idea (module raises `Set Player Gate Lockpick` / `Hacking` through a hidden perk) is not the v1 plan.
- Needs the Papyrus toolchain first, proved with a trivial script.
- Robot effects seen in the script: visual `DLC01EyebotInteractVFX`, sound `DLC01QSTMSATDoorActivate` (Automatron).
- Proposed odds, unconfirmed: roll 0 to `60 + 5 x base stat + 20 x (mark - 1)`; success if above lock level.
- Owner, 2026-11-25: fusion core drain as the cost; a single try is fine; asked about a cooldown for retrying. (Owner: a robot companion can keep retrying, it just takes time.)
- Cooldown: possible by script; per lock (store the time in our own actor value on the target) or suit-wide.
- Core drain: no direct drain function found yet. `PABatteryDamageRate` `0015A8B2` exists (drain rate); untested.
- Owner idea: spend AP, which in power armor drains the core. `Fallout4.esm` has `fPowerArmorPowerDrainPerActionPoint` = 0.05 (also running 0.05 per second; jump, melee, landing 0). Untested whether AP removed by script or console drains the core. Test: in power armor, `player.damageav actionpoints 100`, watch the core.
- Owner, 2026-11-25: cost scales with lock tier. Proposed, unconfirmed: 25 / 40 / 55 / 70 AP for Novice / Advanced / Expert / Master.
- Max AP from game settings: `60 + 10 x Agility` (`fAVDActionPointsBase`, `fAVDActionPointsMult`): 70 at AGI 1, 160 at AGI 10, before perks and gear.
- Open: module slot (a piece has one misc slot), cooldown scope and length, perk requirements. Never key, barred, chained or terminal-only locks.

### Automatron robot unlock roll (script disassembled, `DLC01CompanionUnlockScript`)

- Module sets an actor value on the robot (1 = can): `DLC01_Ability_Lockpicking`, `DLC01_Ability_Hacking`. A flag only; it does not change the odds.
- Target must be a locked container or door (lockpick) or terminal (hacking).
- Success: `Utility.RandomInt(0, 110) > GetLockLevel()`, then `Unlock`. No perk or level in the roll.
- Per attempt: Novice (25) 77%, Advanced (50) 54%, Expert (75) 32%, Master (100) 9%. Levels 251-255 (barred, chained, terminal only, inaccessible, key) never succeed.
- Failure plays a sound and counts the attempt; a failed flag can be set on the target. The attempt limit was not read.
- Adapting it: raising the top of the roll scales the odds; keep it under 251.

## Lock modules: unlock and category (2026-11-25)

- Owner: with no overlap with vanilla perks, these are not perk replacers; category 1 entries become perk-adjacent passive capabilities.
- Owner: unlock our modules when the robot versions become craftable. AP costs by tier "feel right".
- Robot recipes `co_DLC01Bot_Torso_Misc_Lockpick` `0100137F` / `..._Hack` `01001381`: only condition is `ModdedItemHasKeyword(DLC01WorkbenchNoHackOrLockpickKeyword) != 1` (keyword added by `DLC01Bot_Keywords_AV_Codsworth`). No perk or global.
- Robot workbench recipe `DLC01workshop_co_CraftingRobot` `010036CE`: `GetStageDone(DLC01MQ01, 3000) == 1`. Using the same condition gives the same unlock point, no script; needs `DLCRobot.esm` as master; hiding untested.

## Augments bought in a terminal or holotape (owner, 2026-11-25)

- A perk point means: in the terminal or holotape, choose to augment the power armor (e.g. to hack); it costs one point, one not put into Hacker. Using it then costs AP and so on.
- Needs: grant (`AddPerk`, seen in Cheat Terminal), spend (`AddPerkPoints(-1)`, untested), read the balance (no Papyrus function found).
- Leads: `pipboy_statspage.swf` contains `PerkPoints`; `levelupmenu.swf` contains `uiPerkCount`; the game has a `PerkPointIncreaseEvent`. Whether F4SE `UI` functions can read the value is untested.

### Chosen: augment only (owner, 2026-11-25)

- A perk augment bought on the holotape; no module or misc slot. Use costs AP by lock tier.
- Prerequisite: the robot module is unlocked (`GetStageDone(DLC01MQ01, 3000)`).
- Holotape option "build and develop this capability" charges a build cost **in addition to** the perk point.
- Supersedes the module-based v1 and its module marks: how odds and tiers upgrade is open (e.g. ranks bought on the holotape).

## Lock augments: current design (2026-11-25, replaces earlier lock sections where they differ)

**LOCKED by owner, 2026-11-25** (Suit Lockpick and Suit Intrusion: augments 1 and 2), including the materials and AP costs shown as proposed below. Mechanics are still untested.

| | Suit Lockpick | Suit Intrusion |
|---|---|---|
| Prerequisites | Automatron robot modules unlocked (`GetStageDone(DLC01MQ01, 3000)`), Robotics Expert 2, Armorer 2 | Same |
| Cost | 1 perk point + materials, once, on the holotape | Same |
| Materials (proposed, unconfirmed) | Screwdriver `0004D1F4` x1, Bobby Pin `0000000A` x10 | Military-Grade Circuit Board `00154AD2` x1, Sensor Module `001ACC8E` x1 |
| Use | Prompt on a locked target, power armor only; AP 25 / 40 / 55 / 70 by tier (proposed); drains core if scripted AP use counts | Same |
| Odds | Roll 0 to `60 + 5 x current STR`, success above lock level | Same with **current** INT |

- Owner decided: single purchase, no ranks or modules; both need Robotics Expert 2 and Armorer 2.
- Robotics Expert 2: INT 8, level 19 (`00065E64`). Armorer 2: STR 3, level 13 (`0004B255`).
- Owner, 2026-11-25: scale on **current** stats for both (gear, chems, magazines and the suit count).
- Power armor raises current STR (`EnchPA_Abilities` has Strength effects; resulting value in the suit believed 11, unverified), so Lockpick odds will vary little by character. Check in game.
- The perk prerequisites still check base stats. No cap on the formula; refuse lock levels 251 and up regardless.
- v2: robot blue scan on hacking, punch animation on lockpick.
- Owner, 2026-11-25: "intrusion, in v2 this switches to trained - we have learned to use our strength to brute-force open locked items". Confirmed: the owner meant **Suit Lockpick**, not Intrusion. In v2 it is trained: perk point only, no materials; v1 stays built.
- **LOCKED, v2 Suit Lockpick (owner, 2026-11-25):** Iron Fist 3 (level 18) + Armorer 2; 1 perk point, no materials; punch prompt, AP by lock tier, odds from current STR. Robotics Expert 2 and the robot unlock condition dropped.
- Robot module recipes require no perks (all installed plugins searched for those two recipes).

## Augment 3: Stagger Compensation (owner, 2026-11-25, in design)

"Through your training and familiarity you have learned how to absorb and reduce the impact of incoming staggers." Trained augment: perk point only.

| Rank | Effect | Requires (Adamantium Skeleton for all ranks, owner) | Cost |
|---|---|---|---|
| 1 | Incoming stagger one step down | Adamantium Skeleton 1 (END 7) | 1 point |
| 2 | Two steps down | Rank 1, Adamantium Skeleton 2 (level 13) | 1 point |

Confirm: matching skeleton rank per rank (as shown), and whether Armorer 2 also applies.

- Vanilla `mod_armor_LessStagger` `00245AFE` (Pneumatic): entry `Mod Incoming Stagger`, function **Add Value -1**. Reduction is in steps, not a percentage.
- Explosion records offer stagger sizes (Small, Medium, Large seen in the wiki text). Whether a multiply works on this entry is unknown.

## Idea source: non-power-armor mods (owner, 2026-11-25)

- Rule: skip anything an existing power armor mod already does (so Sprint Efficiency is out); borrow ideas from ordinary armor mods and the like.
- Owner: **no duplicating legendary effects**; perks or mundane armor effects only.
- Mundane armor candidates with no base game power armor counterpart seen: Weighted (melee/unarmed ignore armor), Braced (less melee damage blocking), Stabilized (steadier scope), BioCommMesh (chems +50% duration), Strengthened (limb damage), Muffled / Sleek (stealth).
- DLC, Creation Club and third-party mods not checked.

## Augments in design: Crushing Blows and Guard Stance (owner likes both, 2026-11-25)

Values read from `Fallout4.esm` (Combat armor arm linings; other families share the enchantments):

- **Weighted** (`..._IgnoreArmor`): `Mod_IgnoreArmor_AV` +10 per arm piece. Perk `mod_armor_IgnoreArmorPerk` (`Mod Target Damage Resistance`, multiply 1 + AV x -0.01, conditioned on weapon type): 10% armor ignored per arm, 20% with both if the value adds.
- **Braced** (`..._BetterBlocking`): `ArmorBlockPercent` +15 per arm piece; its enchantment also lists magnitude 25 on the same value. How they combine is not established.

- **Stabilized** (`mod_armor_Combat_Lining_LimbArm_Stabilized`): `Mod_Stabilized_AV` +2 per arm; perk `mod_armor_StabilizedPerk` (`Mod Actor Scope Stability`, multiply 1 + AV x 0.01): 2% per arm by that formula.

Owner rules (2026-11-25): braced, weighted and stabilized are the three under design. **One rank (one perk point) is worth about one arm's mod**, not both. Guard stance name: boxing term wanted ("Absorb Blows" floated).

| Augment | Rank 1 | Rank 2 (proposed) |
|---|---|---|
| Crushing Blows | 10% armor ignored | 20% |
| Guard stance (name open) | +15 block | +30 |
| Servo Control (working name) | 2% scope stability | 4% |

- Owner, 2026-11-25: Servo Control stays **faithful** to Stabilized: 2% / 4%.
Owner, 2026-11-25, prerequisites: Roll with the Punches: Moving Target 1; Crushing Blows: Basher; Servo Control: Science! or another tech perk. Rank 2: Roll with the Punches needs Moving Target 2 (owner confirmed, level 24); Crushing Blows (Basher 2) and Servo Control (Science! 2) still to confirm.
Owner, 2026-11-25: Servo Control (was Gyro Stabilizer) is **trained**. Crushing Blows and Roll with the Punches should be tied to perks other than Iron Fist, Big Leagues or Basher; owner is looking. Servo Control prerequisites open.

## Fire Suppression Protocols (owner chose, 2026-11-25; costs a perk point; prerequisite open)

- **ON HOLD (owner, 2026-11-25):** method known, ranks and prerequisite open. First set judged good; moving to the next set.

- Owner: **trained**. Focus new work on trained augments, since they move with the person into any suit. No power armor function prevents being set on fire (owner), so this fills a gap.
- Trained: perk point only.
- **Method found (records read 2026-11-25, untested):** vanilla immunity perks do this with no script. `ImmuneToAcid` / `ImmuneToPoison`: `Mod Incoming Spell Magnitude` set 0 on a damage-type effect keyword, plus `Mod Incoming Weapon Damage` set 0. `VRWorkshopShared_ImmuneToDamagePerk` lists fire spells by ID (`FireHazard`, `FlameThrowerFireHazardSpell`, `ExplosionFireHazardSpell`, `FXEnchFireHit`, `FXEnchFireHitMolotov`, `FlamerFXEnchFireHit`, `EnchWeapMod_JunkJetFire`, `enchMod_LaserReceiver_Fire1/2`) and sets 0. `PowerArmorRadResistPerk` uses the same entry in the suit. `Mod Incoming Spell Duration` also exists.
- Fire effects with keyword `DamageTypeFire` (`dtFireEnchFlameChance*`) can be matched by keyword; others (incendiary, flame visuals, some hazards) need listing by ID. DLC and Creation Club fire effects not scanned.

- Asbestos lining (`mod_armor_RailroadSWAT_Lining_Torso_FlameResistance` checked): +15 on a resistance value and keyword `dn_HasLining_FlameResistance`.
- In `Fallout4.esm` the only condition found on that keyword is in `FXFireHitVisuals` (condition function 682, keyword != 1). So "immune to being set on fire" may be mostly the burning visual; whether burn damage is affected is not established.
- It checks a **worn** keyword, which a perk does not supply. Needs another method: find one before designing.

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

## Perk point test result (2026-11-25)

- Owner tested in game: adding **-1** perk points does not work.
- Cheat Terminal as installed (author gir489, 1442 scripts checked): six `AddPerkPoints` calls (+1, 5, 10, 20, 50, 100), none negative, no read of a balance; no perk point actor value found in `Fallout4.esm` or the plugin. A Gemini claim that it reads and subtracts points is false for this version.
- So a holotape cannot charge a point by script that way. Next: test whether a new playable perk appears in the level-up chart (game handles spending).

## Perk chart and other mods (2026-11-25)

- Owner does not like paying with a SPECIAL point.
- *Traits and More Perks* (Cirosan, Beta 4, read from the download): craft an injector, use it, script runs `AddPerk`; traits via holotape; no perk point calls seen. Its readme says the standard perk chart "precludes adding new perks". The perk record checked is not Playable.
- Vanilla `levelupmenu.swf` holds per-perk art classes named `PerkClip<formid>` and a grid view; a new perk has no clip there. How the grid is filled (game or menu) is not established.
- Adding a section means shipping a changed `levelupmenu.swf` (derived from a game file: never commit it) and likely clashes with other menu mods. LevelUpMenuEx (F4SE) is an existing replacement chart.

## LevelUpMenuEx (PRKF) read from the download, 2026-11-25 (not installed or tested)

- Files: `F4SE/Plugins/PRKF.dll`, `Interface/LevelUpMenu.swf` (replaces the vanilla chart), `Scripts/PRKF/PRKF.pex` + source, MCM config, `Data/PRKF/*.ini`.
- The DLL contains runtime `1.11.240`, matching the installed game and F4SE 0.7.9. Download name also says 1.11.240.
- Papyrus: `PRKF:PRKF.GetPP()` returns perk points; `AddPP(int)` returns the result. Negative values untested. Also trait menu and tag skill functions.
- Ini `[Main]`: `PerksList` (a form list of perks), `disableVanillaPerks`, `PPPerLevel`. Value format not confirmed. Menu text includes a "Non SPECIAL" group.
- Gives two routes: perks listed in the replacement chart (game-handled spend, likely no script), or a holotape that reads and spends points.

- **Owner, 2026-11-25: no F4SE.** Rules out LevelUpMenuEx as a dependency, the `UI.Invoke` / `SelectPerk` and `UI.Get` ideas, and `RegisterForControl`.
- Owner asked whether a SPECIAL point taken as payment can be added back later (script can restore it; design open).

## Perk cost mechanism (owner, 2026-11-25; replaces the perk point spend ideas above)

- Taking a perk-cost augment lowers a **named** base SPECIAL by 1 per rank (story: time and study), then grants it. The player rebuys the stat with a perk point, immediately or later. No F4SE; needs a script. **Tested in game by the owner, 2026-11-25:** Endurance 4 lowered to 3 with `player.setav`, bought back in the chart, then raised to 10 (7 points). Still unchecked: owned perks, health, save and reload.
- Floor: cannot pay with a stat at 1. Requirements are checked before paying.
- Base Strength lost costs little in the suit (raised to 11), so avoid it as a price.

Proposed stats, unconfirmed:

| Augment | Stat per rank |
|---|---|
| Suit Intrusion | Endurance |
| Suit Lockpick (v1, v2) | Perception |
| Stagger Compensation | Agility |
| Crushing Blows | Perception |
| Roll with the Punches | Agility |
| Servo Control | Charisma |
| Actuator Overclock (ranks 1-4) | Endurance, Agility, Charisma, Luck |
| Fire Suppression (on hold) | Luck |

## Next session (owner request, 2026-11-25)

- Owner wants to be told how to install the Creation Kit (seen on Steam) on the Deck alongside Mod Organizer 2, or whether to use a different compiler.
- Facts so far: Steam app `1946160`; reports of running it under Proton were mixed and mostly old; Caprica is an alternative compiler that still needs the vanilla base script sources. The loose sources in the game folder looked like F4SE's set only. Back up `Data/Scripts` before installing.
- Then: compile a trivial script, test a stat change from script, detection test for overclocks, Stagger Compensation end to end.
- Still unchecked from the stat test: owned perks, health, save and reload, behaviour at 11.

## Arm shield (idea, 2026-11-26; owner would like it with a big blocking shield, on the power armor left arm)

### Model
- `SupermutantArmor0_Arms` `001B3A01` (playable `00248FD3`), `Actors\Supermutant\CharacterAssets\SMArmor0_Arms.nif`; base game. The wanted part is the big plate from the mutant's right arm.
- Both arms are one skinned shape (super mutant arm, hand and finger bones); material `Materials\actors\Supermutant\SupermutantArmor1.BGSM`. Ground model `SMArmor0_ArmsGO.nif` is unskinned; geometry not examined.
- Work: read geometry, isolate the plate, make rigid, move to left forearm (rotate or mirror), fit, render previews. Commit the script only, never the model. No meshing tool is set up (a reader and previewer exists, below).
- Creation Club candidates by name, not chosen: `ballisticshield.nif`, `heavyincineratorshield.nif`.

### Fitting every set
- Intended: one shield following the left forearm bone, offset measured per arm model (about five base game shapes; DLC, Creation Club and mod armor each need a look). Untested.

### Slots and race (records read, nothing tested in game)
- `PowerArmorRace` `0001D31E` has its own skeleton (`actors\PowerArmor\CharacterAssets\skeleton.nif`).
- T-60 left arm: `AA_Power_Arm_Left`, body slot 42, primary race Human with `PowerArmorRace` additional, model `ArmorPALeftArm.nif`; visible arm from OMOD `PA_T60_LArm` (`PA_T60_LArm.nif`). Frame: slots 33, 34, 35, 60.
- Preferred, no vanilla edits: our own wearable in a free body slot, same race pattern. Free slots checked 2026-11-26 (below).
- Fallback: own attach point `ap_PAX_Shield`. Child slots (misc, lining, paint) come from each set's base arm mod (`PA_T45_ArmLeft`, `PA_T51_LArm`, `PA_X01_LArm`, `PA_Raider_LArm`, `PA_T60_LArm`), so those need overriding, preferably by an xEdit patch script over the winning records, as an optional plugin. Owner has not decided.

### Left arm connect points (read from the base game models, 2026-11-26)
| Model (`actors\PowerArmor\CharacterAssets\Mods\`) | Parent points on root | Position |
|---|---|---|
| `PA_Raider_LArm.nif`, `PA_T45_LArm.nif`, `PA_X1_LArm.nif` | `p-Misc`, `p-Paint`, `p-Lining` | (-14.11, -7.33, 123.44) |
| `PA_T51_LArm.nif` | same three | (-14.11, -7.33, 122.94) |
| `PA_T60_LArm.nif` | same three | (-14.07, -7.33, 123.44) |

- Each of the five attaches with child point `C-LArmMod` to `P-LArmMod` on the base `ArmorPALeftArm.nif`. All have the bones `LArm_ForeArm1`, `LArm_ForeArm_Armor`, `LArm_UpperArm`, `LArm_UpperArm_Armor`, `L_Pauldron`.
- No shield or forearm accessory point on any of them; none read on the power armor skeleton either. No vanilla arm misc mod has a model. Headlamps are an example of a rigid add-on model on its own point (`c-Headlamp`).
- Route A (looks best, untested): skin the shield fully to `LArm_ForeArm1` and let it use an existing point. No vanilla model edits; one shield may suit all sets. Unproven: that a shared point accepts an extra part; fit against each arm's bulk.
- Route B: rigid shield on a new PAX point, edited into each set's arm model. More work and mod conflicts.

### Preview reader (2026-11-26)
- `scripts/nif/nifpreview.py` (`info`, `render`): lists loose parts, bones and connect points; draws six flat-shaded views. Previews stay outside every repo.
- `SMArmor0_Arms.nif` splits into two parts: the right arm (456 triangles, mostly `RArm_ForeArm3_skin`) and the left (292). The big right-hand piece is plate and glove joined by position; splitting at texture seams separates them cleanly. Bare shield: `render --seams --parts 1,5,6` (289 triangles). Its inner face looks open in the middle, where the glove covered it.
- The T-60 left arm's forearm shell is weighted to `LArm_ForeArm1` and `LArm_ForeArm_Armor`. Its stored coordinates differ from the super mutant's, so placing the plate takes the bone transforms (`placeshield.py`, below).
- Full-size fit on T-60, standing pose (`scripts/nif/placeshield.py`, 2026-11-26): the plate is mirrored and carried from the super mutant's left forearm bone to the power armor's (bone lengths 29.8 and 27.0), keeping its offset. It sits on the outer forearm and clears torso and leg. The arm shell pokes through the middle, so it needs to move outward. Its upper end passes the elbow, close under the pauldron; bent elbow and aiming poses are not checked.
- Adjusted (`--slide 6 --out auto`, push 7.8): no sampled point of the arm's forearm shell pokes through; the plate runs from 2.4 above the elbow to 43.4 toward the fingers (hand joint 27.0). A straight push leaves the plate standing off the arm; owner: pushed out too far.
- Closer fit (`--slide 6 --tilt -16 --roll 5 --out auto`, push 2.6): nothing sampled shows through the outer face; the arm sits partly inside the plate's thickness. Runs 2.4 above the elbow to 41.8. Owner: sinking into the arm is fine as long as nothing protrudes through the shield.
- Bent elbow (`--bend`, elbow only, shoulder still): at roll 5 the shield's top cuts into the upper arm and shoulder pad (15 of 289 plate triangles at 45 degrees, 42 at 90, 80 at 120). Sliding and scaling barely help; swinging round the arm does. `--slide 6 --tilt -16 --roll -40` (push 3.2): none cut in at 0 or 90, about 7 at 120. It turns the face toward the back when the arm hangs. `--roll -30` (push 2.3): clean at 90, about 24 at 120. Owner: hanging too low, too near the hand.
- Moved toward the elbow (`--slide 0 --tilt -12 --roll -40`, push 5.0): runs 8.5 above the elbow to 36.4; none cut in at 0 or 90, about 9 at 120. Halfway option `--slide 3 --tilt -16 --roll -40` (push 4.3, 8 at 120). The arm is thicker near the elbow, so moving up needs more push.
- Owner: height looks ok. More elbow-end tilt at the same push (5.0, slide 0, roll -40): at -12 nothing sampled shows through the front hanging or at 90, the arm only sinks into the back (at 120 the upper arm shows through by up to 1.1); at -16 the forearm comes through by up to 1.2, at -20 by 2.8, at -24 by 5.6.
- **Chosen (owner, 2026-11-26):** T-60 placement `--slide 0 --tilt -12 --roll -40 --out 5.0` at full size, "close enough". Checked by sampled points with the elbow only bent; other sets, animations and in-game fit are open. Run: `python3 -I scripts/nif/placeshield.py <meshes> <outdir> --slide 0 --tilt -12 --roll -40 --out 5.0`.

### Held tests (in game)
- `player.getisrace PowerArmorRace` inside and outside the suit (expected 1 and 0).
- Can an extra item be worn and seen in power armor, and does it stay through exit and re-entry?

### Test 1: separate wearable (built 2026-11-26, not yet run)
- Slots (plugins found in Data and the MO2 mods folder): power armor pieces use 30-39, 41-50, 52 and 60. No armor of any race uses 53, 56 or 57; the test uses 56 and 57.
- `scratch/pax/test1/build_test1.py` writes `PAXTest1.esp` in `~/Downloads/PAX-Test1.zip`: "PAX Test A (mutant arms)" in slot 56, "PAX Test B (X-01 left arm)" in slot 57; race Human plus `PowerArmorRace`.
- Steps: install with MO2 (Test profile, spare save). Console `help "PAX Test" 4 ARMO`, `player.additem <id> 1`, `player.equipitem <id>`. Check each outside the suit first (shows the plugin works), then in the suit: visible in third person, stays through exit and re-entry, and through save and reload. Note whether equipping works from the Pip-Boy.
- Caveat: the super mutant model has body segments that the game may hide under worn armor; item B avoids that.
- Result (2026-11-26): the suit refused plain apparel ("you can not equip that in power armor"). Added C and D, the same models with keyword `ArmorTypePower` `0004D8A1` and health 100; installed in the MO2 mod "PAX Test 1".
- **Attachment works (in game, owner screenshots, 2026-11-26):** C and D equip and show on the T-60. C is the unchanged super mutant model, so its big plate is on the right arm, as in the original; D is on the left arm. Route: our own wearable, no vanilla edits. Open: re-entry, save and reload, displaced parts, workbench.
- On exit (in game, 2026-11-26): C and D stay with the frame, listed in its Power Armor menu beside the T-60 pieces, not moved to the player's inventory, but are not displayed on the empty suit. Cause unknown. Getting back in equips and shows them again.
- Pip-Boy in the suit (in game): C and D show as equipped beside all five T-60 pieces; nothing displaced.
- **Item E built (2026-11-26, not yet seen in game):** `placeshield.py ... --write` (`scripts/nif/writeshield.py`) cuts the super mutant model to the plate (192 vertices, 289 triangles), stores it in `LArm_ForeArm1` coordinates, weights it to that bone and reverses the mirrored faces. Installed as `Meshes\PAX\Test\ShieldE.nif` in the MO2 mod, slot 56. The model stays out of the repo.
- **E in game (owner screenshot):** shows on the left arm at the previewed position. Owner: off a bit, nothing connects it to the arm (looks blank; wants metal that joins it), and it is see-through from the back.
- Second version (`--mounts --write`, `scripts/nif/mounts.py`): two solid blocks (3 to 9 and 16 to 23 along the forearm) from arm to shield using the plate's texture, and back faces on the whole plate. Checked offline with back faces hidden (`nifpreview.py render --cull`); no sampled mount point shows through the front. 3600 vertices, 1650 triangles. Position unchanged.
- In game (owner screenshots, aiming with a two-handed gun, 2026-11-26): looks solid; the shield rides the forearm across the front of the body.
- Owner's feel (not measured): the elbow end still stands far off, and it may be turned too far to the outside of the arm. Accepted for now. Open idea (owner): how many attachments PAX should have, beside skills that cost SPECIAL.

## Attachments: cost and unlock (owner, 2026-11-26)
- Attachments cost **no perk point**. They require research or finding something that teaches how, for example the super mutant arm armor the shield comes from, or require that item itself.
- Hand-placed `SupermutantArmor0_Arms_Playable` `00248FD3` in `Fallout4.esm` (read 2026-11-26): Boston Public Library interior (ref `00249009`) and Weston Water Treatment exterior (ref `00248FE6`). DLC, respawning and other sources not checked. Mutants wear `001B3A01` through `CreatureOutfit_Supermutant_Arms` `001B3A22`; whether that one can be looted is unchecked.
- Unlock method open: consume the piece as an ingredient (no script; crafting from a wearable crashed the game once in Regalia, cause unproven), or learn it on finding (needs a script, or a book or perk gate).
- Owner (2026-11-26, leaning, not settled): attachments may also need a SPECIAL cost, with an offset or drawback.
- Placeholder (owner, 2026-11-26): see whether paint schemes can apply to the new visible items.

## Other suits and round 2 (2026-11-26)
- The T-60 placement and its mounts used on the T-45, T-51, X-01 and Raider left arms (offline): at the same settings the forearm shell shows through the front on none, and no plate triangle cuts into the upper arm or shoulder pad hanging or bent 90. The T-60 mounts reach every arm; worst stand-off 2.2 (T-51, elbow block). So one model looks usable for all five. Not seen in game.
- In game with the mounted shield (2026-11-26, owner, screenshot): "blocking looks great".
- Round 2 in the test plugin (installed in MO2 2026-11-26; results below): "PAX Shield (proof)" with armor 50, energy 30 and -1 Agility while worn (`abReduceAgility`); perk `PAXSprintProof` `xx000811` (no sprint AP cost, only in power armor); perk `PAXLockProof` `xx000812` (prompt "PAX: Force Lock" on locked objects in power armor, does nothing); chemistry station recipe making the shield from `00248FD3` and one steel.
- Round 2 results (in game, owner, 2026-11-26): the worn effects apply and reverse on removal. "PAX: Force Lock" shows with the perk in power armor, does nothing, and is not offered outside the suit. The recipe lists at the chemistry station, but the preview shape looks wrong (probably our zero bounds and missing preview transform; fixed in the script, not yet seen). Crafting from the gauntlet made the shield without a crash. Sprint perk works: no AP drain in power armor, normal drain outside (an earlier "no drain anywhere" was god mode). All four round 2 tests pass.
- Craft preview and dropped item (in game, owner, 2026-11-26): copying the vanilla gauntlet's bounds and preview transform (`PTRN` `0022FD4B`) fixed the stretched preview; both then showed the two super mutant arm pieces. Owner: drop the other gauntlet. The shield items now use a trimmed copy (`scripts/nif/trimparts.py --keep 1`, collision unchanged); not yet seen in game.
- In game (owner, 2026-11-26): the one-gauntlet dropped model looks good, and so does the chemistry station preview.

## Slower armor wear (augment, costs SPECIAL; owner, 2026-11-26)
- On the "costs a SPECIAL" list. A multi-point investment that slows power armor wear; never off (Danse-style immunity is too strong). Floor: about 25% of normal wear at the highest.
- Assistant suggestion, not agreed: three ranks at 75%, 50% and 25% wear. SPECIAL stat open.
- Read in game: `fPowerArmorPCArmorDamageMultiplier` is 1.00 (NPC setting 3.0, see [`power-armor-durability.md`](power-armor-durability.md)). That setting is global, so it cannot follow a perk rank without a script.
- Method open. Untested lead (inferred): the perk entry point `Mod Incoming Limb Damage`, conditioned on wearing power armor, if piece wear follows limb damage (the exe has `fPowerArmorLimbDamage...` settings).

## Fist weapons in power armor (read from "WaFists DLC", Nexus 25358, 2026-11-26)
- Its fist weapons are new `WEAP` records whose `DNAM` animation type is 1 (one-handed sword) instead of 0 (hand to hand). The Deathclaw Gauntlet copy differs from vanilla in only that byte; unarmed keywords are kept. *(inferred: this is what lets the suit equip them; untested by us)*
- It also overrides `PowerArmorRace` with no change we found beyond attack order and literal strings, and ships facial bone files; both look like editor leftovers. PAX should not override the race.
- Needs Far Harbor.

## Open questions

- Spending a real perk point: how does a new perk get offered? Adding to the vanilla perk chart may not be possible without changing the interface; a holotape or terminal would need script.
- Whether `WornHasKeyword` detects a vanilla mod on a worn suit (in game).

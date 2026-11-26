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

## Open questions

- Spending a real perk point: how does a new perk get offered? Adding to the vanilla perk chart may not be possible without changing the interface; a holotape or terminal would need script.
- Whether `WornHasKeyword` detects a vanilla mod on a worn suit (in game).

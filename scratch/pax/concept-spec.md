# PAX concept spec (Power Armor eXpansion)

> **Unverified, Gemini-generated.** Saved 2026-11-25 as a starting idea, not a source of truth. Gemini brainstorming has proven full of hallucinations: treat every record name, FormID, function and engine effect below as unconfirmed until read in xEdit or the script sources, or tested in game.

## Open items

Concerns not marked *checked* come from general FO4 knowledge, untested. Sections under *Notes* supersede the draft where they differ.

| # | Claim in the draft | State | How to check |
|---|---|---|---|
| 1 | `Game.GetPlayer().ModPerkPoints(-1)` | *Checked 2026-11-25:* installed sources declare `Game.AddPerkPoints(int)`; no `ModPerkPoints` seen in them (not every vanilla script is present). Whether a negative value works is unknown | In game |
| 2 | `RegisterForControl("SecondaryAttack")` | *Checked 2026-11-25:* it is an F4SE addition (`ScriptObject.psc`), so F4SE would be a requirement the draft does not list. Likely does not suppress the grenade or bash | In game |
| 3 | Shoulder and forearm meshes on biped slots 55 and 56 | May not render on a power armor frame. Hardpoint and Deflector Guard visuals depend on it; new meshes are a large job | One throwaway mesh test |
| 4 | Vanilla power armor mod names, body slots and keywords | *Checked 2026-11-25:* base game names and slots correct for those checked (see Notes). DLC and Creation Club not scanned | In game: keyword detection |
| 5 | `Mod Armor Health`, companion `Misc` attach points, speed, swing speed, knockdown and other effects | Engine behaviour not confirmed | xEdit, then in game |
| 6 | Compatibility with NEO, UCO and legendary overhauls; "zero conflict" | No overrides lowers risk but proves nothing. Treat as a goal | Test with those mods |
| 7 | Papyrus toolchain on the Deck (Creation Kit or Caprica) | Not set up. Not needed yet; spending perk points from a holotape will need it | Decide when scripting starts |
| 8 | Unlock method without scripts | Options: recipe gates (see Notes), or a crafted book that grants the perk. Neither spends perk points | Four-recipe test: which conditions hide a recipe |
| 9 | v1 scope | Undecided. Suggested start: passive perks and a few mod-gated upgrades | Owner |

## Notes (2026-11-25)

### Design direction (owner)
- Every upgrade has a cost or a trade-off: it costs something, or has a drawback that makes the player ask "why would I use it".
- Upgrades stack on top of vanilla mods; existing records are left alone so other power armor mods don't conflict.
- Example: a perk overclocking Motion-Assist Servos, +1 Strength per perk spent up to a maximum, only in power armor.
- Working notes: `common.md` and the `notes.md` in each area folder (see `handoff.md`).
- Gate progression to make it interesting: robot-themed upgrades behind knowing the robot recipe (Automatron); others behind quests or recovering an object; simple overclocks and expertise behind perks.

### Gating without our own script
| Gate | Recipe condition | Behaviour |
|---|---|---|
| Know a robot recipe | `GetGlobalValue` on an Automatron global | Expected to hide; untested in our plugin |
| Expertise | `HasPerk` | Greyed; only two shown |
| Quest progress | `GetStageDone` or `GetQuestCompleted` | Untested |
| Recover an object | `GetItemCount` | Only while carried; hiding untested |

Detail: Alexandria `fo4-recipes-and-gates`. Robot gates need Automatron as a master, finishing it opens them all, and only some robot parts have a global.

Open: should a robot-gated upgrade also require a perk (the part reveals it, expertise builds it)?

### Vanilla power armor misc mods (`Fallout4.esm`, read from the plugin)
| Slot | Mods (keyword suffix after `dn_HasMisc_`) |
|---|---|
| Helmet | Targeting HUD (`DetectLife`), Internal Database (`Int`), VATS Matrix Overlay (`VATSChance`), Sensor Array (`Sensor`), Recon Sensors (`Recon`), Rad Scrubbers (`RadScrubbers`) |
| Torso | Motion-Assist Servos (`Str`), Stealth Boy (`StealthBoy`), Medic Pump (`MedicPump`), Core Assembly (`BatRegen`), Reactive Plates (`Reactive`), Tesla Coils (`Tesla`), Jet Pack (`JetPack`), Blood Cleanser (`Cleanser`), Emergency Protocols (`Emergency`), Kinetic Dynamo (`Kinetic`), Welded Rebar (`DMGShield`) |
| Arms | Hydraulic Bracers (`Unarmed`), Optimized Bracers (`Optimized`), Tesla Bracers (`ShockDmg`), Rusty Knuckles (`Bleed`) |
| Legs | Calibrated Shocks (`Carry`), Explosive Vent (`ExplVent`), Overdrive Servos (`SprintBoost`), Optimized Servos (`OptimizedServos`), Kinetic Servos (`APRegen`) |

- All attach at `ap_PowerArmor_Misc`: one per piece.
- Raider has no Stealth Boy, Jet Pack, Tesla Bracers, VATS Matrix Overlay or Recon Sensors. Welded Rebar is Raider only.
- Whether `WornHasKeyword` sees these on a worn suit is untested.
- Rad Scrubbers already exists; the draft's "Closed-Loop Rad Scrubbers" overlaps it.
- T-60 torso mod recipes checked use perk conditions only.

---

## Original draft (unedited)

# Fallout 4 Mod Architecture & Design Specification: Modular Power Armor Engineering Chassis Expansion \- or Power Armor eXpansion

**Target Environment:** SteamOS / Steam Deck (Desktop Mode) via Mod Organizer 2 (MO2), FO4Edit (xEdit), and PapyrusCompiler (`Caprica` / Creation Kit compiler under Proton)  
**Target Plugin Format:** `.esl` (Light Master — zero load-order slot impact)  
**Compatibility Guarantee:** Zero record overrides on vanilla Power Armor pieces (`ARMO`), Object Mods (`OMOD`), Instance Naming Rules (`INNR`), or leveled lists (`LVLI`). Full compatibility with NEO, UCO, and legendary-swapping overhauls.

---

## 1\. Architectural Overview & Core Principles

This mod transforms Power Armor from static stat-sticks into a modular, resource-driven engineering platform controlled via a custom **Holotape / Terminal interface**.

### Key Design Pillars

1. **Zero-Conflict Isolation:** All progression is driven by player-only hidden Perks (`PERK`), Magic Effects (`MGEF`), Spells (`SPEL`), and Papyrus scripts gated by `IsInPowerArmor == 1`. General NPCs and vanilla Power Armor records remain untouched.  
2. **Dual-Gating Progression:** Unlocking upgrades on the Holotape requires spending **Perk Points** (`Game.GetPlayer().ModPerkPoints(-1)`) plus **salvaged components / hardware** (`RemoveItem`), replacing arbitrary SPECIAL attribute gates with active engineering investments.  
3. **Hardware Prerequisite Overclocks:** Rather than overriding vanilla Power Armor workbench mods, advanced "Overclock" firmware reads existing attached vanilla mods via `WornHasKeyword(...)` (e.g., checking for the vanilla *Stealth Boy*, *Tesla Coils*, *Medic Pump*, or *Hydraulic Bracers* keywords). This forces meaningful physical loadout choices at Power Armor Stations without slot conflicts.  
4. **Operational Fuel & Resource Consumption:** Active modules and failsafes check for and silently deduct physical ammunition, medical supplies, or scrap components upon firing or triggering (`GetItemCount` / `RemoveItem(..., abSilent = true)`), integrating tightly with Survival Mode and hardcore resource loops.

---

## 2\. Activation Taxonomy (Engine Mapping)

Modules are organized by **how the Fallout 4 engine triggers them**, separating passive perk math from combat-event listeners and manual hotkeys:

| Activation Category | Engine Mechanism | Trigger Condition | Companion Support |
| :---- | :---- | :---- | :---- |
| **1\. Always-On Frame Firmware** | Hidden `PERK` / `SPEL` | `IsInPowerArmor == 1` | Player-only (via Holotape Perks) |
| **2\. Workbench Overclock Passives** | Hidden `PERK` / `SPEL` \+ `WornHasKeyword` | `IsInPowerArmor == 1` AND specific vanilla `OMOD` keyword present | Works natively if baked onto companion `OMOD`s |
| **3\. Action-Bound Enhancers** | Conditioned `SPEL` / `PERK` (`IsSprinting`, `IsBlocking`, `IsMoving == 0`) or `RegisterForControl` | Triggered automatically during movement/stance actions (with optional `WornHasKeyword` hardware gate) | Inconsistent (AI sprints/blocks erratically) |
| **4\. Threshold & Reactive Failsafes** | `OnHit` / `OnEnterBleedout` events or HP/AP threshold conditions (`GetActorValuePercentage`) | Fires automatically on state changes; deducts emergency fuel/consumables | Very reliable via `OnHit` / threshold `SPEL`s |
| **5\. Active Mounted Hardpoints** | `RegisterForControl("SecondaryAttack")` (Grenade/Bash key) \+ Slot `55` visual mesh | Manual hotkey press on cooldown \+ ammo/component check | Not suitable for AI; use automated combat `SPEL`s instead |
| **6\. Sensor & Toggle Suites** | Holotape toggle GlobalVariables (`GLOB`) \+ `IMAD` / `PERK` | Semi-persistent toggle switched via Holotape | Player-only |
| **7\. Squad Commander Link** | Teammate Aura (`IsPlayerTeammate == 1`) \+ dedicated Companion `OMOD`s on vanilla `Misc` slots | Active when player is in PA or bolted directly onto companion armor pieces | Full support (passive/reactive `OMOD`s \+ workstation rename tagging) |

---

## 3\. Complete Module Roster (v1.0 Candidate Matrix)

### Category 1: Always-On Frame Firmware (Direct Perk Replacements)

*Active whenever wearing any Power Armor frame. No physical workbench mod required.*

| Module Name | Replaces / Emulates | Mechanical Effect | Holotape Unlock Cost |
| :---- | :---- | :---- | :---- |
| **Sub-Routine: Locksmith** | *Locksmith* (PER 4\) | Unlocks Novice \$\\rightarrow\$ Master locks while in Power Armor. | 1 Perk Point \+ `2x Circuitry`, `2x Bobby Pins` |
| **Sub-Routine: Intrusion** | *Hacker* (INT 4\) | Unlocks Novice \$\\rightarrow\$ Master terminals while in Power Armor. | 1 Perk Point \+ `3x Circuitry`, `1x Fiber Optics` |
| **Ablative Plate Reinforcement** | Custom Durability Scaling | Reduces Power Armor piece wear (`Mod Armor Health`) by 25% / 50% / 75% across 3 ranks. | 1 Perk Point/rank \+ `5x Steel`, `2x Aluminum` |
| **Closed-Loop Rad Scrubbers** | *Rad Resistant / Ghoulish* | \+150 Rad Resist and slow passive radiation purge when out of combat. | 1 Perk Point \+ `2x Nuclear Material`, `3x Rubber` |
| **Servo-Assisted Load Bearing** | *Strong Back* (STR 6\) | \+50 / \+100 Carry Weight and allows normal walking speed while over-encumbered. | 1 Perk Point \+ `4x Gears`, `4x Springs` |

### Category 2: Workbench Overclock Passives (Hardware-Gated)

*Requires the listed vanilla Power Armor workbench mod installed on your worn armor (`WornHasKeyword`).*

| Vanilla PA Mod Required | Overclock Upgrade | Mechanical Effect | Unlock Cost |
| :---- | :---- | :---- | :---- |
| **Motion-Assist Servos** *(Torso)* | **Heavy Actuator Overdrive** | Boosts Strength bonus from \+2 to **\+4** and increases melee/unarmed swing speed by **\+15%**. | 1 Perk Point \+ `3x Gears`, `2x Oil` |
| **Internal Database** *(Helmet)* | **Tactical Co-Processor** | Grants **Awareness** (target resistances in VATS) and **Concentrated Fire** accuracy stacking. | 1 Perk Point \+ `3x Circuitry`, `1x Crystal` |
| **VATS Matrix Overlay** *(Helmet)* | **Ballistic Trajectory Predictor** | Adds **Ricochet** projectile deflection chance and \+15% VATS critical damage. | 1 Perk Point \+ `2x Fiber Optics`, `2x Silver` |
| **Optimized / Hydraulic Bracers** *(Arms)* | **Gyro-Stabilized Weapon Mounts** | Grants **Sniper** breath/sway elimination and tightens hip-fire spread by 25%. | 1 Perk Point \+ `2x Springs`, `2x Aluminum` |

### Category 3: Action-Bound Enhancers (Movement & Stance Triggers)

*Fires automatically during player movement or combat stances. Overclocked entries require the paired vanilla workbench mod.*

| Module Name | Hardware Prerequisite | Trigger & Mechanical Effect | Operational Fuel / Constraint |
| :---- | :---- | :---- | :---- |
| **Assaultron Optical Overclock** | **Stealth Boy** *(Torso)* | Extends Stealth Boy invisibility field to **Sprinting** (`IsSprinting == 1`), turning the suit into an optical blur while rushing cover. | Drains AP at 2x vanilla Stealth Boy rate while sprinting; drops when AP hits 0\. |
| **Ballistic Deflector Guard** | **Hydraulic Bracers** *(Arms)* | Reduces incoming ballistic/energy damage by **\-40% while blocking** (`IsBlocking == 1`) and displays forearm shield plates (Slot `56`). | Drains `5 AP` per blocked heavy hit. |
| **Mr. Handy Horizontal Thrusters** | **Explosive Vent** *(Legs)* | Converts vertical drop-vent tech into a **horizontal sprint-dash** (`Blitz` lunge) that staggers enemies in path. | Costs `25 AP` per dash \+ 8-second cooldown. |
| **Hydraulic Ground-Anchor Clamps** | **Calibrated Shocks** *(Legs)* | Grants **Rooted** (-30% incoming damage, \+25% melee damage) whenever standing still (`IsMoving == 0`). | None (mechanical clamp lock). |
| **Ramming Speed Overclock** | **Overdrive Servos** *(Legs)* | Grants **Pain Train Rank 3** sprint knockdowns and \+20% sprint speed without Strength 10\. | Drains 2x Fusion Core charge while sprinting. |

### Category 4: Threshold & Reactive Failsafes (Automated Combat Triggers)

*Triggered by `OnHit` events or HP/AP thresholds. Automatically consumes inventory supplies when firing.*

| Module Name | Hardware Prerequisite | Trigger & Mechanical Effect | Operational Fuel / Cost |
| :---- | :---- | :---- | :---- |
| **Triage Nanite Emitter** | **Medic Pump** *(Torso)* | Pulses an out-of-combat **Squad Regeneration Beacon** that heals injured/downed companions after combat ends. | Consumes **1x Stimpak** (or `1x Antiseptic`) per post-combat triage pulse. |
| **Overdrive Capacitor Surge** | **Core Assembly** *(Torso)* | Auto-fires a **Sentry Steam Vent** knockback \+ **\+100 AP instant restore** when AP drops below 15% in combat. | Consumes **1x Nuclear Material** per surge \+ 45-second cooldown. |
| **Shrapnel Counter-Detonation** | **Reactive Plates** *(Torso)* | Triggers an automated fragmentation blast when struck in melee, staggering heavy attackers. | Consumes **2x Steel** (or `1x Frag Grenade`) per detonation \+ 12-second cooldown. |
| **Cryo-Coolant Emergency Dump** | None (Frame Failsafe) | Triggers a freezing AoE nova around the suit when HP drops below **20%**, slowing attackers so you can relocate. | Consumes **1x Cryo Cell** (or `2x Antifreeze / Coolant`) \+ 60-second cooldown. |

### Category 5: Active Mounted Hardpoints (Hotkey `SecondaryAttack`)

*Visual shoulder mount rendered on Biped Slot `55`. Fired manually via the Grenade/Bash key (`SecondaryAttack`) without unequipping your primary weapon.*

| Hardpoint Name | Visual Mesh | Tactical Effect | Operational Fuel & Cooldown |
| :---- | :---- | :---- | :---- |
| **Sentry Cluster Mortar** | Shoulder-mounted missile/mortar pod (Slot `55`) | Launches a high-arc explosive micro-missile salvo toward the player's aim vector. | Consumes **2x Missiles** (or `4x 5mm Rounds`) \+ 15-second cooldown. |
| **Assaultron Focus Beam** | Shoulder emitter array (Slot `55`) | Fires a sustained high-energy crimson laser beam that melts heavy armor. | Consumes **3x Fusion Cells** \+ 20-second cooldown. |
| **Voltaic Arc Discharge** | Requires **Tesla Coils** *(Torso)* | Fires a chain-lightning shockwave that stuns robots/turrets and jumps between up to 4 targets. | Consumes **2x Fusion Cells** \+ 20-second cooldown. |
| **Corrosive Acid Sprayer** | Shoulder chemical nozzle (Slot `55`) | Sprays a short-range cone of armor-stripping acid (`Mod Target Damage Resistance`). | Consumes **1x Acid** from junk inventory \+ 12-second cooldown. |

### Category 6: Sensor & Toggle Suites (Holotape Switches)

*Toggled on or off via the Holotape menu using GlobalVariables (`GLOB`).*

| Suite Name | Hardware Prerequisite | Mechanical Effect |
| :---- | :---- | :---- |
| **Low-Light Optical Overlay** | **Targeting HUD** *(Helmet)* | Clean green/amber `IMAD` Night Vision toggle without red target-highlight clutter. |
| **Deep-Scan Penetrator** | **Sensor Array** *(Helmet)* | Grants **Penetrator** (VATS targeting through walls/cover) and Recon enemy tagging while aiming. |

### Category 7: Squad Commander Link (Companion Support)

*Designed for companion AI reliability—avoiding manual hotkeys and relying on passive `OMOD`s on vanilla `Misc` attach points plus workstation renaming (`[Squad] ...`) for stash clarity.*

* **Squad Ballistic Sync (Holotape Perk):** Grants active companions (`IsPlayerTeammate == 1`) unbreakable Power Armor piece durability and infinite ammo (`TeammateDontUseAmmoKeyword`) while wearing Power Armor.  
* **Companion-Tuned `OMOD`s (Craftable on Vanilla `Misc` Slots):** Dedicated workbench mods (*Automated Point-Defense Tesla*, *Self-Sealing Ablative Plating*, *Auto-Stim Triage Core*) that attach to standard Power Armor `Misc` points so they display cleanly in the Pip-Boy inspect card without modifying vanilla `ARMO` records.

---

## 4\. Holotape & Terminal UX Architecture

1. **Suite Diagnostics (Top Menu):** Dynamically reads `WornHasKeyword` and unlocked `PERK` states to display which Overclocks are currently `ONLINE` vs. `OFFLINE (Missing Hardware)` on your equipped suit.  
2. **Firmware & Overclock Installation:** Categorized submenus by activation type showing Perk Point cost, required scrap components, and hardware prerequisites.  
3. **Sensor & Hardpoint Configuration:** Toggle switches for Night Vision `IMAD` and selection of which unlocked **Mounted Hardpoint** is currently mapped to `SecondaryAttack` (Slot `55`).

---

## 5\. Implementation Roadmap for Claude Code

1. **Phase 1 — Plugin Skeleton (`.esl`):** Create clean base records (`KYWD`, `GLOB`, `MESG`, `TERM`, `HOLOTAPE`) in FO4Edit / xEdit automation script with `0x800+` FormIDs and zero vanilla overrides.  
2. **Phase 2 — Passive & Overclock Perks (`PERK` / `SPEL`):** Implement Categories 1, 2, 3, and 6 using native condition functions (`IsInPowerArmor`, `WornHasKeyword`, `IsSprinting`, `IsBlocking`, `IsMoving`) before writing custom Papyrus.  
3. **Phase 3 — Papyrus Event & Resource Controller:** Write modular Quest/Alias Papyrus scripts (`PAEng_ControllerScript.psc`) handling:  
   * `RegisterForControl("SecondaryAttack")` for Mounted Hardpoints \+ cooldown timers.  
   * `OnHit` / threshold checks for Reactive Failsafes.  
   * Inventory checks (`GetItemCount` / `RemoveItem(..., abSilent = true)`) for ammo, Stimpaks, and scrap fuel consumption.  
4. **Phase 4 — Holotape Terminal & Diagnostics:** Wire `TERM` menu conditions and Papyrus fragments for Perk Point deduction, salvage removal, and live suit diagnostics.  
5. **Phase 5 — Companion `OMOD`s & Testing:** Build companion-specific `OMOD`s targeting vanilla `ap_PA_*_Misc` attach points and validate in-game under MO2 on SteamOS.
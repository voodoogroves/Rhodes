# Plan spec: Blade of Bastet (version 0.1)

*Status: DRAFT. Mechanics for the one item in 0.1. Intent lives in `concept-spec.md`. Each fact is marked **Verified** (read from the game files or the xEdit source on 2026-11-22) or **To verify** (needs xEdit or in-game testing). Nothing here has been built or tested.*

## Goal (from the concept-spec)

Convert a Chinese Officer Sword the player already owns into the Blade of Bastet. It keeps the sword's vanilla stats and mods, and adds 30% built-in armor penetration. Later, with the Eye of Ra worn, it ignores all armor (not part of 0.1).

## Plugin

- One light plugin (`.esl`), no scripts, no archives, no vanilla record overrides. **Name: to decide** (the brainstorm used `OrderOfMysteries.esl`).
- **Master dependencies:** `Fallout4.esm` only for 0.1. No DLC asset is used.

## Base record

| Item | Value | Status |
|---|---|---|
| Source weapon | `WEAP 00147BE4` `ChineseOfficerSword` (the brainstorm's `$000330B8` is wrong) | Verified |
| Keywords on the source | `Anims1hmWeapon`, `WeaponTypeMelee1H`, `QuickkeyMelee`, `ma_ChineseOfficerSword`, `AnimsStabWeapon`, `ObjectTypeWeapon` | Verified |
| Attach points | `ap_melee_MeleeMod`, `ap_Legendary` | Verified |
| Equip type | `RightHand` | Verified |
| Instance naming | `dn_CommonMelee` | Verified |

**New record:** `MoM_WEAP_BladeOfBastet`, a copy of the source with a new name. Keep `ma_ChineseOfficerSword` and both attach points so the vanilla sword mods still apply and the legendary slot stays open. *To verify:* that vanilla sword mods attach to the copy through that keyword.

Base damage and speed are inherited unchanged. *Not yet read:* the sword's damage lives in a record or template I did not trace; compare in xEdit before final.

## Armor penetration (the one change)

**How vanilla does it (Verified):**
- Weapon stat `ArmorPenetration` (AVIF `00097341`): 0 to 100, a percentage of the target's armor ignored.
- Legendary "Penetrating": OMOD `001F4426` sets that property to `30.0` and attaches ENCH `001F4425` -> MGEF `001F4423` (Add Perk) -> PERK `001F4166`.
- That perk has one entry point, **Mod Target Damage Resistance** (entry point 37 in the xEdit definitions), with the AV `ArmorPenetration` and a small multiplier (about `-0.01`). *Inference, not confirmed:* it subtracts (weapon stat x 1%) from the target's damage resistance.

**Our approach (proposed), avoiding the legendary slot:**
1. Weapon `EITM` (base enchantment) = new `MoM_ENCH_BladeOfBastet`, constant effect on the wielder.
2. ENCH effect = new MGEF `MoM_MGEF_BladeOfBastetPerk`, a copy of `001F4423` (Add Perk).
3. MGEF adds new PERK `MoM_PERK_BladeOfBastet`: entry point **Mod Target Damage Resistance**, value **-0.30** (30% of the target's armor ignored). A second entry for the Eye of Ra (-1.00) comes later, conditioned on the Eye being worn.

Why this over copying the OMOD: the vanilla legendary OMOD occupies `ap_Legendary`, which would stop players adding a legendary effect. A weapon's own `EITM` does not use that slot.

**To verify:**
- That a constant-effect `EITM` on a melee weapon applies while it is equipped and stops when it is not.
- That the perk's armor reduction works as inferred (a 30% reduction of the target's resistance), by comparing damage against an armored enemy with and without.
- Fallback if it fails: the OMOD route (set `ArmorPenetration` = 30 as a property, as vanilla does), accepting that it uses the legendary slot or needs a new attach point.

## Crafting and discovery

**Recipe (`COBJ`):** consume `1x Chinese Officer Sword` plus materials; create `MoM_WEAP_BladeOfBastet`. The brainstorm proposed: 2 Silver, 2 Circuitry, 1 Fiber Optics, perk gates (Blacksmith 1, Science! 1). *Component FormIDs and the perk gates are not verified and the brainstorm's IDs contain known duplicates; re-derive all of them in xEdit.* **Workbench: to decide.** A weapon workbench only crafts mods in vanilla, so the Chemistry Station (utility category) is the likely home; the keyword names were not confirmed.

**Discovery gate (Verified IDs, behaviour to verify):**
- Quest `MS04` = `QUST 00027556`.
- Costume `ARMO 000E1A25` `MS04_SilverShroudCostume`. Other Silver Shroud armors exist (`ClothesSilverShroud 0014E58B`, hat `0014E58E`, `MS04_SilverShroudArmor_15/25/35/45`); decide which one the player actually receives and whether to test any of them.
- Condition: has the costume **or** quest stage reached. The brainstorm's stage `20` is **unverified**; read the quest's stages in xEdit.
- Condition encoding (Verified): `GetItemCount` index 47, `GetStageDone` index 59, `>=` is Type `96`, `==` is Type `0`, the OR flag is `1` on the first of two OR'd conditions. Run On: Subject `0`.

## Known errors in the Gemini brainstorm that this spec corrects

- Wrong sword ID; wrong condition indices; wrong `Run On` for "Target"; `MOD2`/`MOD3` swapped; wrong slot numbers; invented material paths; a script that would not run. See the Alexandria note `memory/fo4-xedit-reference.md`.

## Test plan (for the Steam Deck, in the separate MO2 instance)

1. Plugin loads (light master) with no errors in xEdit.
2. Recipe is hidden until the discovery condition is met, then appears.
3. Crafting consumes the sword and produces the Blade; vanilla mods still attach.
4. Damage against a heavily armored enemy is higher than the plain sword; against an unarmored enemy it is the same.
5. Removing the Blade removes the effect; a legendary effect can still be added.

## Open items

- Plugin name; workbench and category; materials and perk gates; Silver Shroud stage number and which costume item; the damage/template tracing.

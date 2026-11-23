# Plan spec: Blade of Bastet (version 0.1)

*Status: DRAFT. Mechanics for the one item in 0.1. Intent lives in `concept-spec.md`. Each fact is marked **Verified** (read from the game files or the xEdit source on 2026-11-22) or **To verify** (needs xEdit or in-game testing). Nothing here has been built or tested.*

## Goal (from the concept-spec)

Convert a Chinese Officer Sword the player already owns into the Blade of Bastet. It keeps the sword's vanilla stats and mods, and adds 30% built-in armor penetration. Later, with the Eye of Ra worn, it ignores all armor (not part of 0.1).

## Plugin

- One light plugin (`.esl`), no scripts, no archives, no vanilla record overrides.
- **Filename: `RegaliaOfMystery.esl`** (decided). It must not change once saves exist, so it covers the whole set, not just the Blade. The public title (e.g. on Nexus) can differ.
- **EditorID prefix: `MoM_`** (decided), used on every new record.
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

**Recipe (`COBJ`), proposed:** consume the sword, plus materials; create `MoM_WEAP_BladeOfBastet`.

| Ingredient | Amount | Why |
|---|---|---|
| Chinese Officer Sword (`00147BE4`) | 1 | the conversion base (vanilla recipes already use items as ingredients: the Baseball grenade uses a `Baseball`, the Bottlecap mine a `LunchBoxKids01`) |
| Steel (`c_Steel`) | 4 | the blade work |
| Silver (`c_Silver`) | 3 | the ceremonial theme |
| Circuitry (`c_Circuitry`) | 2 | the fine mechanism |
| Adhesive (`c_Adhesive`) | 3 | common, matches other melee recipes |

About 12 components plus the sword, in line with vanilla sword mods (the Shock mod costs 18 components; Shock+Serrated 26). No fiber optics, gold or nuclear material, which are scarcer.

**Perk gate: Blacksmith rank 2 only** (`Blacksmith02`, via the `HasPerk` condition, function index `448`). The sword's own Serrated and Shock mods use the same rank (Verified), and the story gate already limits who sees it, so a second perk gate (Science) would be ceremony.

*Component names above are verified to exist in the game (31 components, including Silver, Steel, Circuitry, Adhesive). FormIDs still need reading in xEdit.* *To verify in-game:* whether a sword that already has mods installed counts as the ingredient, and what the player gets back (the Blade comes unmodded).

**Workbench: Chemistry Station** (see below).

**Workbench: Chemistry Station (keyword `WorkbenchChemlab`).** Verified: in Fallout4.esm, the DLC and the installed Creation Club files, the 20 recipes that create a weapon item (mines and grenades) all use this station; the weapon and armor workbenches are built around mods, not new items. The recipe's category/filter keyword is *to verify*.

**Discovery gate:**
- Quest `MS04` = `QUST 00027556`. The brainstorm's stage `20` does not exist. Stages that do exist (from the quest's log text): `25` Kent's call, `100` Kent wants a costume from Hubris Comics, `200` found the costume, `390` refused to be the Shroud, `400` agreed to be the Shroud (wear the costume, patrol), `410`-`1360` the missions, `1400` Sinjin dealt with, `1425` the Silver Shroud story wrapped up.
- **Gate: the player has answered Kent, either way (stage 390 or later).** Refuse at 390 ("I am the Mistress") or accept at 400; both unlock the recipe, and players still at stages 25 to 200 do not get it.
- **Single condition:** `GetStage(MS04) >= 390`. `GetStage` is condition index `58` (Verified in the xEdit definitions); `>=` is Type `96`; comparison value `390`; Run On Subject `0`. No item check (an item check cannot see stored gear) and no OR.
- **Fallback if `GetStage` misbehaves:** two conditions, `GetStageDone(MS04, 390) == 1` OR `GetStageDone(MS04, 400) == 1` (`GetStageDone` is index `59`; OR flag `1` on the first).
- Rejected: stage 200 (found the costume; loses the choice theme), 1425 (too late), 390 alone (probably excludes everyone who accepts the role).
- Condition encoding (Verified): the `MS04` quest is the vanilla Silver Shroud quest; the costume items (`MS04_SilverShroudCostume 000E1A25` etc.) are not needed under this gate.
- *To verify in-game:* that `GetStage` returns the highest/most recent stage (not reset when the quest advances or completes), that stage 390 is set on refusal and 400 on acceptance, and that the recipe stays visible after the quest finishes.

## Instructions item

A holotape (or similar) explaining the conversion. It cannot be placed in the world or given by a script without editing vanilla records or using Papyrus, so the likely route is a craftable item shown with the recipes once discovered. *To verify:* the holotape/note record type that shows text without a script (probably a note that opens a terminal), and that it can be crafted at the same station.

## Known errors in the Gemini brainstorm that this spec corrects

- Wrong sword ID; wrong condition indices; wrong `Run On` for "Target"; `MOD2`/`MOD3` swapped; wrong slot numbers; invented material paths; a script that would not run. See the Alexandria note `memory/fo4-xedit-reference.md`.

## Test plan (for the Steam Deck, in the separate MO2 instance)

1. Plugin loads (light master) with no errors in xEdit.
2. Recipe is hidden until the discovery condition is met, then appears.
3. Crafting consumes the sword and produces the Blade; vanilla mods still attach.
4. Damage against a heavily armored enemy is higher than the plain sword; against an unarmored enemy it is the same.
5. Removing the Blade removes the effect; a legendary effect can still be added.

## Open items

- Materials and perk gate (proposed above, awaiting agreement); instructions item (holotape) mechanism; recipe category keyword; materials and perk gates; gate behaviour (`GetStage >= 390`) tested in-game; the damage/template tracing.

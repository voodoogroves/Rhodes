# Checkpoint: Regalia of Mystery (2026-11-22)

**Decided:** plugin `RegaliaOfMystery.esl`, EditorID prefix `MoM_`. Versions 0.x, 1.0 = release. 0.1 = Blade of Bastet (convert a Chinese Officer Sword; 30% armor penetration; 100% with Eye of Ra later). Eye of Ra is a non-visible locket before 1.0. Discovery gate `GetStage(MS04) >= 390`. Chemistry Station, `RecipeUtility`. Instructions in the item description for 0.1.

**Where things live:** concept (active) here in Rhodes; plan specs in `fo4-regalia-of-mystery/spec/`; Gemini brainstorm and old scratch copies in Alexandria `historical/regalia/`; verified xEdit/asset facts in Alexandria `memory/fo4-xedit-reference.md`.

**Open:** the in-game tests listed in the specs; item specs for Eye of Ra, Veil, Garb, Voice of Set. (Component and perk FormIDs and the sword's base damage are done.) The concept retires when every item has a spec.

**Done 2026-11-23:** separate MO2 for Fallout 4 built with MO2-LINT; F4SE 0.7.9 loads and the game reaches the main menu; FO4Edit 4.1.5f (32-bit) loads Fallout4.esm and the DLC. Steps and gotchas are in `refs/steam-deck-mo2.md`.

**Built (2026-11-23):** `RegaliaOfMystery.esp` (a plain `.esp`; ESL flag still to do) made by `fo4-regalia-of-mystery/build/xedit/BuildBlade.pas`: the Blade (sword copy, vanilla armor-penetration enchantment, template stat 30) and an ungated recipe. It crafts in game; the description shows in the crafting menu only. Verified FormIDs, the sword's base damage (16) and the penetration mechanism are in the specs and Alexandria `memory/fo4-xedit-reference.md`.

**Armor penetration status (end of 2026-11-23):** the weapon-record approach (EITM + template stat) does NOT work: stat 0, no perk, dummy unchanged; the legendary-mod template include also failed. A vanilla legendary (Sword of Wonders) works and is the control (`getav ArmorPenetration` 30, `hasperk 001F4166` 1). The earlier "Upgrade-slot mod" test was invalid (a script bug), so that is still untested. Vanilla facts and the three mechanisms are in the spec ("Armor penetration: in-game findings") and Alexandria `memory/fo4-xedit-reference.md`.

**Next session:** run `build/xedit/BuildBladePerk.pas` (plugin name `RegaliaPerkTest2`; the BUILD entry already points at it). Mod B (vanilla trio on an Upgrade-slot mod): equip, then the two console checks. Mod A (our keyword + our perk): `help "Bastet" 4 PERK`, `player.addperk <ID>`, dummy in the heavy combat chest (plain 15, expect about 31). Only `RegaliaPerkTest2.esp` ticked; set Normal difficulty. The older `Regalia*.esp` files in the game's Data folder are stale test plugins (OfMystery, Test100, ModTest, LegendaryTest, LegendTest, LegendTest2, PerkTest): untick or remove. `BuildBlade.pas` still has TEST100 values uncommitted; restore to 30 or retire it once the approach is chosen.

**Ideas on the table (Chris):** a mundane Blade (keyword for the vanilla 15%, no bleed/shock, tuned damage; Eye of Ra raises it to 100% via a perk with a worn-item condition; maybe a re-textured blade via material swap, not yet investigated); a holotape "Cryptos" as the instructions and perk-grant hub (a small Papyrus `AddPerk` is acceptable; lore: a computer Rivers had in Fallout 76, unverified); the legendary + Eye of Ra coordination for 100%.

**Then:** add the quest and perk gates (`GetStage(MS04) >= 390`, `Blacksmith02`), flag the plugin ESL, item specs for Eye of Ra, Veil, Garb, Voice of Set.

**Checked:** `~/Repos/CLAUDE.md` (a symlink into Rhodes) does load when Claude starts from `~/Repos`.

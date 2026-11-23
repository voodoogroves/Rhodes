# Checkpoint: Regalia of Mystery (2026-11-22)

**Decided:** plugin `RegaliaOfMystery.esl`, EditorID prefix `MoM_`. Versions 0.x, 1.0 = release. 0.1 = Blade of Bastet (convert a Chinese Officer Sword; 30% armor penetration; 100% with Eye of Ra later). Eye of Ra is a non-visible locket before 1.0. Discovery gate `GetStage(MS04) >= 390`. Chemistry Station, `RecipeUtility`. Instructions in the item description for 0.1.

**Where things live:** concept (active) here in Rhodes; plan specs in `fo4-regalia-of-mystery/spec/`; Gemini brainstorm and old scratch copies in Alexandria `historical/regalia/`; verified xEdit/asset facts in Alexandria `memory/fo4-xedit-reference.md`.

**Open:** the in-game tests listed in the specs; item specs for Eye of Ra, Veil, Garb, Voice of Set. (Component and perk FormIDs and the sword's base damage are done.) The concept retires when every item has a spec.

**Done 2026-11-23:** separate MO2 for Fallout 4 built with MO2-LINT; F4SE 0.7.9 loads and the game reaches the main menu; FO4Edit 4.1.5f (32-bit) loads Fallout4.esm and the DLC. Steps and gotchas are in `refs/steam-deck-mo2.md`.

**Built (2026-11-23):** `RegaliaOfMystery.esp` (a plain `.esp`; ESL flag still to do) made by `fo4-regalia-of-mystery/build/xedit/BuildBlade.pas`: the Blade (sword copy, vanilla armor-penetration enchantment, template stat 30) and an ungated recipe. It crafts in game; the description shows in the crafting menu only. Verified FormIDs, the sword's base damage (16) and the penetration mechanism are in the specs and Alexandria `memory/fo4-xedit-reference.md`.

**Open question:** does the armor penetration really work? Single hit counts on a Protectron: plain 22 to 23, Blade (30) 22, TEST100 18. The formula predicts about 2x fewer hits for stat 100, so the effect is smaller than expected or noise. Next: repeated counts (3 each), a fixed-stat target (`00106B09`) or a heavily armored one, then decide whether the template-level stat is enough or the OMOD route is needed. **Uncommitted on purpose:** `BuildBlade.pas` still has the TEST100 values; restore to 30 and commit when testing is done. `RegaliaTest100.esp` is in the game's `Data` folder; untick or remove it afterwards.

**Then:** add the quest and perk gates (`GetStage(MS04) >= 390`, `Blacksmith02`), flag the plugin ESL, item specs for Eye of Ra, Veil, Garb, Voice of Set.

**Checked:** `~/Repos/CLAUDE.md` (a symlink into Rhodes) does load when Claude starts from `~/Repos`.

# Checkpoint: Regalia of Mystery (2026-11-22)

**Decided:** plugin `RegaliaOfMystery.esl`, EditorID prefix `MoM_`. Versions 0.x, 1.0 = release. 0.1 = Blade of Bastet (convert a Chinese Officer Sword; 30% armor penetration; 100% with Eye of Ra later). Eye of Ra is a non-visible locket before 1.0. Discovery gate `GetStage(MS04) >= 390`. Chemistry Station, `RecipeUtility`. Instructions in the item description for 0.1.

**Where things live:** concept (active) here in Rhodes; plan specs in `fo4-regalia-of-mystery/spec/`; Gemini brainstorm and old scratch copies in Alexandria `historical/regalia/`; verified xEdit/asset facts in Alexandria `memory/fo4-xedit-reference.md`.

**Open:** read component and perk FormIDs in xEdit; trace the sword's base damage; in-game tests (listed in the specs); item specs for Eye of Ra, Veil, Garb, Voice of Set. The concept retires when every item has a spec.

**Done 2026-11-23:** separate MO2 for Fallout 4 built with MO2-LINT; F4SE 0.7.9 loads and the game reaches the main menu; FO4Edit 4.1.5f (32-bit) loads Fallout4.esm and the DLC. Steps and gotchas are in `refs/steam-deck-mo2.md`.

**Next:** the xEdit lookups under Open (component and perk FormIDs, sword base damage), then build 0.1. Make a clean MO2 test profile first (untick the unmanaged third-party plugins).

**Checked:** `~/Repos/CLAUDE.md` (a symlink into Rhodes) does load when Claude starts from `~/Repos`.

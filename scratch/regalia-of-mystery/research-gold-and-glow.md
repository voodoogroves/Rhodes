# Research: gold tint and glow for the Blade of Bastet (2026-11-24)

Research only; nothing built or tested. Evidence is community forum posts and wikis (2015 to 2019 mostly), plus search snippets. Nexus blocks automated fetches, so three threads were read from text Chris pasted. **Everything here needs verifying in game.** Items marked *(unverified)* are one source or my inference.

## Verdict

Both are well-trodden. Gold = a **material swap** (MSWP) applied by the Blade's OMOD. Glow = **emittance** on that same material for a surface sheen; a **real light** is a separate, optional layer.

## 1. Gold tint

**Mechanism.** FO4 recolors weapons by swapping the `.bgsm` material. Many materials are *palette based*: a grayscale base texture plus a palette `.dds` (a strip of colors), where a **color remapping index** picks where on the strip to read. Like a Photoshop gradient map. Examples to inspect: baseball-bat paint OMODs use `PaintedBatLookup.dds`; hair uses `HairColor_LGrad_d.dds` (hardcoded, can't redirect).

**How the palette works (Kutsumiya, 2016, tested on combat armor; the best source so far).** The palette is a look-up table (LUT):
- **Horizontal axis = the diffuse map's gray value.** 128 px wide = gray 0 to 127 (256 px wide also works, as in Custom Combat and Synth Armor). Each part of the model (on combat armor: pouch, armor, belt, buttons) sits in its own gray range, so the palette recolors parts independently. For the sword, the blade, guard and grip will each sit in their own gray range; look at the diffuse map to see which.
- **Vertical axis = which palette row, chosen by the color remapping index** (a float, 0 to 1; the last row is 1). Vanilla is 64 rows with seven material "bands" stacked. Only **one pixel row** per band is actually read (the rest is padding; he expects even a 128x7 palette to work if the indices are calculated right, *unconfirmed*). Observed: index 0.18 = row 11, 0.33 = 21, 0.5 = 31, 0.66 = 42, 0.82 = 52, 1.0 = 63. That is roughly `row = index x (height - 1)`; so for our own palette, **pick the row, then compute the index**.
- **Index lives on the OMOD** (the `ColorRemappingIndex` property), which works. **An index set only inside a Material Swap did not work**: the game read row 0 instead (this is the "rusty Brotherhood combat armor" bug). Fix that worked: put the index on the OMOD too. For the Blade: set the index on our OMOD, not only in the swap.
- **Palette file format: uncompressed 32-bit A8R8G8B8, no DXT/BC.** He says it will not work properly otherwise (reason unknown).
- Making a new palette is the recommended way for a new color; he warns that stretching the vanilla one means editing vanilla OMOD indices and conflicts easily.
- **NifSkope always shows row 0** (it can't compute the index), so its preview is wrong for palette materials; judge in game.
- Experiment pattern he used: paint one 1-px row a loud color, point the index at it, and see what turns that color (a good way to verify mapping). Related article he wrote, not read: a Minutemen blue combat-armor palette ("super easy").

**Two routes, cheapest first.**
1. **Reuse a vanilla gold.** Our own checkpoint already flags this: check whether the weapon-material mods in the OMOD list (e.g. `Weapon_Material_Default` `0024A0D9`) offer a gold. If one does, point our swap at it; no new assets.
2. **New material.** Copy the blade's `.bgsm`, tint it, register it as an MSWP.
   - If the blade material is palette based: either pick a gold spot on the existing palette and set the index, or make a new, differently named palette `.dds` with a gold strip and point the new `.bgsm` at it.
   - If not: tint or retexture the copy directly.

**Gold as a palette.** A gold LUT is a gradient from dark gold (left, gray 0) to bright gold (right, gray 127), on the row the index points at. If the blade's material is palette based, that is all that is needed besides the `.bgsm` pointing at the new palette.

**Applying it.** An OMOD property `pwMaterialSwaps` with **ADD** (or SET); and the color index on the OMOD itself (see above). A forum case where the swap seemed to do nothing was a property set to **REM**, so the swap never applied. Because our OMOD already is the Blade's own mod, this fits the build: the swap rides on our OMOD. One guide suggests two swaps (a default and a recolor) so the original can be restored; not needed for us, since the Blade is its own weapon.

**Also noted.** A forum author found each new color needed roughly 3 OMODs for weapon paints; that was for a multi-color variety mod, not a single fixed gold. Color index can also be overridden per placed reference (for statics), not relevant to a held weapon.

**Not established.** Whether a swapped `.bgsm` needs its own palette or the original's persists *(one forum data point suggests the original's can persist)*. The index-to-row mapping is now answered above, but from one author's combat-armor tests, not the sword.

## 2. Glow

Two separate things; people conflate them.

**Surface glow (the sheen).** Set in the `.bgsm` (the NIF's own emissive values are **ignored** when the mesh points at a material file):
- enable Emittance; set the emittance color (gold) and multiplier (glow brightness). Start modest.
- Glowmap checkbox + a glow map restricts the glow to parts of the blade; without one the whole surface glows. Save glow maps DXT1 with mipmaps.
- Pitfalls: `bEnvironmentMapping` on can make the glow map ignored (turn it off); visual distortion with a bgsm plus glow map was fixed by disabling the vanilla normal map; a NIF with a TextureSet plus an injected bgsm can fail silently; editing a shared vanilla `.bgsm` affects every mesh using it (so copy it).
- A glow does **not** light surroundings; it only haloes the mesh.

**Real light (optional, and the more fiddly).** It is **not** the NiPointLight in the NIF (people edited those in 2016 without effect). *(One 2017 source, unverified:)* the NIF carries an **AddOnNode** with an index; that index points to an AddOnNode record in the Creation Kit (Special Effects > AddOnNode), which points to a **Light** record (World Object > Light) where color and intensity are set. Use a vanilla light or make a gold one. Risks: the index is shared across mods and a clash causes lighting conflicts (a community list of claimed indexes: https://www.nexusmods.com/fallout4/mods/16497/); and the sword's NIF would need the node (unknown whether it has one).

**Effect mesh (a halo or aura).** A separate shape with a BSEffectShaderProperty and a `.bgem` material, as plasma and fire weapons do. Reference mods to open in NifSkope: a Plasma Sword mod, a glowing power-fist mod, a Shishkebab glow thread. Not researched further; only if the sheen isn't enough.

## What the sword's own files say (read from the vanilla archives, 2026-11-24)

Extracted with `baunpack` (see `refs/fo4-archives.md`). These replace guesses.

- **The plain blade** `meshes/weapons/chineseofficersword/blade.nif` (and `_1`, the first-person copy) uses one material: `Materials\Weapons\ChineseOfficerSword\ChineseOfficerSword01A.BGSM`. **That exact path is the swap's Original Material.** The serrated blade uses `...\Serrated.BGSM`; the shock variants add `Weapons\RocketHammer\Mod_Stunpack.BGSM` (the stun pack component, a normal material, not a glow).
- **Not palette based.** No sword material lists a greyscale (palette) texture; each is just diffuse, normal and specular maps plus a cubemap plus the template `template/WeaponMetalTemplate_Wet.bgsm`. **The palette/index route is out for this sword.** Gold has to come from a new diffuse texture (as in the 44 Gold Magnum mod), or from a cubemap trick below.
- **The hilt mesh** (`chineseofficersword01.nif`) uses *both* `...01A` and `...01B`. 01A and 01B are identical except the cubemap: 01A uses `mipblur_DefaultOutside1.dds` (neutral), 01B uses `Shared/Cubemaps/Bronze_e.dds` (bronze). Both use the same textures `ChineseOfficerSword01_d/n/s.dds` (the blade and hilt share one texture set). So a swap on 01A inside a blade-only mesh leaves the hilt alone.
- **Cubemap idea (unverified, cheap).** A swap from 01A to 01B tints the blade's reflections bronze with no new textures; and vanilla has more warm cubemaps (`metalbrushedbronze01cube_e`, `mipblur_outsidebronze`) and a gold-ish one is plausible. Reflection tint is not a gold diffuse, so it may read as bronze steel, not gold. Worth one in-game test since 01B already exists.
- **Vanilla gold materials exist** (e.g. `vault111/v111ducts02gold`, `props/gildedgrasshopper`, `cryogun/cryogunbrass`), but each uses its own textures laid out for another mesh, so swapping one onto the sword puts the wrong texture on the sword's UVs. They show what a gold material file looks like; they are not drop-in.
- **No vanilla glow on this sword.** The shock blade is geometry plus normal materials, with no effect shader and no emissive on the strings I read. So there is no in-sword example to copy; glow stays the `.bgsm` emittance / `.bgem` overlay work described above.
- **Our current Blade** uses the serrated blade model, so its blade material is `Serrated.BGSM`; if the build session moves to the plain blade (the mundane Blade idea), the target is `01A`.

## Suggested path for the build session

1. ~~Find the blade's `.bgsm`; check for a palette.~~ Done: `ChineseOfficerSword01A.BGSM`, not palette based.
2. Test the cheap trick first: swap 01A to the existing 01B (bronze cubemap) via an MSWP, in game. Also look at `Weapon_Material_Default` and its siblings (xEdit) for an existing gold.
3. For a real gold: paint a gold diffuse (`ChineseOfficerSword01_d.dds` is shared by blade and hilt; save our own copy), write a small `.bgsm` that points at it with the same template, and swap to that. Emittance on that `.bgsm` adds the glow. The `.bgsm` is ~450 bytes; the `.bgsm` question is how to write it (script, or the Material Editor under Proton).
4. Create the MSWP; add it to our OMOD with `pwMaterialSwaps` **ADD**; verify in game.
5. Consider the real light only after the sheen is judged.

## Open checks

- ~~Is the blade material palette based?~~ No (see above).
- Does the 01A to 01B swap look gold enough in game?
- Does the sword NIF already have an AddOnNode?
- **Tooling on the Deck is unresolved.** The sources all assume a `.bgsm` editor. The one named is the Fallout 4 Material Editor by ousnius (a Windows tool; a Nexus mod) *(unverified; I haven't confirmed it runs under Proton or MO2 here)*. The Creation Kit also has a material editor of some kind *(unverified)*. `.bgsm` is a binary format, documented at https://www.fo4docs.org/File%20Formats/Assets/Textures%20and%20Materials/ , so a script could read or write it if no editor runs. If xEdit can reach everything except the `.bgsm` contents themselves (the MSWP, OMOD and records are all xEdit work), the editor is only needed for the material file.
- Is the blade's gray range separate from the guard and grip (so a gold palette can recolor only the blade)? Read the sword's diffuse map.
- The two Japanese palette guides are now read (translated PDFs from Chris, text and screenshots): http://f4mod.hatenablog.com/entry/textures/Color_Palette_1 and ..._2. Unread: his Minutemen palette article (a start-to-finish new palette).

## Sources

Community, mostly 2015 to 2019; verify against the current game.
- Creation Kit wiki: [Material Swap](https://falloutck.uesp.net/w/index.php?title=Material_Swap&mobileaction=toggle_view_desktop), [Object Mod](https://falloutck.uesp.net/wiki/Object_Mod) (`fColorRemappingIndex`, `pwMaterialSwaps`).
- [Simple material swap guide](https://chiaroscorner.wordpress.com/2018/10/01/how-to-do-a-simple-material-swap-in-the-fallout4-creation-kit/) and [FO4Edit material swap tutorial](https://www.modsfallout4.com/material-swap-mod-tutorial-fo4edit-tips-by-dm/).
- [fo4docs: Textures and Materials](https://www.fo4docs.org/File%20Formats/Assets/Textures%20and%20Materials/) and [Bethesda Modding Library](https://baddogskyrim.github.io/BethesdaLibrary/file-formats/textures-materials/) (emittance fields, NIF values overridden by material).
- Kutsumiya, Fallout Sandbox DIY (read via Chris's translated PDFs): [Investigating the structure of the color palette](http://f4mod.hatenablog.com/entry/textures/Color_Palette_1) and [Changing the palette and correcting the BoS combat armor](http://f4mod.hatenablog.com/entry/textures/Color_Palette_2), both 2016-09-24.
- Nexus threads (read via pasted text): [Changing weapon luminance/glow](https://forums.nexusmods.com/topic/3562285-changing-weapon-luminanceglow) (2015 to 2017), [Material swaps and grayscale](https://forums.nexusmods.com/topic/7273116-question-regarding-material-swaps-and-grayscale) (2018), [Color remapping index](https://forums.nexusmods.com/topic/4839060-color-remapping-index) (2016).
- Search snippets only (pages not read): [Shishkebab glow](https://forums.nexusmods.com/topic/3915231-shishkebab-glow-color-assistance), [Glow maps don't work](https://forums.nexusmods.com/topic/9766568-glow-maps-dont-work), [Retexture of weapons and material editing](https://www.nexusmods.com/fallout4/mods/27574).

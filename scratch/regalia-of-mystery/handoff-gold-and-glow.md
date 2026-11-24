# Handoff: gold tint and glow for the Blade of Bastet

From: the research session (read-only; no mod, plugin or game file was changed). To: the session that builds the mod.

Full detail and sources: `Rhodes/scratch/regalia-of-mystery/research-gold-and-glow.md`. Archive tool: `Rhodes/refs/fo4-archives.md`. Everything below marked *(unverified)* has not been seen in game.

## What is established (read from the vanilla archives)

- The plain blade `meshes/weapons/chineseofficersword/blade.nif` uses exactly one material: `Materials\Weapons\ChineseOfficerSword\ChineseOfficerSword01A.BGSM`. This is the swap's **Original Material**. The serrated blade uses `...\Serrated.BGSM`. Our test Blade currently uses the serrated model, so its target is Serrated unless we move to the plain blade.
- The sword's materials are **not palette based** (no greyscale texture). The color-remapping-index route does not apply to this sword.
- `ChineseOfficerSword01B.BGSM` already exists and is identical to 01A except its cubemap is `Shared/Cubemaps/Bronze_e.dds` (bronze reflections) instead of `mipblur_DefaultOutside1.dds`. The hilt mesh uses both.
- Blade and hilt share one texture set: `Weapons/ChineseOfficerSword/ChineseOfficerSword01_d/_n/_s.dds`.
- There is no vanilla glow on this sword (the shock blade is geometry with normal materials).
- Vanilla gold materials exist elsewhere but use textures for other meshes; not drop-in.

## How a recolor is applied (CK wiki and forum sources, 2015 to 2019)

1. Create a Material Swap record (MSWP): Original Material = the path above; Replacement Material = the new `.bgsm`.
2. On our OMOD, add property **`pwMaterialSwaps` with ADD** (or SET), pointing at that MSWP. A forum case where a swap did nothing was the operation set to **REM**.
3. A material swap only does something if a form uses it; the OMOD is that form. A swap on the blade OMOD's model should not touch the hilt (the hilt is the weapon record's model).

## Suggested order

1. **Cheapest test, pure xEdit:** MSWP from 01A to the existing **01B** (bronze cubemap). No new files. Judge in game whether it reads gold enough *(unverified; may read as bronze steel)*. Also check the `Weapon_Material_*` OMODs (e.g. `Weapon_Material_Default` `0024A0D9`) for an existing gold.
2. **Real gold:** paint a gold diffuse (a new file under our own path, e.g. `Textures/Weapons/BladeOfBastet/`), and write a small `.bgsm` (about 450 bytes) with the same template `template/WeaponMetalTemplate_Wet.bgsm`, the same normal and specular maps, and our diffuse; swap to it as above. The shine comes from the specular map and the cubemap, so a flat gold diffuse alone may look like yellow paint. A worked example of this approach: the "44 GOLD MAGNUM" mod in Downloads (loose retexture: new `_d/_n/_s` plus five tiny `.bgsm` files; it overwrites vanilla paths, which we must not do; use our own paths and a swap).
3. **Glow (surface sheen):** in that `.bgsm`, enable Emittance, set the color (gold) and a modest multiplier; optionally a glow map. Pitfalls: with environment mapping on, a glow map can be ignored; if the mesh points at a material file, the NIF's own emissive values are ignored (edit the material); distortion fixed by disabling the vanilla normal map (one report).
4. **Real light (optional, later):** a Light record plus an AddOnNode record, with the NIF carrying an AddOnNode index; indexes are shared across mods (conflicts). Needs a NIF edit. One 2017 source *(unverified)*.

## Open items for you

- **Writing the `.bgsm`:** no editor is set up on the Deck. Options: a small script (the format is documented at fo4docs.org and the file is tiny); the Fallout 4 Material Editor (ousnius) under Proton *(unverified it runs)*; or xEdit if the swap and OMOD are all that is needed (the `.bgsm` contents are not xEdit work).
- Verify in game: the 01B swap result; whether the swap leaves the hilt alone; whether emittance shows.
- `baunpack` (installed at `~/.local/bin/baunpack`, build script in Rhodes `scripts/fo76utils/`) can list and extract any vanilla material or mesh for comparison.
- Review the license of anything reused from third-party mods; use them as reference only.

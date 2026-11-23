# Concept spec: Order of Mysteries Regalia & Arsenal

*Location: Rhodes `scratch/regalia-of-mystery/` while we plan; published to `fo4-regalia-of-mystery` once firm.*

*Status: DRAFT for agreement. Intent only. No FormIDs, condition numbers, record types or numbers; those belong in `plan-spec.md`. Source material: `gemini-brainstorming.md`.*

## What this is

A Fallout 4 mod that brings the Fallout 76 **Order of Mysteries** set into the Commonwealth as a small espionage/assassin loadout, tuned for Survival Mode.

## Intent

- **A coherent set, not a bag of items.** Each piece is decent on its own; Eye of Ra makes the others stronger when worn.
- **Theme over raw power.** A run dressed as the Mistress of Mysteries should be viable and fun, and the gear shouldn't feel like a mistake next to Throatslicer, The Deliverer, the Problem Solver, Splattercannon, Pickman's Blade, a wounding minigun or Spray and Pray. It doesn't need to match them; being thematically strong is the point.
- **A stealth-and-control fantasy.** Quiet approach, hazard and disease resilience, talking your way past trouble, disrupting a fight rather than winning it by damage.
- **Earned, not handed over.** The set is discovered through the Silver Shroud storyline and built by converting ordinary items the player already carries.
- **Fits the vanilla game.** It should feel like it was always in FO4: same workbenches, same upgrade habits, vanilla look.

## The set (what, not how)

| Piece | Role | Fantasy |
|---|---|---|
| Garb of Mysteries | Outfit | Armored, discreet; a sneaking outfit |
| Veil of Secrets | Face piece | Hazard and disease protection; social edge |
| Eye of Ra | Amulet / catalyst | The piece that makes the others stronger |
| Blade of Bastet | Melee | A ceremonial blade that ignores armor |
| Voice of Set | Sidearm | A revolver that disrupts groups instead of killing them |

## Staging

- **v1:** one item, end to end, to prove the pipeline.
- **v2:** the Veil plus one more item.
- Later versions add the rest.

Each stage must be useful and installable on its own.

## Constraints (these are intent, not detail)

1. **Vanilla assets only.** No new meshes, textures or materials.
2. **Light and simple to install.** A single light plugin, no scripts, no archives.
3. **Doesn't touch vanilla.** No changes to existing records; coexists with major gameplay overhauls.
4. **Works on Steam Deck** through Mod Organizer 2 and xEdit.
5. **Baseline is Anniversary Edition plus all DLC.** Using DLC or Creation Club assets is fine, but each use is called out in the plan-spec (it makes that DLC a hard requirement).

## Decided

- Each piece is decent standalone; Eye of Ra amplifies the others (replaces former Q1).
- Power level: viable, not competitive with top legendaries; theme is the priority (replaces former Q4).
- **v1 is the Blade of Bastet.**
- Male characters can wear the dress (the Fallout wiki shows men in the vanilla dresses on the same rig), so no separate male outfit is planned; confirm in-game.
- The look is the **Mistress** of Mysteries (there is no male counterpart in the lore). Eye of Ra is a neck-clasped piece with green fabric, the green being the costume's colour accent; revisit only if a better neck piece turns up when we check assets.
- **Discovery gate: the Silver Shroud costume** (item or quest stage), because it needs no vanilla edits. Players who skip that quest won't see the recipes; accepted.
- Phantom Device is cut. Staging is v1 = one item, v2 = Veil plus one more.

## References (not decisions)

- **Cape body colour:** the Institute division-head uniform green (`Materials\Clothes\InstituteUniform\InstUniformMDH_green.BGSM` / `FDH`), a medium leaf green (about rgb 83,132,88 where green). Reference only. A material swap replaces the whole texture, and the cape's texture layout (UVs) differs from the uniform's, so the real result must be checked in-game before we commit to it.
- **Cape and brooch:** the Maxson cape (`FCapeMaxon.nif` / `MCapeMaxon.nif`) uses one material and one texture holding the red cloth and the dark metal clasp plates together. A swap cannot change the clasp or symbol on its own.

- **UCO (Unified Clothing Overhaul), checked against its plugin:** `ClothesUCOCape` makes the vanilla Maxson cape a standalone wearable on slot 54, using the same vanilla meshes (`FCapeMaxon` / `MCapeMaxon`) and the same single texture; it adds no cape art. `ClothesUCOScarf` sits on the neck slot (50) and uses the vanilla `Armor\Metal\MScarf.nif`; UCO ships no scarf or cape textures. So a standalone cape is proven workable, and slot choice for Eye of Ra matters for UCO users (50 and 54 are both taken by UCO items).
- **Round symbol:** the round disc on the cape's texture, lower right, in the same image as the cloth. Cannot be replaced on its own by a swap.

## Open questions

1. **Eye of Ra form.** Either a visible green cape (a free slot, with the swap and UV caveats above), or a **non-visible** worn item that only carries the catalyst effect, shown as the Silver Locket in the inventory, like a ring but on the neck slot. The invisible option avoids the cape's texture and slot problems; the cost is that you never see it on the character.

## Out of scope (for now)

Phantom Device (cut), custom art, new quests or voice, FO76 upgrade tiers, scripted effects, compatibility patches for specific overhauls.

## Next

Agree this file, then write `plan-spec.md` (mechanics, records, recipes), verified against the xEdit definitions in Alexandria.

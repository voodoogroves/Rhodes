# Concept spec: Order of Mysteries Regalia & Arsenal

*Location: Rhodes `scratch/regalia-of-mystery/` while we plan; published to `fo4-regalia-of-mystery` once firm.*

*Status: DRAFT for agreement. Intent only. No FormIDs, condition numbers, record types or numbers; those belong in `plan-spec.md`. Source material: `gemini-brainstorming.md`.*

## What this is

A Fallout 4 mod that brings the Fallout 76 **Order of Mysteries** set into the Commonwealth as a small espionage/assassin loadout, tuned for Survival Mode.

## Intent

- **A coherent set, not a bag of items.** Wearing the pieces together should feel different from wearing them apart.
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

## Open questions (we need to agree on these)

1. **Eye of Ra and standalone pieces.** Should each piece be good on its own, with Eye of Ra as an optional booster added later? Or should the pieces only really shine together?
2. **Which item is v1?**
3. **Discovery gate.** Is the Silver Shroud costume the right trigger? Too early, too late, or a nuisance for players who skip that quest?
4. **Power level.** Where does this sit against vanilla legendaries and common overhauls: a clear side-grade, or a strong specialist build?
5. **Eye of Ra visual.** The brainstorm uses a cape mesh for an "amulet". Is that what we want to see on the character?
6. **Female and male looks.** Same outfit both ways, or an accepted different look per gender?

## Out of scope (for now)

Phantom Device (cut), custom art, new quests or voice, FO76 upgrade tiers, scripted effects, compatibility patches for specific overhauls.

## Next

Agree this file, then write `plan-spec.md` (mechanics, records, recipes), verified against the xEdit definitions in Alexandria.

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

## Decided

- Each piece is decent standalone; Eye of Ra amplifies the others (replaces former Q1).
- Power level: viable, not competitive with top legendaries; theme is the priority (replaces former Q4).
- Phantom Device is cut. Staging is v1 = one item, v2 = Veil plus one more.

## Open questions (we need to agree on these)

1. **Which item is v1?** (Suggestion: Blade of Bastet, the simplest to build end to end.)
2. **Discovery gate.** Is the Silver Shroud costume the right trigger? Too early, too late, or a nuisance for players who skip that quest?
3. **Eye of Ra visual.** The brainstorm uses a cape mesh for an "amulet". Is that what we want to see on the character?
4. **Female and male looks.** Same outfit both ways, or an accepted different look per gender?

## Out of scope (for now)

Phantom Device (cut), custom art, new quests or voice, FO76 upgrade tiers, scripted effects, compatibility patches for specific overhauls.

## Next

Agree this file, then write `plan-spec.md` (mechanics, records, recipes), verified against the xEdit definitions in Alexandria.

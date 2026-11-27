# Handoff: outfits
Updated: 2026-11-27, from VS Code on Steam Deck

## State

FO4 outfit fitting and kitbashing. The vanilla Vault 111 suit (female, third person) now has a defined version that was called **good enough**. Seen in offline renders only, never in game.

**Direction:** respect the vanilla body. The goal is more definition, not a bigger or different shape. The stronger and wider-hip variants were offered and not taken.

**Method** (inspired by Femshepping's unzipped suit; none of their geometry is used): split every triangle into four, hug the cloth toward the body, then add soft shaping (mostly the back).

| Script (`scripts/nif/`) | Does |
|---|---|
| `subdivide.py` | splits triangles so there is room for detail |
| `fitbody.py` | `measure`, `push` (out of the body), `hug` (toward it) |
| `sculpt.py` | adds definition at fixed places on a female outfit; defaults are the accepted version |

All three are **not yet committed**.

**Rebuild** (matched the accepted model byte for byte on 2026-11-27). Extract with `baunpack`, each archive into its own new empty folder outside the repo:

- from `Fallout4 - Meshes.ba2`: `characterassets/femalebody.nif` (vanilla body, `V`) and `clothes/vault111suit/femalevault111suit.nif` (suit)
- from `evbunderwear - main.ba2`: `characterassets/femalebody.nif` (the installed body replacer, `E`)

```
python3 subdivide.py suit.nif sub.nif
python3 fitbody.py hug E sub.nif hug.nif --ref V --offset 0.2 --keep 0.2 --smooth 1 --above=-105 --carry 1100
python3 sculpt.py hug.nif defined.nif
```

**Files on this machine** (game-derived, never commit):

- `~/Downloads/Outfit-Work/`: `vault111suit-defined.nif` (accepted), `vault111suit-hug-only.nif` (before shaping), `rear.py` (renders two models from behind with smooth shading: `rear.py OUT.png A.nif B.nif`)
- `~/Downloads/Outfit-Renders/`: pictures; the last comparisons are `rear-old-vs-new.png` and `torso-shaped.png`
- `~/Downloads/Prudy-VanillaFit-test.zip`: Prudy's dark suit pushed out to the vanilla shape (separate trial, personal use, untested in game)

## Next

Package the defined suit as its own outfit (own mesh path, never the vanilla one; needs a plugin) and look at it in game, standing and moving.

## Open questions

- Commit the three scripts and this note to `dev`?
- Spike at the zipper pull under the collar (from `--carry`): fix before or after the in-game look?
- Same steps on the Institute uniform? Is that the "Institute jumpsuit" meant? An earlier hug-only trial exists in pictures.
- Prudy zip in game: Test profile, enable Prudy, install the zip below it, `help "Prudy" 4 ARMO`.
- Later: first-person and male versions; combining pieces (idea: Prudy gloves on the True Vanilla suit; separate glove items may clash with hand slots, untested).
- Release would need a decision on shipping reshaped vanilla meshes; other modders' pieces need their permission.
- An Alexandria `fo4-mod` note on outfit meshes, proposed once something is confirmed in game.

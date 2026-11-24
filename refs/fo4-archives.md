# Reading Fallout 4 archives (BA2) on the Deck

**Tool: `baunpack` from [fo76utils](https://github.com/fo76utils/fo76utils)** (MIT, C++, native Linux). Verified 2026-11-24: lists and extracts from `Fallout4 - Materials.ba2` and `Fallout4 - Meshes.ba2`; lists `Fallout4 - Textures*.ba2` (texture extraction not tried).

Build and install (once): `~/Repos/Rhodes/scripts/fo76utils/build-baunpack.sh`. It clones to `~/Repos/upstream/fo76utils` if missing and puts `baunpack` in `~/.local/bin` (not on PATH in an assistant's shell; use the full path). Built against upstream commit `c52da18`; no scons needed.

```
D=~/.local/share/Steam/steamapps/common/"Fallout 4"/Data
baunpack "$D/Fallout4 - Materials.ba2" --list chineseofficer          # list by name pattern
baunpack "$D/Fallout4 - Meshes.ba2" -- chineseofficersword/           # extract into the current directory
```

- Extraction writes the archive paths under the **current directory**; run it from a fresh empty directory, never from the game folder.
- Patterns are substrings, matched case-insensitively against the archive path. Archives listed first win on duplicates.
- Materials (`.bgsm`/`.bgem`) are small binaries; `strings -n 4 file.bgsm` shows the texture paths, cubemap and template they use. Meshes: `strings` shows shader and material paths too. fo76utils also has `bgsmfile.cpp`, `nif_info.cpp` and `esmdump.cpp` (not built) if real parsing is needed.
- The vanilla archives hold *only vanilla*. Creation Club content is in `Data/cc*` and DLC `.ba2`s; list them the same way.
## Reading records (ESM/ESP) without xEdit's GUI

- **`esmdump`** (also fo76utils): build with `~/Repos/Rhodes/scripts/fo76utils/build-esmdump.sh` (about 12 seconds). Lists records as text, e.g. `esmdump "$D/Fallout4.esm" "$D/Fallout4 - Interface.ba2" -i BOOK -edid -n -o book.txt` (`-i TYPE` filters, `-edid` resolves form IDs to names, `-n` drops the stats; the `.ba2` argument supplies localized strings). **It prints only the fields it knows**: BOOK's `DATA`/`DNAM` and `MODS` are missing, for example. Use `-v` for a few more.
- **`esmrec.py`** (ours, `scripts/fo76utils/esmrec.py`, standard-library Python): prints *every* raw subrecord of chosen records by form ID or EditorID, e.g. `python3 -I esmrec.py "$D/Fallout4.esm" BOOK 8E74A` or `... STAT HighPoly_Grognak10`. Walks all of `Fallout4.esm` in about 1.6 seconds. Fields come out as hex, so layouts must be decoded by hand (compare against `Rhodes/scratch/fo4-magazines.md` for an example). Localized `FULL`/`DESC` show as 4-byte string IDs.
- Resolving a form ID to a name: dump the type with `esmdump -i TYPE -edid` and grep the ID.
- Both read only; they never write the plugin.

## Other tools

- Other prior art found, not used: the xEdit 4.1.5f archive ships a Windows `BSArch` (see `steam-deck-mo2.md`); B.A.E. and Archive2 (Windows); a Linux C rewrite of BSArch at github.com/sableeyed/BSArch.

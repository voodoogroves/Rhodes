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
- Other prior art found, not used: the xEdit 4.1.5f archive ships a Windows `BSArch` (see `steam-deck-mo2.md`); B.A.E. and Archive2 (Windows); a Linux C rewrite of BSArch at github.com/sableeyed/BSArch.

# Steam Deck: Mod Organizer 2 setup

Runbook for rebuilding the modding setup on a new or reset Steam Deck. Lives in Rhodes because it applies across projects (`fo4-pax`, `fo4-regalia-of-mystery`).

**Status (2026-11-23):** the Fallout 4 instance was built from this runbook and reached the main menu through F4SE. Everything under "Per game" is verified. Open items are at the bottom. Facts from upstream docs that haven't been run here are marked *(upstream)*.

## The model

One independent MO2 instance per game, built by **MO2-LINT** (`~/Repos/upstream/modorganizer2-linux-installer`, docs at docs.furglitch.com/modorganizer2-linux-installer). It installs MO2 into a normal folder, puts `mo2-redirector.exe` in the game folder, and registers a Steam compatibility tool for the game (`mo2_<appid>_redirector`, so `mo2_377160_redirector` for Fallout 4). You set the **game's own Steam entry** to that tool. Launching the game from Steam then opens MO2, and the game is started from MO2's top-right dropdown (F4SE, Fallout 4, ...). It appears in gaming mode like any Steam game.

Never launch the game any other way (plain Steam without the tool, or Wine directly). That can break the prefix.

## Prerequisites

1. Desktop mode, and a real terminal (Konsole). The installer's menus need a TTY, so an assistant's shell can't run `install` (it aborts with "Input is not a terminal").
2. **Proton 11.0** installed in Steam. It's the only version upstream supports.
3. The game installed and **launched once to the main menu**, so Steam creates its prefix (`compatdata/<appid>/pfx`).
4. At least one other game or shortcut left on the stock Proton, or Steam may remove it and break the MO2 tool.

## Install the installer

1. Download the `mo2-lint` release binary (v7.0.0+) from the GitHub releases page.
2. `chmod +x mo2-lint`, then move it to `~/.local/bin/` (already on PATH).
3. Config is created at `~/.config/mo2-lint/settings.toml`. Defaults put instances under `~/Games/mo2-lint/mo2-{game}-{launcher}`. State is `~/.config/mo2-lint/state.json`; logs are `~/.cache/mo2-lint/logs/`.
4. v7.0.0 worked, though 7.0.5 was out. If something fails, update the binary first.

## Per game

```bash
mo2-lint install --help                      # find the exact game id
mo2-lint install fallout4 ~/Games/mo2-lint/mo2-fallout4-steam -L steam -s
```

`-s` installs the script extender (F4SE for Fallout 4). The prompts, in order:

1. **"Have you set the compatibility tool?"** Answer **y**. The tool doesn't exist yet at this point; it appears only after the install. The prefix just needs to exist.
2. **Script extender version.** F4SE must match the game's exact version. Read it first:
   ```bash
   python3 -I -c 'd=open("Fallout4.exe","rb").read();i=d.find("FileVersion".encode("utf-16le"));print(d[i:i+100].decode("utf-16le","ignore"))'
   ```
   (run from the game folder `~/.local/share/Steam/steamapps/common/Fallout 4`). On 2026-11-23 the game was 1.11.240.0, which is **F4SE 0.7.9**. Menu entries list the runtime they need.
3. **Menus use arrow keys and Enter.** Typing a number does nothing visible and selects the highlighted entry. Check the highlight before pressing Enter.

Then in Steam: Fallout 4 **Properties → Compatibility → force a specific tool → `mo2_377160_redirector`**. Launch the game from Steam; MO2 opens.

### MO2 first run

- **Nexus categories:** choose Nexus categories (cosmetic; changeable in Settings → Categories).
- **nxm links:** yes. Only one program owns `nxm://` at a time, so if you ever run more than one MO2 on the Deck, the most recent registration wins. The "Mod Manager Download" button is untested here.
- **Unmanaged entries** in the mod list are normal: base game, DLC, Creation Club, and anything installed from the in-game menu live in the game's `Data` folder. See "Unmanaged mods".

### Verify F4SE

Pick **F4SE** in MO2's dropdown and Run. Get to the main menu, then quit. Then check the logs:

`~/.local/share/Steam/steamapps/compatdata/377160/pfx/drive_c/users/steamuser/Documents/My Games/Fallout4/F4SE/`

- `f4se.log` should show `F4SE runtime: initialize (version = 0.7.9 ...)` and end at `init complete` / `RegisterPapyrusFunctions_Hook`.
- `f4se_loader.log` ends at `launching`. `WinVerifyTrust ... 80090008` lines are normal under Wine; ignore them.
- The log is in the **prefix's Documents**, not MO2's `overwrite` folder.

Verified 2026-11-23: F4SE 0.7.9 loaded and the game reached the main menu with about 85 plugins in the load order.

### Recovery: wrong F4SE version (or any bad install)

Don't re-run `install` over it (the first run had already completed; a second one hits a non-empty folder). Run:

```bash
mo2-lint uninstall -g fallout4
```

It removes the redirector, the Steam wrapper, the launch option, and every tracked F4SE file. Verified clean on 2026-11-23: no leftover `f4se_1_10_163.dll`. Then install again.

## FO4Edit (xEdit)

**Source:** the official `TES5Edit/TES5Edit` GitHub releases page (xEdit is one project; FO4Edit is its Fallout build). No Nexus account needed. Latest release on 2026-11-23 was **xEdit 4.1.5f** (2024-04-28).

How it was fetched and installed (2026-11-23):

```bash
# list releases
curl -s https://api.github.com/repos/TES5Edit/TES5Edit/releases?per_page=4
# download into a scratch dir, then hash
curl -sSL -o xEdit.4.1.5f.7z https://github.com/TES5Edit/TES5Edit/releases/download/xedit-4.1.5f/xEdit.4.1.5f.7z
sha256sum xEdit.4.1.5f.7z
# extract into a new empty folder (bsdtar reads .7z; no 7z needed)
mkdir -p ~/Games/mo2-lint/tools/xEdit-4.1.5f
bsdtar -xf xEdit.4.1.5f.7z -C ~/Games/mo2-lint/tools/xEdit-4.1.5f
# FO4 build: copy the 64-bit Fallout exe under a name xEdit recognises
cd ~/Games/mo2-lint/tools/xEdit-4.1.5f && cp xFOEdit64.exe FO4Edit64.exe
```

- Size 31,345,110 bytes (matches the GitHub release metadata); SHA-256 `54c014da621f83f06a64fd92ddb8e32ed3082d1c65f543dc1c4e432130dced08`. GitHub published no digest to compare against, so the hash is a record, not a verification.
- The archive holds `xFOEdit64.exe`/`xFOEdit.exe` (Fallout), plus TES/SF/Dump builds, BSArch and `Edit Scripts/`. There is no file called FO4Edit in it.
- **Game selection:** xEdit takes the game from a `-FO4` command-line switch or from an exe name containing `fo4` (read from `xEdit/xeInit.pas` on current master, not from the 4.1.5f binary). A copy named `FO4Edit64.exe` needs no arguments. Alternative: keep `xFOEdit64.exe` and pass `-FO4`.
- Use the 64-bit exe (`FO4Edit64.exe`); the 32-bit build is the usual cause of out-of-memory errors on big load orders (general xEdit knowledge, not checked here).

**Observed 2026-11-23 (Proton 11.0, MO2 2.5.2, xEdit 4.1.5f):**
- **Use the 32-bit `FO4Edit.exe`.** `FO4Edit64.exe` showed the "64-bit is slower" prompt, then died on startup with `Runtime error 216` (an access violation inside the exe; the Proton log showed a chain of faults at `FO4Edit64.exe+0x1C8EC4`). Cause not found. The 32-bit copy (`cp xFOEdit.exe FO4Edit.exe`) starts fine.
- **Click OK on the "Not implemented." box.** It appears right after "Loading active plugin list" and is non-fatal; xEdit carries on and opens. Expect a few splash screens (support/donation nags) too.
- **Pick the right exe in MO2.** The first attempt used `xFOEdit64.exe` (no `fo4` in the name, no `-FO4` switch), so xEdit couldn't tell the game. Use `FO4Edit.exe`.
- **Loading works.** The Module Selection list appears with every plugin ticked. For vanilla lookups, right-click → **Select None**, then tick only `Fallout4.esm` and the 6 `DLC*.esm`, and OK. Loading finished ("Background Loader: finished" in the message pane) with a stream of tip/donation screens to close along the way. Entries struck through in the list are in `Plugins.txt` but missing from `Data`; harmless.
- xEdit creates `FO4Edit Cache` and `FO4Edit Backups` folders inside the game's `Data` folder. Normal.
- To debug a crash, set the game's launch options to `PROTON_LOG=1 %command%`; the log lands at `~/steam-377160.log` and is overwritten each launch. Remove it afterwards (it is large and slows things).

**Running xEdit scripts without clicking (verified 2026-11-23).** xEdit can apply a script on startup from MO2's executable Arguments. The reusable tool is `scripts/xedit/Lookup.pas` in this repo: edit `~/Games/mo2-lint/tools/our-scripts/requests.txt` (`id`, `edid`, `list`, `file` and `npcstats` lines; see the script header), set the `FO4EDIT` executable's Arguments to:

```
-autoload -autoexit -script:"Z:\home\deck\Repos\Rhodes\scripts\xedit\Lookup.pas" -R:"Z:\home\deck\Games\mo2-lint\tools\our-scripts\xe.log" Fallout4.esm
```

Run it from MO2, click OK on the module list (it still appears) and the "Not implemented" box, and read `our-scripts/out.txt`. It takes seconds after loading.

- **Use home paths (`Z:\home\deck\...`) for everything.** xEdit runs inside Proton and cannot see `/tmp`; it will say "Could not open script" for a `/tmp` path. An assistant's shell in the VS Code Flatpak has a private `/tmp` too.
- After editing Arguments, re-open the gear to confirm it saved; a stale old line cost a retry.
- **Keep two executable entries:** `FO4EDIT` with empty Arguments for normal GUI use, and a second one (e.g. `FO4EDIT lookup`) with the script Arguments. If the script Arguments are left on the normal entry, opening FO4Edit runs the script and exits. (As of 2026-11-23 the single entry still has the script Arguments.)
- **Do not launch xEdit by running `proton run` from a shell.** It fails (no display authorisation) and rewrites Proton runtime files in the game's prefix.
- Reference ids are in Alexandria `memory/fo4-xedit-reference.md`.

Add it to MO2 (a GUI step; don't edit `ModOrganizer.ini` while MO2 is running): gear icon (Edit executables) → **+ → Add from file…** → `~/Games/mo2-lint/tools/xEdit-4.1.5f/FO4Edit64.exe`. Title `FO4Edit`. Run it from MO2 so it sees the virtual `Data` folder. Output files land in MO2's `overwrite` folder.

## Building a plugin with xEdit scripts (the Claude workflow)

Claude can build plugin records by writing an xEdit Pascal script; you click Run in MO2 and paste back the message pane (a screenshot works). Each round takes a minute or two. Prototype first, fix from the error text, commit when it proves out. The project's own scripts live in its repo (e.g. `fo4-regalia-of-mystery/build/xedit/BuildBlade.pas`); generic tools live here in `scripts/xedit/`.

Lessons (2026-11-23, xEdit 4.1.5f under Proton 11.0):
- **The binary is the authority, not the source.** The `TES5Edit` clone in `~/Repos/upstream` is the newer, unreleased `dev-4.1.6`; 4.1.5f lacks some functions it has. `AddNewFileName(name, light, medium)` is source-only: the binary says `Undeclared Identifier`. In 4.1.5f, `AddNewFile` takes no arguments and shows a "Filename without extension" box (type the name; it creates a `.esp`). An EJvInterpreterError in the message pane names the line and the problem ("Type mismatch", "Undeclared Identifier"); read that line first.
- **A new file has no masters.** Copying a record "as new" does not add masters, so references to vanilla records save against a master that does not exist (they show as `<Error: Could not be resolved>` and FormIDs come out with a stray `01`). Call `AddMasterIfMissing(file, 'Fallout4.esm')` right after creating the file. *Confirmed 2026-11-23: with the master added, every reference resolved and the saved plugin header carried the `MAST`.*
- **The plugin is only written if you accept xEdit's save prompt** when you close the window after "You can close this application now." If you close without saving, nothing is written. Don't re-run if the file is already there: the filename box then says "a file of that name already exists" (check `Data/` first; the file can appear a moment after you accept).
- **Check the saved file, not just the message pane.** A small Python read of the plugin header (`MAST` records) showed the missing master at once.
- **The new plugin is written into the game's real `Data` folder**, not MO2's `overwrite` (xEdit uses the `S:` drive path, which MO2's virtual folder doesn't intercept). Move it into an MO2 mod folder afterwards; delete a stale copy from `Data` before re-running a build script.
- **The ESL flag is a later step.** The prototype is a plain `.esp`.
- **Log every step** in the script and write a log file to a home path; one failing step then shows where it stopped.
- **An assistant can't see xEdit, MO2 or the game running.** `pgrep` from the VS Code Flatpak shell doesn't see processes inside Proton, so "nothing found" is not evidence that they're closed (2026-11-23: a plugin was judged "not saved" when xEdit was still open and saved a moment later). Ask the person whether they've closed everything, and check files by timestamp after they say so.

## Editing MO2 settings by file

MO2 rewrites `ModOrganizer.ini` when it exits, so edit it only with MO2 **closed** (back it up first). Executables are the numbered entries under `[customExecutables]`; bump `size=` when adding one. Typing into MO2's Edit Executables fields is error-prone (autocorrect once put a stray `v` in front of `-autoload`, and a mistyped `FO4Edit.exe` gave "not found"), so for long Arguments lines let Claude write the entry, then reopen MO2.

## Testing in game on the Deck

- **A clean Test profile plus a prepared save** (level 20, the perks needed, a few of the item under test) makes every test start from the same state. Local saves are on, so saves stay in the profile.
- **Console:** needs a keyboard (Bluetooth works); the tilde key opens it. The cheat terminal holotape is easier on a controller for god mode and spawning. Console text is small and `getav` readouts were unreliable here, so prefer a measure that needs no reading, such as counting swings to kill, or attach a screenshot to chat for the assistant to read.
- **Record stats do not always match spawned actors** (templates, level scaling). Check against the game, not just the xEdit record.
- For a before/after test of an effect, use a throwaway "TEST" plugin variant (different plugin name, editor IDs and item name) so the real plugin stays untouched; untick it afterwards.

## Unmanaged mods

MO2 lists plugins in the game's `Data` folder that aren't in a mod folder as "Unmanaged". On this Deck that's about 85 plugins:

- About 18 official: base game, 6 DLC, 10 Creation Club `cc*.esl`. Normal.
- The rest are third-party (Sim Settlements, Clothing Overhaul, SKK, Eli's mods, and so on), almost certainly from the in-game Mods menu. They load, but MO2 can't version or update them.

For mod development, use a separate **Test profile** with the third-party plugins disabled, leaving vanilla, DLC and CC. This doesn't touch the game folder. Don't delete the unmanaged mods: they're packed as BA2s named after their plugins (107 non-Bethesda archives; the only loose `Data` folders are F4SE's `Scripts`, `Video` and xEdit's cache), so unticking a plugin also stops its assets loading.

**Building the Test profile by hand** (done 2026-11-23, with MO2 closed; MO2 accepted it and showed the right plugin list):

```bash
cd ~/Games/mo2-lint/mo2-fallout4-steam/profiles
cp -r Default Test
# in Test/plugins.txt: strip the leading * from every line except the plugins to keep
# (files use CRLF line endings; keep them)
# in Test/settings.ini: LocalSaves=false -> LocalSaves=true
```

- `*Unmanaged:` lines in `modlist.txt` can't be switched off there; `plugins.txt` is what controls loading.
- Official DLC and Creation Club plugins aren't listed in `plugins.txt` (the game enables CC through `Fallout4.ccc`), so they stay on.
- Kept enabled: `cheatterminal.esp` (needs only `Fallout4.esm`) for god mode, spawning items and moving around during tests.
- `LocalSaves=true` keeps test saves out of the normal profile. In MO2 pick **Test** from the profile dropdown; answer No if asked to transfer saves.
- Game launch with this profile: works (2026-11-23). The prologue autosaves landed in `profiles/Test/saves`, so local saves are working. Confirmed in game: the cheat terminal holotape is there and the third-party mods are gone.

## Fallout 4 caveats *(upstream)*

- Some F4SE plugins misbehave under Proton. No F4SE plugins are installed yet.
- Missing some audio: add `WINEDLLOVERRIDES="winmm,version=n,b" %command%` to the game's launch options. If it persists, try Proton GE.
- ENB 0.393 and older may need `EnablePostPassShader` disabled.
- F4SE breaks whenever Steam updates Fallout 4 ahead of a new F4SE build. Fix: install the newer F4SE (uninstall and reinstall the instance, or see upstream `update`).

## Troubleshooting

- Install aborts with "Could not resolve Steam Proton wrapper": the required Proton isn't installed (seen 2026-10-28, Proton Experimental). Install Proton 11.0 and retry.
- Install aborts with "Input is not a terminal": run it in Konsole, not from an assistant.

## Open

- Split the FO4Edit entry in two (normal and lookup), see above.
- Test a Nexus "Mod Manager Download" and confirm it lands in this instance.

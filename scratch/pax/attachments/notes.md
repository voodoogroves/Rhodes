# Attachments: shields, claws and blades

Later sections replace earlier ones where they say so. Shared goal and rules: [`../common.md`](../common.md).

## Arm shield (idea, 2026-11-26; owner would like it with a big blocking shield, on the power armor left arm)

### Model
- `SupermutantArmor0_Arms` `001B3A01` (playable `00248FD3`), `Actors\Supermutant\CharacterAssets\SMArmor0_Arms.nif`; base game. The wanted part is the big plate from the mutant's right arm.
- Both arms are one skinned shape (super mutant arm, hand and finger bones); material `Materials\actors\Supermutant\SupermutantArmor1.BGSM`. Ground model `SMArmor0_ArmsGO.nif` is unskinned; geometry not examined.
- Work: read geometry, isolate the plate, make rigid, move to left forearm (rotate or mirror), fit, render previews. Commit the script only, never the model. No meshing tool is set up (a reader and previewer exists, below).
- Creation Club candidates by name, not chosen: `ballisticshield.nif`, `heavyincineratorshield.nif`.

### Fitting every set
- Intended: one shield following the left forearm bone, offset measured per arm model (about five base game shapes; DLC, Creation Club and mod armor each need a look). Untested.

### Slots and race (records read, nothing tested in game)
- `PowerArmorRace` `0001D31E` has its own skeleton (`actors\PowerArmor\CharacterAssets\skeleton.nif`).
- T-60 left arm: `AA_Power_Arm_Left`, body slot 42, primary race Human with `PowerArmorRace` additional, model `ArmorPALeftArm.nif`; visible arm from OMOD `PA_T60_LArm` (`PA_T60_LArm.nif`). Frame: slots 33, 34, 35, 60.
- Preferred, no vanilla edits: our own wearable in a free body slot, same race pattern. Free slots checked 2026-11-26 (below).
- Fallback: own attach point `ap_PAX_Shield`. Child slots (misc, lining, paint) come from each set's base arm mod (`PA_T45_ArmLeft`, `PA_T51_LArm`, `PA_X01_LArm`, `PA_Raider_LArm`, `PA_T60_LArm`), so those need overriding, preferably by an xEdit patch script over the winning records, as an optional plugin. Owner has not decided.

### Left arm connect points (read from the base game models, 2026-11-26)
| Model (`actors\PowerArmor\CharacterAssets\Mods\`) | Parent points on root | Position |
|---|---|---|
| `PA_Raider_LArm.nif`, `PA_T45_LArm.nif`, `PA_X1_LArm.nif` | `p-Misc`, `p-Paint`, `p-Lining` | (-14.11, -7.33, 123.44) |
| `PA_T51_LArm.nif` | same three | (-14.11, -7.33, 122.94) |
| `PA_T60_LArm.nif` | same three | (-14.07, -7.33, 123.44) |

- Each of the five attaches with child point `C-LArmMod` to `P-LArmMod` on the base `ArmorPALeftArm.nif`. All have the bones `LArm_ForeArm1`, `LArm_ForeArm_Armor`, `LArm_UpperArm`, `LArm_UpperArm_Armor`, `L_Pauldron`.
- No shield or forearm accessory point on any of them; none read on the power armor skeleton either. No vanilla arm misc mod has a model. Headlamps are an example of a rigid add-on model on its own point (`c-Headlamp`).
- Route A (looks best, untested): skin the shield fully to `LArm_ForeArm1` and let it use an existing point. No vanilla model edits; one shield may suit all sets. Unproven: that a shared point accepts an extra part; fit against each arm's bulk.
- Route B: rigid shield on a new PAX point, edited into each set's arm model. More work and mod conflicts.

### Preview reader (2026-11-26)
- `scripts/nif/nifpreview.py` (`info`, `render`): lists loose parts, bones and connect points; draws six flat-shaded views. Previews stay outside every repo.
- `SMArmor0_Arms.nif` splits into two parts: the right arm (456 triangles, mostly `RArm_ForeArm3_skin`) and the left (292). The big right-hand piece is plate and glove joined by position; splitting at texture seams separates them cleanly. Bare shield: `render --seams --parts 1,5,6` (289 triangles). Its inner face looks open in the middle, where the glove covered it.
- The T-60 left arm's forearm shell is weighted to `LArm_ForeArm1` and `LArm_ForeArm_Armor`. Its stored coordinates differ from the super mutant's, so placing the plate takes the bone transforms (`placeshield.py`, below).
- Full-size fit on T-60, standing pose (`scripts/nif/placeshield.py`, 2026-11-26): the plate is mirrored and carried from the super mutant's left forearm bone to the power armor's (bone lengths 29.8 and 27.0), keeping its offset. It sits on the outer forearm and clears torso and leg. The arm shell pokes through the middle, so it needs to move outward. Its upper end passes the elbow, close under the pauldron; bent elbow and aiming poses are not checked.
- Adjusted (`--slide 6 --out auto`, push 7.8): no sampled point of the arm's forearm shell pokes through; the plate runs from 2.4 above the elbow to 43.4 toward the fingers (hand joint 27.0). A straight push leaves the plate standing off the arm; owner: pushed out too far.
- Closer fit (`--slide 6 --tilt -16 --roll 5 --out auto`, push 2.6): nothing sampled shows through the outer face; the arm sits partly inside the plate's thickness. Runs 2.4 above the elbow to 41.8. Owner: sinking into the arm is fine as long as nothing protrudes through the shield.
- Bent elbow (`--bend`, elbow only, shoulder still): at roll 5 the shield's top cuts into the upper arm and shoulder pad (15 of 289 plate triangles at 45 degrees, 42 at 90, 80 at 120). Sliding and scaling barely help; swinging round the arm does. `--slide 6 --tilt -16 --roll -40` (push 3.2): none cut in at 0 or 90, about 7 at 120. It turns the face toward the back when the arm hangs. `--roll -30` (push 2.3): clean at 90, about 24 at 120. Owner: hanging too low, too near the hand.
- Moved toward the elbow (`--slide 0 --tilt -12 --roll -40`, push 5.0): runs 8.5 above the elbow to 36.4; none cut in at 0 or 90, about 9 at 120. Halfway option `--slide 3 --tilt -16 --roll -40` (push 4.3, 8 at 120). The arm is thicker near the elbow, so moving up needs more push.
- Owner: height looks ok. More elbow-end tilt at the same push (5.0, slide 0, roll -40): at -12 nothing sampled shows through the front hanging or at 90, the arm only sinks into the back (at 120 the upper arm shows through by up to 1.1); at -16 the forearm comes through by up to 1.2, at -20 by 2.8, at -24 by 5.6.
- **Chosen (owner, 2026-11-26):** T-60 placement `--slide 0 --tilt -12 --roll -40 --out 5.0` at full size, "close enough". Checked by sampled points with the elbow only bent; other sets, animations and in-game fit are open. Run: `python3 -I scripts/nif/placeshield.py <meshes> <outdir> --slide 0 --tilt -12 --roll -40 --out 5.0`.

### Held tests (in game)
- `player.getisrace PowerArmorRace` inside and outside the suit (expected 1 and 0).
- Can an extra item be worn and seen in power armor, and does it stay through exit and re-entry?

### Test 1: separate wearable (built 2026-11-26, not yet run)
- Slots (plugins found in Data and the MO2 mods folder): power armor pieces use 30-39, 41-50, 52 and 60. No armor of any race uses 53, 56 or 57; the test uses 56 and 57.
- `scratch/pax/test1/build_test1.py` writes `PAXTest1.esp` in `~/Downloads/PAX-Test1.zip`: "PAX Test A (mutant arms)" in slot 56, "PAX Test B (X-01 left arm)" in slot 57; race Human plus `PowerArmorRace`.
- Steps: install with MO2 (Test profile, spare save). Console `help "PAX Test" 4 ARMO`, `player.additem <id> 1`, `player.equipitem <id>`. Check each outside the suit first (shows the plugin works), then in the suit: visible in third person, stays through exit and re-entry, and through save and reload. Note whether equipping works from the Pip-Boy.
- Caveat: the super mutant model has body segments that the game may hide under worn armor; item B avoids that.
- Result (2026-11-26): the suit refused plain apparel ("you can not equip that in power armor"). Added C and D, the same models with keyword `ArmorTypePower` `0004D8A1` and health 100; installed in the MO2 mod "PAX Test 1".
- **Attachment works (in game, owner screenshots, 2026-11-26):** C and D equip and show on the T-60. C is the unchanged super mutant model, so its big plate is on the right arm, as in the original; D is on the left arm. Route: our own wearable, no vanilla edits. Open: re-entry, save and reload, displaced parts, workbench.
- On exit (in game, 2026-11-26): C and D stay with the frame, listed in its Power Armor menu beside the T-60 pieces, not moved to the player's inventory, but are not displayed on the empty suit. Cause unknown. Getting back in equips and shows them again.
- Pip-Boy in the suit (in game): C and D show as equipped beside all five T-60 pieces; nothing displaced.
- **Item E built (2026-11-26, not yet seen in game):** `placeshield.py ... --write` (`scripts/nif/writeshield.py`) cuts the super mutant model to the plate (192 vertices, 289 triangles), stores it in `LArm_ForeArm1` coordinates, weights it to that bone and reverses the mirrored faces. Installed as `Meshes\PAX\Test\ShieldE.nif` in the MO2 mod, slot 56. The model stays out of the repo.
- **E in game (owner screenshot):** shows on the left arm at the previewed position. Owner: off a bit, nothing connects it to the arm (looks blank; wants metal that joins it), and it is see-through from the back.
- Second version (`--mounts --write`, `scripts/nif/mounts.py`): two solid blocks (3 to 9 and 16 to 23 along the forearm) from arm to shield using the plate's texture, and back faces on the whole plate. Checked offline with back faces hidden (`nifpreview.py render --cull`); no sampled mount point shows through the front. 3600 vertices, 1650 triangles. Position unchanged.
- In game (owner screenshots, aiming with a two-handed gun, 2026-11-26): looks solid; the shield rides the forearm across the front of the body.
- Owner's feel (not measured): the elbow end still stands far off, and it may be turned too far to the outside of the arm. Accepted for now. Open idea (owner): how many attachments PAX should have, beside skills that cost SPECIAL.

## Attachments: cost and unlock (owner, 2026-11-26)
- Attachments cost **no perk point**. They require research or finding something that teaches how, for example the super mutant arm armor the shield comes from, or require that item itself.
- Hand-placed `SupermutantArmor0_Arms_Playable` `00248FD3` in `Fallout4.esm` (read 2026-11-26): Boston Public Library interior (ref `00249009`) and Weston Water Treatment exterior (ref `00248FE6`). DLC, respawning and other sources not checked. Mutants wear `001B3A01` through `CreatureOutfit_Supermutant_Arms` `001B3A22`; whether that one can be looted is unchecked.
- Unlock method open: consume the piece as an ingredient (no script; crafting from a wearable crashed the game once in Regalia, cause unproven), or learn it on finding (needs a script, or a book or perk gate).
- Owner (2026-11-26, leaning, not settled): attachments may also need a SPECIAL cost, with an offset or drawback.
- Placeholder (owner, 2026-11-26): see whether paint schemes can apply to the new visible items.

## Other suits and round 2 (2026-11-26)
- The T-60 placement and its mounts used on the T-45, T-51, X-01 and Raider left arms (offline): at the same settings the forearm shell shows through the front on none, and no plate triangle cuts into the upper arm or shoulder pad hanging or bent 90. The T-60 mounts reach every arm; worst stand-off 2.2 (T-51, elbow block). So one model looks usable for all five. Not seen in game.
- In game with the mounted shield (2026-11-26, owner, screenshot): "blocking looks great".
- Round 2 in the test plugin (installed in MO2 2026-11-26; results below): "PAX Shield (proof)" with armor 50, energy 30 and -1 Agility while worn (`abReduceAgility`); perk `PAXSprintProof` `xx000811` (no sprint AP cost, only in power armor); perk `PAXLockProof` `xx000812` (prompt "PAX: Force Lock" on locked objects in power armor, does nothing); chemistry station recipe making the shield from `00248FD3` and one steel.
- Round 2 results (in game, owner, 2026-11-26): the worn effects apply and reverse on removal. "PAX: Force Lock" shows with the perk in power armor, does nothing, and is not offered outside the suit. The recipe lists at the chemistry station, but the preview shape looks wrong (probably our zero bounds and missing preview transform; fixed in the script, not yet seen). Crafting from the gauntlet made the shield without a crash. Sprint perk works: no AP drain in power armor, normal drain outside (an earlier "no drain anywhere" was god mode). All four round 2 tests pass.
- Craft preview and dropped item (in game, owner, 2026-11-26): copying the vanilla gauntlet's bounds and preview transform (`PTRN` `0022FD4B`) fixed the stretched preview; both then showed the two super mutant arm pieces. Owner: drop the other gauntlet. The shield items now use a trimmed copy (`scripts/nif/trimparts.py --keep 1`, collision unchanged); not yet seen in game.
- In game (owner, 2026-11-26): the one-gauntlet dropped model looks good, and so does the chemistry station preview.

## Fist weapons in power armor (read from "WaFists DLC", Nexus 25358, 2026-11-26)
- Its fist weapons are new `WEAP` records whose `DNAM` animation type is 1 (one-handed sword) instead of 0 (hand to hand). The Deathclaw Gauntlet copy differs from vanilla in only that byte; unarmed keywords are kept. *(inferred: this is what lets the suit equip them; untested by us)*
- It also overrides `PowerArmorRace` with no change we found beyond attack order and literal strings, and ships facial bone files; both look like editor leftovers. PAX should not override the race.
- Needs Far Harbor.

## Claw gauntlets (owner, 2026-11-26)

Lightning-claw style: 2-3 blades on a chassis on the **right** forearm, fought with the punching animations.

- **Chosen: way 1.** A worn attachment like the shield, always on, that raises punch and bash damage while equipped. Way 2 (a separate weapon swapped in, as in WaFists) is not chosen now; owner says it is known to work from that mod.
- Shishkebab and electrified officer claws should carry their fire and shock (read by the assistant as damage and look; owner to correct).

| Claw | Blades | Source model | Housing extras |
|---|---|---|---|
| Shishkebab | 2 | `weapons\shishkebab\shishkebab.nif` | Gas canister, pipes, nozzles, valve |
| Officer (electric) | 2 | `weapons\chineseofficersword\serratedbladeshock.nif` | Battery and wires |
| Assaultron | 3, staggered | `dlc01\weapons\assaultronblade\vibroblade.nif` (`DLCRobot - Main.ba2`) | Open |
| Ritual | 3, staggered | `weapons\machete\sacrificalblade.nif` | Open |

- Suggested, not agreed: one body slot for all claws; drawback of worse gun handling (fallback: the -1 Agility worn effect).
- Open: damage amounts, drawback, unlock (needs the source weapon?), whether bash triggers on-hit effects.

Models read (2026-11-26):
- The shock officer blade already has a coil and wires (`SerratedBladeShock:1`) and a pack at the root (`SerratedBladeShock:2`).
- In `Shishkebab_02:0`, loose part 18 is the blade, 1 the grip, 4 the trigger lever; the rest is tank, valve and pipes. Flames are separate effect shapes and particles with controllers; not examined for reuse.
- Right forearm bone `RArm_ForeArm1`: X toward the hand (hand joint 27, fingertips about 41), Y across the knuckles (thumb positive), Z out of the back of the hand.
- Preview script: `scripts/nif/placeclaw.py` (generated placeholder chassis; writes no game model).
- First layouts (offline, T-60 only, not yet judged by the owner): blades angled 9 degrees down beyond the chassis; officer pack on the chassis with generated cables; shishkebab tank and pipes on top, its pipe ends sitting above the blades. Elbow bend, gun poses and other suits not checked.

Records read from `Fallout4.esm` (2026-11-26):
- `PowerArmorRace` unarmed weapon is `UnarmedPowerArmor` `000C2C32`, keyword `WeaponTypeUnarmed` `0005240E`.
- Iron Fist: perk entry point 35 (read as Mod Attack Damage), multiply, weapon-tab `HasKeyword WeaponTypeUnarmed`; ranks x1.2, 1.4, 1.6, 1.8.
- Basher: entry point 26 (inferred: bash damage), multiply x1.25, 1.5, 1.75, 2, no conditions.

### Claw cost and unlock (owner, 2026-11-26)

- Both: crafting **needs items** (consuming a one-off source weapon takes it out of the game), **and** the recipe is gated behind research and training paid for with a SPECIAL point (the proxy perk cost). Invest the point, then get the recipe.
- Some claws can be crafted only once.
- Open: which SPECIAL stat, one research per claw or one for all, whether this replaces "no perk point, find or use the item" for the shield too. The SPECIAL spend needs a script.

Records read from `Fallout4.esm` (2026-11-26):
- Kremvh's Tooth appears to be a base `Machete` `00033FE0` with mod `mod_melee_Machete_Sacrificial` `001CF2A0`, from leveled list `DN033_LL_Machete_Sacrificial` (two placed references use that list). A recipe asking for a Machete takes any machete; a one-off ingredient needs our own plain item.
- Shishkebab looks **not** unique: `LL_Shishkebab` is also in `LL_Weapon_Melee_All_Unique` and the legendary melee base list. Quest `DN121` uses it. In-game supply not checked.

### Ritual claw test build (2026-11-26, installed, not yet seen in game)

- Owner: two blades, flat face turned (edge inward, outward or angled) instead of edge down. Three variants built: `--roll -90` (In), `90` (Out), `45` (Angled, angled outward).
- `scripts/nif/writeclaw.py` writes the model (blades with `MacheteBladeSacrificial.BGSM`, housing with `T60Arm01.BGSM`).
- In `PAXTest1.esp`: "PAX Claw In / Out / Angled", slot 53; worn perk doubles unarmed and bash damage (test value); chemistry station recipe for Claw In from a machete and one steel, gated on perk `PAXClawResearch`.
- Previous plugin kept on the Deck as `~/Downloads/PAXTest1.esp.before-claws`.
- Owner, 2026-11-26: **Angled** looks best in the mockups (not yet seen in game).
- On-hit effects need no script (read): Iron Fist adds disarm with perk entry point 51 (read as Apply Combat Hit Spell), a chance condition and a weapon-tab unarmed condition. Not yet tried on the claw.
- Owner, 2026-11-26: the Assaultron blade's electrified version does the same shock as the officer claw (no stagger); they may differ in requirements and styling. Officer blades lie flat (rolled 90), Assaultron blades stay edge down. Two blades each.
- Installed, not yet seen in game: "PAX Claw Officer" and "PAX Claw Assaultron" (`writeclaw.py --claw officer` / `assaultron_shock`). Same test damage perk; **no shock effect yet**.

### Claw crash (2026-11-26, open)

- In game (owner): equipping "PAX Claw Angled" crashed the game. No crash dump found. The model passes structural checks; cause unknown.
- Owner: only Angled crashed, and it was the first claw tried; read as the others equipping fine. So possibly a first-equip problem and not that model (unproven). Retry Angled first.
- Later (owner): Assaultron also crashes. All five installed claw models share the same block layout and pass the same structural checks, including the ones not reported to crash. `crashDumps` is empty.
- Installed to separate causes: "PAX Diag Model" (Angled model, no perk) and "PAX Diag Perk" (shield model, claw perk), both slot 53.

### Claws in game (owner, 2026-11-26)

- "PAX Diag Model" (the Angled model) equips and shows on the right forearm with textures (screenshot). "PAX Diag Perk" equips; it shows as the shield, as built.
- Crash seen when equipping Diag Model again after Diag Perk (both slot 53).
- Diag Model also crashed on the first equip of a later run, so the crash is intermittent. Diag Perk survived ten equips. Suspect: the claw model files. Next split: "PAX Diag Blades" and "PAX Diag Metal".
- Wanted: ritual blades slid up so the first hook near the hilt lands on the edge of the block mount (script now slides them back 5; **not installed yet**). Later: a few small bolts, dots or screws as fasteners.
- Split items "PAX Diag Blades" and "PAX Diag Metal" installed 2026-11-27. Previous plugin kept as `~/Downloads/PAXTest1.esp.before-split`.
- "PAX Diag Blades" crashed on equip (owner, 2026-11-27). Metal not yet tested. A byte comparison with the working shield and the T-60 arm (offline) showed no structural fault in the blade model. Owner: if Metal does not crash, the ritual blades go on hold.
- "PAX Diag Metal" did not crash (owner, 2026-11-27; number of tries not reported). **Ritual blades are on hold.** The fault looks to be in the blade shape (copied geometry or the weapon's material and shader), not in the writer as a whole. Assaultron also crashed and is built the same way; the officer claw is too.
- Installed 2026-11-27, not yet tested: "PAX Diag Swap", the crashing blade shape with the T-60 metal material (`writeclaw.py --only source --paint metal`). Previous plugin kept as `~/Downloads/PAXTest1.esp.before-swap`.
- "PAX Diag Swap" crashed on equip (owner, 2026-11-27), so the weapon material is not needed for the crash. Offline, the blade vertex data shows no bad values, unused vertices or empty triangles. Differences left between the claw writer and the working shield: 3 segments against 5, root node flags, file header source.
- Installed 2026-11-27, not yet tested: "PAX Diag Pack", the crashing blades with the shield's packaging (`writeclaw.py --only source --like-shield`). Previous plugin kept as `~/Downloads/PAXTest1.esp.before-pack`.
- "PAX Diag Pack" crashed on the first equip (owner, 2026-11-27): the shield's packaging does not cure it. Proposed next: a crash logger. A web search (not verified here) found Addictol Crash Logger (Nexus 84214), whose page says it supports 1.11.240; it needs Address Library for F4SE Plugins.

### Claw crash cause (2026-11-27; fix installed)

- Addictol Crash Logger 1.7.0 (installed on the Deck from its GitHub release) caught "PAX Diag Pack": access violation in `BSFixedString::operator=`, under `NiStream::LoadFixedString` and `BSLightingShaderProperty::LoadBinary`.
- Cause (read in the files): a lighting shader holds two string references, its material name and a root material (offset 60 in these models). `writeclaw.py` rebuilt the string table and updated only the first, so the second pointed past the end. All claw and diag models had this, including "Diag Metal", which happened not to crash. The shield keeps the source's whole table.
- Fixed in `writeclaw.py`, which now also checks both references on read-back. The five claw models and "Diag Pack" were rebuilt and installed; ritual claws now include the 5 unit slide back. Old models kept in `~/Downloads/PAX-claw-models.before-fix/`.
- The ritual hold was a response to this crash; lifting it waits on the in-game test.
- In game (owner, 2026-11-27): rebuilt "PAX Claw Angled" equipped ten times with no crash. Other claws still to be tried.

### Claw looks in game (owner, 2026-11-27)

- Screenshots show the ritual Angled, Assaultron and officer claws worn, textured.
- Ritual Angled: good enough; the rough, welded-on look suits the blades. Wanted: slid up so they reach less far past the hand. Housing texture or detail later.
- Assaultron: blades look right. Wanted: slid up until the points are about level with the knuckles; **three** parallel blades, same orientation. Later, a housing shaped after a robot (sentry bot, Protectron, Assaultron or Mr Handy).
- Officer: a bit long, slide up. Coil and wires are liked; wanted about four batteries in a line.
- Built for this (not yet seen in game): slide back 11 (ritual), 19.2 (Assaultron), 12 (officer); knuckles are about 35 along the forearm.
- Installed 2026-11-27, not yet seen in game: ritual (In, Out, Angled), officer with four batteries, three-blade Assaultron. Parts of a blade behind a cut inside the housing are left off. Old models kept in `~/Downloads/PAX-claw-models.before-slide/`.
- Owner idea (2026-11-27): officer claw mounted in **two laser pistol bodies**, blades out of the muzzles, extra wires. Mocked up offline (`placeclaw.py --claw officer_laser`, `~/Downloads/PAX-claw-previews/laser/`), pistol parts `laserreceiver.nif` and `laserpistolbarrel.nif`; no batteries in this version. Owner: very amusing, the silly-and-dangerous Fallout mix they enjoy; the pistols could sit closer (mockup moved from 3.4 to 2.5 off the middle). `writeclaw.py` cannot write it yet (some pistol shapes have another vertex layout or a node rotation).

### Claw looks, second pass (owner, 2026-11-27)

- Screenshots: ritual angle good but the join looks flimsy (wanted: blades parallel to the block, or straps over the join, perhaps a flatter top or matching bevel). Assaultron a little short. Officer length is right: tips should land between the start and the end of the fingers.
- Calibration: in the game's relaxed pose a tip near 45 along the forearm lands among the fingers; the earlier "knuckles at 35" target was too short.
- Installed, not yet seen in game: Angled ritual on a straight block with 45 degree faces, blades lying on them under two straps with bolt heads; Assaultron tips at 45. In and Out ritual not rebuilt. Old models in `~/Downloads/PAX-claw-models.before-straps/`.
- Wanted later: a rounded, robot-like Assaultron housing; perhaps the back of the power fist as a detail.

- In game (owner, 2026-11-27): placement is good on all the current claws; the straps over the ritual blades are liked.
- The "PAX Diag" crash test items (IDs 840 to 84B) were removed from the test plugin.

### Shishkebab claw look (owner, 2026-11-27)

- Wanted: angled blades like the ritual Angled claw, because the Shishkebab blade arcs with a curve. Not yet mocked up.

### Claw tests, third pass (owner, 2026-11-27)

- Works in game: the damage perk is added with a claw on, punch and bash each do about double, and the perk goes on unequip and suit exit and returns on getting back in.
- Recipe: lists at the chemistry station showing the PAX Claw Research requirement (screenshots). Crafting not tried (no machete).
- Glitch: three claws (all slot 53) showed as equipped at once and none drew, also after exit and re-entry; the shield still drew. The installed records and models had not changed. A game restart cleared it. Possibly set off by switching to first person during punch tests (owner's guess); not reproduced afterwards. Cause unknown.
- Swap test (claw model in slot 57, shield model in slot 53): both drew. Items sharing slot 53 replace each other; different slots stack. The swap items were then removed from the plugin.
- Claws have no first-person model. Gun poses look good (owner).

## Clawed arm and per-suit attachments (owner, 2026-11-27)

- Owner idea: build the claw into a power armor arm ("Clawed T-60") in place of a worn item; equipping on and off is nice but may be the wrong approach.
- Owner: attachments need not cover every suit; for example Raider gets one claw, T-60 and T-51 the Assaultron or officer blades.
- Assistant suggestion, not agreed: a model mod on the normal right arm (our copy of the arm model with the blades merged in), installed at the power armor station. Spike one first (T-60, Angled) and judge first person. Untested: paint, first-person model, carrying the damage perk and research gate on the mod.

## Shield types (owner, 2026-11-27)
- Consider a couple of shield types.
- Equipping each gives a nominal bonus, plus an additional one while blocking.
- Each costs a SPECIAL point to learn to build, as a limiter. This bears on attachments question 1 in [`handoff.md`](../handoff.md) (does the shield follow the claw rule).
- Open: which types, the bonuses, which SPECIAL stat.

## Claw recipes by source weapon (2026-11-27; replaces earlier claw cost lines where they differ)

- Owner: no "loose mod" ingredients. They are not found in game, so the player would have to build the mod and strip it, a tedious middle step. Ask for the base weapons and charge the materials instead.
- Assistant suggestion: put the perk requirements on the research (holotape), with the SPECIAL cost, and have the recipe ask only for the research perk (the craft screen shows two perks).

| | Officer claw | Assaultron claw |
|---|---|---|
| Research | Blacksmith 3, Science 1, SPECIAL point (stat open) | Blacksmith 2, Science 1, Automatron, SPECIAL point (assistant proposal) |
| Weapons | 2 Chinese Officer Swords `00147BE4` | 3 Assaultron Blades (`DLCRobot.esm` `xx008B8E`) (owner: 3) |
| Materials | Twice the electrified serrated mod: aluminum 16, adhesive 10, rubber 8, oil 8, fiberglass 6, circuitry 4 | Three times the electrified mod (assistant proposal): aluminum 24, adhesive 12, rubber 9, circuitry 9 |

- Officer swords are renewable (records read): raider lists, legendary base list, one NPC, melee vendors.
- Assaultron Blade supply (records read, scripts not checked): the melee Rust Devil's weapon list (blade or Mr. Handy buzz blade, equal entries), and that NPC found only in three random encounter quests; one in the boss chest of the Fort Hagen satellite array quest (alias `DLC01MQ04BossChest`). No vendor or other list found.
- Suggested, not agreed: place one extra blade at a Rust Devil location, for two sure blades and one hunted.
- To test: crafting from weapons does not crash; which copy is consumed when one is a favorite or equipped.

## Tessa's Fist and the Tesla suit

Suit themes are in [`../common.md`](../common.md), "Suit themes".

Records read (2026-11-27):
- Tessa's Fist: a Raider right arm (`LL_Armor_Power_Raider_ArmRight`) with Hydraulic Bracers `00203748` and the legendary "Almost Unbreakable" `001F1E0C`. The durability effect belongs to the legendary and is not specific to punching; the punch bonus is the bracers.
- The Tesla T-60 set (left arm, right arm, torso) is in `DLCRobot.esm`, listed in `DLC01LL_Armor_Power_T60_Set_A_Tesla`, used by `DLC01_PowerArmorFurnitureTesla`.
- `DLC01PowerArmorFurnitureTesla` is the suit of `DLC01LvlBotRaider_FemaleBoss`, the Rust Devil placed as that quest's boss. This matches the owner's T-60 Tesla boss.

## Station arm swap, Tesla T-60 (2026-11-27)

### Upgrading an item and keeping it (owner)
- Wanted: a bladed Tessa's Fist, upgrading the item and preserving the base.
- Assistant suggestion: our claw as a replacement arm model mod installed at the power armor station, so the item, its legendary and its misc mod stay (inferred, untested). The mod must offer the same child attach points (misc, lining, paint where present).
- Read: arm model mods sit on `ap_PowerArmor_RArmMod`. `PA_T60_RArm` has a recipe (`co_PA_T60_RArm`); `PA_Raider_RArm` has none. Whether the station offers the slot is the biggest unknown.
- Name: expected to stay "Tessa's Fist" (untested). Adding "Bladed" would likely need the vanilla naming rules edited.
- Proposed first spike, not agreed: Tessa's Fist arm swap (station slot, item preservation, first person).
- The Tesla T-60 right arm is itself an arm model mod, so a Tesla claw would be its own variant (inferred).

### Tesla T-60 (owner, thinking aloud)
- Tesla shield on the left arm instead of the plain shield; arcing electrified Assaultron blades on the right. The shield could block and reflect some damage as electricity.
- If too hard: a Tesla array on the back (like the sentry bot missiles) and a grenade-like Tesla lobber.
- Read: perk entry points `Mod Percent Blocked` and `Mod Reflect Damage Chance` exist (offline CK wiki). Electric reflected damage is open. Untested.
- Conflicts to settle: reflect is a legendary effect (`mod_Legendary_Armor_ReflectDamage`) and the owner ruled out duplicating those; a shock back at attackers may be distinct. A back array on the torso misc slot would exclude Tesla Coils (inferred).

### First person (read 2026-11-27)
- Each base game arm has a second model, `..._1st.nif` (T-60 right: forearm only, bone `RArm_ForeArm1`). The arm mod record names only the third-person file; the game likely finds the other by suffix (inferred; `_1st` is in the exe).
- A clawed arm would ship both. Worn test items set no first-person model in their armor addon, the likely reason they do not show (untested).

### Ambient effects and animation (owner: wanted for the claws)
- Shishkebab: not yet built. `shishkebab.nif` carries effect shapes, a particle system, a light, animation controllers and a behaviour file (`UniqueBehaviors\ShishkebabFX`); idle loop sound `WPNShishkebabIdleLPM` `00231FC5`. Whether the animation runs on armor is the main risk. Angled layout first.
- Electrified officer and Assaultron blade models have no effect shapes. `meshes\effects\shaderparticles\shockswordconstfxs.nif` exists; what attaches it was not found.
- On-hit fire and shock are separate from the ambient look.
- Open: ambient effects always on, or only with weapons drawn?

## Super Mutant Heavy Gauntlet supply (records read, 2026-11-27)
- Playable `00248FD3`: two placed references in `Fallout4.esm` (`00248FE6`, `00249009`). No leveled list, outfit, container (so no vendor) or recipe there refers to it, and no reference was found in the DLC or Creation Club plugins.
- The gauntlets super mutants wear (`001B3A01`) are flagged non-playable.
- Not checked: scripts, third-party mods, and whether the two placed items come back when their areas reset.

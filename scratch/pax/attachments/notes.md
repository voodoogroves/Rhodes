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

## Raider: first suit (owner chose, 2026-11-27)
Theme: ritual (machete) blades with Tessa's Fist, upgrading the item and keeping it. Base game only.

Where it stands:
- Ritual Angled claw as a worn item: placement, look with straps, double punch and bash damage and gun poses passed in game; the blade crash is fixed. Crafting not tried. No first-person model.
- Tessa's Fist: Raider right arm, Hydraulic Bracers, "Almost Unbreakable" (records above).
- `PA_Raider_RArm` sits on `ap_PowerArmor_RArmMod`, has no recipe and no paint point seen. It has a first-person file, `pa_raider_rarm_1st.nif`.
- Placement so far was worked out on the T-60; the Raider arm is not fitted.
- Cost rule: an arm swap adds on top (the arm keeps its modules), so it needs a SPECIAL or perk cost, plus items.

First steps (proposed):
1. Spike: a copy of the Raider right arm as our own arm mod. Does the station offer it, and do the legendary, bracers and name survive?
2. Merge the Angled blades into the third-person and first-person arm models; check both views.
3. Move the damage perk and research gate onto the mod.

To decide:
- Ingredients: a recipe asking for a Machete takes any machete, so what is the hunt (rare item, or one we place)?
- SPECIAL stat for research, damage amounts, any drawback.
- Whether the left arm gets anything, and whether the claw is only for the right arm.
- Whether other Raider pieces get options.

### Raider arm slot and Overboss (records read 2026-11-27)
- The arm model slot `ap_PowerArmor_RArmMod` `00055F8E` has no display name and is not in the station's slot order list `do_ModMenuSlotKeywordList` `0005F814`; misc, paint and lining are named and listed. Whether the station offers it anyway is untested (the 2021 CK wiki describes the list as ordering the slots).
- On that slot, base game, DLC and Creation Club right arm model mods: only `PA_T60_RArm` has a recipe. `PA_Raider_RArm` `00137B7F` has no name, recipe or target keywords. The recipe `co_DLC01_Armor_Power_T60_Tesla_ArmRight` makes `0100C57A`, not the arm mod `0100C575` (inferred: the whole armor piece).
- `ma_PA_Raider_RArm` `00184180` is on the Raider right arm `00140C53` and the Overboss right arm (`DLCNukaWorld.esm` `xx00DC28`).
- **Overboss:** every limb, torso and helmet is its own armor piece with higher stats (right arm health 80 against 50; corrected 2026-11-27, the earlier 130 and 75 were the value field) and its own Overboss model mod (`DLC04_PA_Overboss_RArm` `xx00B8EA` and the like), on the same attach points. Its keywords on the right arm match the Raider arm's, so Raider arm mods apply to it. A claw arm model mod would replace the Overboss look unless we make a second one merged into `Overboss_Rarm.nif`.

### Upgrade scope (owner, 2026-11-27)
- The claw is an upgrade to **any Raider power armor arm**, Tessa's Fist included; on Tessa's Fist the base ability stays.
- Open: does it cover Overboss arms (assistant: leave them out, per the suit theme table); right arm only, or both.

### Arm swap spike (built and installed 2026-11-27, not yet tested)
- In `PAXTest1.esp`: arm mods "PAX Spike Arm (T-60 look)" `xx000850` and "PAX Raider Arm" `xx000852` (restores the Raider model), each with a one-steel recipe, offered by `ma_PA_Raider_RArm`. Their record data is the vanilla Raider arm mod's, so only the model differs. No new models.
- To answer: does the station show the slot; do the legendary, Hydraulic Bracers, name and lining survive; does swapping back work; save and reload.
- If the slot does not show (assistant order): name the slot by overriding the keyword (breaks the no-change rule); swap by script (needs a compiler); keep the worn claw.
- Previous plugin kept as `~/Downloads/PAXTest1.esp.before-arm-swap`.


### Rules for arm upgrades (owner, 2026-11-27)
- Arm upgrades never take a limb's misc or lining slot. They stack on vanilla mods, with a SPECIAL cost and a rare component.
- Taking the jetpack's slot is acceptable.
- The Raider claw is built as the arm's model, which the station does not normally offer (spike above).

### Raider claw recipe: Kremvh's Tooth (owner, 2026-11-27; replaces the open ingredient question)
- A SPECIAL cost for the recipe (stat open) and one unique item consumed on construction: Kremvh's Tooth.
- Records read: the Tooth is a base `Machete` `00033FE0` with `mod_melee_Machete_Sacrificial` `001CF2A0`, so a recipe cannot ask for the Tooth itself. The mod has a loose item, `miscmod_mod_melee_Machete_Sacrificial` `0022576E` (a plain `MISC`), and no recipe in the base game or DLC makes the mod.
- Proposed, not yet agreed: the recipe asks for that loose item. The player takes it off the Tooth at the weapon workbench by fitting the standard blade (`co_mod_melee_Machete_Standard` `0018785F`, no components or conditions). Untested in game.
- Supply: leveled list `DN033_LL_Machete_Sacrificial` `0022576D` is used by two placed references: `00225B5E` in Dunwich Borers (`DunwichBorers01`) and `00198DC9` in an unnamed interior cell `00198DA2` at position zero (inferred: not reachable). No other use found in records; scripts not checked.

### Arm swap spike result (in game, owner, 2026-11-27)
- A Raider right arm and "Tessa's Fist" offered only the lining and misc slots at the power armor station (screenshot). Neither PAX arm mod was offered. T-60 check and save/reload not applicable.
- The cause is taken to be the unnamed, unlisted attach point (inferred). The build had no control showing that a mod of our own record format appears at the station.
- Kremvh's Tooth: the console leveled list `0022576D` gave the Tooth, and fitting another blade at the weapon workbench left the mod in inventory. **The recipe ingredient works as proposed** (crafting from it not yet tried).

### Tessa's Fist (correction; replaces "Hydraulic Bracers" as read earlier)
- `player.additem 00248487 1` gave an arm named "Tessa's Fist" with **No Misc Mod** (screenshot).
- Records: its mods come from form list `CustomItemMods_DN109_TessasFist` `00248488`, read by `CustomItemQuest` `0022576B`, so a console copy does not get them (inferred). The list holds `001F1E0C` (Almost Unbreakable) and `00203748`, which is the **T-60** Hydraulic Bracers (`PA_T60_Arm_Misc_Unarmed`), not the Raider ones (`0020374A`). Whether the T-60 mod takes on the Raider arm in a real playthrough is not checked.

## Raider weapons: two arms (owner, 2026-11-27)
- Two weapons, no shield: Raiders are not defense. The super mutant shield is a T-45 option.
- Right arm: the Tooth blade claw (Kremvh's Tooth, Dunwich Borers).
- Left forearm: a brick bound with rebar, power-fist-like but mounted on the forearm, not a held weapon.
- Source models found (read and previewed offline): `weapons\powerfist\rebarfist.nif`, the add-on of `mod_melee_Powerfist_SpikesLarge` `001849E1` (brick, three bars, chain), which matches the idea; `weapons\sledgehammer\mod_sledgehammer_cinderblock.nif` (`mod_melee_Sledgehammer_ExtraHeavyHead` `00185CFB`: block with two riveted bands). Previews in `~/Downloads/PAX-claw-previews/brick/`.
- Open: left arm recipe and unique ingredient, one research or two, effects (punch effects probably apply to both fists), new crafted item or script upgrade.

### Brick ram mockups (offline, 2026-11-27)
- `scripts/nif/placeram.py` mocks it up on the Raider left arm. `rebarfist.nif` is the in-game **Puncturing** Power Fist mod, where the bars are spikes pointing forward; our mockup turns them back along the arm.
- Owner, on the first three layouts: the one with the brick mounted toward the wrist was closest. Wanted: brick lined up with the start of the fingers, no curve in the bracing, and a piece of the Power Fist (its cuff) as one mount. The cuff may sink into the arm and rise above it as a partial curve.
- Second version (`~/Downloads/PAX-claw-previews/raider/wrist_v2_arm.png`, not yet judged): brick spans 31 to 39 along the forearm, three straight bars rising to the cuff arc at 12, one placeholder strap at 22. Not checked: bent elbow, gun poses, textures, whether our writer can handle these shapes.
- Owner changes after the second version, all applied in `placeram.py` (offline, not yet judged): brick tilted to lie along the bars; cuff raised so the outer bars meet it; cuff filled down into the arm with a wider foot, so no air gap; whole mount rolled 13 degrees round the arm to match the knuckle line. The foot is placeholder geometry and the strap is still a placeholder. Earlier pictures kept beside the new one as `wrist_v2_arm_before_tilt.png` and `wrist_v2_arm_before_foot.png` (the latter is the tilted version).
- Third round (owner, 2026-11-27): ring slightly smaller; keep the strap, bent or strapped down, with the ordinary raider chest armor as a style reference; brick moved back to just past the arm armor if the bars still reach it. Applied: ring scale 1.25 (was 1.4); brick back face at 27.6 along the forearm (arm armor ends about 27), leaning only 0.07; bars overlap the brick by about 0.5; a generated tight strap with a buckle at 21. Reference looked at: `armor\raidermodarmor\{litetorso,medtorso}.nif` (material `Materials\Armor\RaiderModArmor\Armor.BGSM`); no piece borrowed yet. Previous picture: `wrist_v3_arm_before.png`.
- Fourth round (owner, 2026-11-27): the rebar should reach **out** from the front of the brick, as on the Puncturing Power Fist (as well as the bars back to the mount); the brick looked too high and tilted up. Applied: the three vanilla bars added in front at their own lengths (longest tip about 53 along the forearm, fingertips about 41); bars and brick lean 0.22, which brings the brick down onto the wrist. Previous picture: `wrist_v4_arm_before.png`. Owner: the forward rebar looks good.
- Fifth round (owner): the chain should actually wrap the brick; the ring flatter, with less of a peak. The vanilla chain also loops round the fist's front plate, so each link is now moved along the arm to lie on the brick; ring height 0.65 of its width. Applied, not yet judged.
- Sixth round (owner: "this is looking really solid"): clip the forward bars back. Raider gear should have some asymmetry and roughness: outers shorter than the middle, kept half twisted. Applied (`SPIKES` in `placeram.py`): lengths past the brick 6.5, 9.0 (middle) and 4.8 (were about 12, 18 and 9), vanilla kinks squeezed in, each bent and swung differently. Previous picture: `wrist_v6_arm_before.png`. Not yet judged.
- Seventh round (owner): the strap should join on each side with a bolt at each end, taking ideas from Gage's armor (Nuka-World). Reference read: `meshes\dlc04\clothes\gage\armorgo.nif` (`materials\DLC04\Clothes\Gage\GageHeavyArmor01.BGSM`): flat bent metal bars held by large hex bolts. Applied: the band runs over the bars to the same depth on both sides, with a plate and hex bolt at each end; buckle kept. Reference only; PAX stays base game, so no Nuka-World asset is used.
- Full suit with both weapons drawn offline (`suit_wrist_v2.png`), not yet judged. Not checked: bent elbow, gun poses, textures, first person.

## Raider: lore note and effects (owner, 2026-11-27)

### Lore note
- A note introducing the Raider upgrades, placed near **Outpost Zimonja**, where Boomer is (owner: one of the first enemies met in power armor). It talks about upgrading raider armor and points to a power fist, or to what Tessa did at Quincy, and the like.
- Records read: `NPC_` `DN168_LvlRaiderBoss` `000AE154` is named Boomer; location `RelayTowerZimonjaLocation` `00055402` is Outpost Zimonja. His armor and the spot for the note are not checked.

### Effects
- Right (claw): **bleed and poison**.
- Left (brick): **armor penetration and more melee damage**.
- Not overpowered; themed to raider armor and to the weapons consumed.
- Records read: Kremvh's Tooth's mod `001CF2A0` already carries `EnchWeapModBleed` `0009733E` and `ench_mod_LegendaryWeapon_DamagePoison` `00085700`. The Puncturing mod `001849E1` adds keyword `ap_melee_ArmorPenetrate` `00097342` and raises damage; it is a craftable mod (`co_mod_melee_Powerfist_SpikesLarge`).
- Open: amounts; punch effects probably apply to both fists (no way is known to tie an effect to one arm), so the pair adds up on every punch; left arm ingredient (a Power Fist implied, not confirmed). Nothing built or tested.
- Claw mount, owner: agreed it looked unfinished next to the ram; "spice up" the mount with bolts or wire mesh / fencing. Applied in `placeram.py` (offline, not yet judged; `writeclaw.py` and the in-game claw are unchanged): generated chain-link wire over the housing, one bolted band at the elbow end, hex bolts on the flanks, one blade 2.2 further forward.
- Owner: the claw should roll like the ram to line up with the fingers. Applied: 13 degrees, from the right knuckle bones. Pictures `claw_v2_arm.png` (before the roll: `claw_v2_arm_before_roll.png`) and `suit_wrist_v2.png`.
- Owner (2026-11-27): both arm mockups look good. Effects landing on every punch is accepted; keep them small for that reason.

## Raider torso / legs (thinking aloud, owner, 2026-11-27; nothing decided)
- A launcher, or something else for the torso or legs. Recalled: a robot mod that gives melee **attackers** a stack of bleed.
- Records read: the Automatron spiked and serrated plates say "Melee targets bleed" and work through `DLC01Bot_CommonArmorPerk` `0100128C`, entry point 51 (Apply Combat Hit Spell), so it is the **wearer's** hits that bleed the target (inferred from the entry point). What does hurt attackers: Reactive Plates (`PA_Raider_Torso_Misc_Reactive` `001D0323`, reflects 50% melee damage) and the Punishing legendary. Far Harbor's freeze and burn attackers legendaries cast a spell from a script (`DLC03:dlc03_Legendary_OnMeleeEffect`). A no-script way to bleed attackers was not found; the 2021 CK wiki has a garbled line suggesting one entry point reaches attackers, not checked.
- Owner (2026-11-27): loves the **junk launcher**; also wants an option for **increased durability** by strapping on extra junk. Details open (see also `../secondary-weapons/notes.md` and "Slower armor wear" in `../perks/notes.md`).
- Owner (2026-11-27): the **scrap harness** goes on legs and torso and costs a SPECIAL point plus materials; looks: signs and junk clamped on.
- Owner: for the launcher, an area burst that is not a grenade, with attacks to reference; otherwise lots of sawed-off shotguns.
- Records read (`Fallout4.esm`; spread and count decoded by the assistant, not seen in game): explosions can spawn projectiles. `TrapfragGrenadeExplosion3` `001C037B` throws 15 of `TrapFragGrenadeProjectile2` over 120 degrees; `SentryShoulderClusterExplosionChild` `00216362` 5 over 30; `HeavyProjectileExplosion` `001B88DA` spawns shrapnel (`MedShrapnelProjectileChild`). Sawed-off barrel: `mod_DoubleBarrelShotgun_BarrelShotgun_VeryShort` `00149CA5`.
- Owner (2026-11-27): the scrap harness could increase both durability and protection. Next: mock up the shotgun rack.
- Shotgun rack, first mockup (offline, not yet judged): `scripts/nif/placerack.py`; pictures `~/Downloads/PAX-claw-previews/raider/rack_back.png` and `rack_suit.png`. Five sawed-offs (`weapons\shotgun\` receiver, short barrel and short stock) fanned over the shoulders at uneven angles, three on the left and two on the right, two bolted bands, two rebar uprights, a wire fence patch. Not checked: pauldron and arm movement, textures, clipping with the helmet cage, whether the writer can handle these shapes.
- Rack, owner changes (2026-11-27): face the guns forward; one of each barrel (handmade triple, handmade double, base double sawed-off, combat shotgun), one by each side of the head and one low on each side; too arm-mounted on hips and shoulders, so on the torso and head; shorter barrels are fine. Applied in `placerack.py`: head pair at about 154 high, chest pair at about 111, barrels at 0.55 of the short length (combat 0.7), fitted bolted clamps, rebar struts. The handmade shotguns come from `ccFRSFO4001-HandmadeShotgun` (Creation Club), which becomes a requirement; this replaces "base game only" for the Raider set. Offline, not yet judged; skinned to which bone is undecided (the head pair would not turn with the head if on the torso).
- Rack, next change (owner): lower pair slid back, mounted at the belt; upper pair down by the neck, poking out of the helmet mesh. Applied: upper guns at 139 high, muzzles out through the cage; lower at about 100, beside the waist. Previous pictures `rack_front_v3.png`, `rack_suit_v3_chest.png`. Not yet judged; arm clipping not checked.
- Rack, next change (owner): slide the guns back; the neck barrels can be longer and rest along the collar; drop the back straps, add a few on the sides. Applied: collar pair slid back with full short barrels (combat 0.85); belt pair slid back about 10; back bands, uprights and fence patch removed; a bolted strap along each side at belt and collar height. Previous pictures `rack_front_v4.png`, `rack_suit_v4_neck.png`. Not yet judged.
- Owner (2026-11-27), on the fifth rack layout: it captures an amusing raider concept. Committed as it stands.

## Raider set as it stands (2026-11-27; summary, replaces the open items in "Raider: first suit")

| Piece | Does | Cost (owner) | State |
|---|---|---|---|
| Claw, right arm (Kremvh's Tooth blade) | Bleed, poison | SPECIAL + the blade | Worn test claw passed in game; dressed mockup offline |
| Brick ram, left arm | Armor penetration, melee damage | SPECIAL; a Power Fist implied, not confirmed | Offline mockup, owner: looks good |
| Shotgun rack, jetpack slot | Area volley | Takes the slot; no extra cost is the assistant's reading of the balance rule | Offline mockup, owner likes it |
| Scrap harness, torso and legs | Durability and protection | SPECIAL + materials | Offline mockup |

- Punch effects land on every punch (accepted); keep them small.
- Lore note near Outpost Zimonja.
- The rack needs Creation Club `ccFRSFO4001-HandmadeShotgun`.
- Open: how the arms are delivered (station swap failed; script swap, new crafted arm item, or worn piece; the owner has not chosen after the new-item proposal), how the rack fires (grenade type untested, spray direction unknown), real models (writer handles only simple one-bone shapes so far), body slots for several worn pieces, textures, bent elbow, gun poses, arm clipping, first person, the SPECIAL stat, a compiler.


## Scrap harness junk (owner, 2026-11-27)
- Picks: **hubcap, frying pan, signs**, and a stuffed animal such as a **teddy bear** to help absorb shocks.
- The **manhole cover** is saved for a second shield later.
- First harness mockup (offline, not yet judged): `scripts/nif/placeharness.py`, picture `~/Downloads/PAX-claw-previews/raider/harness_suit.png`. Highway sign on the chest, Diamond City street sign across the left thigh, frying pan at the waist, hubcap on the right knee, dirty teddy bear strapped to the left knee. Models: `setdressing\signage\highwaysign01`, `setdressing\dmndclutter\dmndstreetsign01` (boards only), `vehicles\automotive\automotivehubcap01`, `setdressing\playerhouse\playerhouse_potsfryingpan01`, `setdressing\teddybear\toyteddybeardirty01`. Known faults: the suit shows through a notch in the chest sign; the pan stands a little off the waist. Not checked: leg movement, textures.
- Harness, second version (owner changes): leg items off the knees and angled outward, one on each calf and one on a thigh; frying pan off the waist; chest sign bent to the chest; one item wrapped in chain and one in fencing instead of metal straps. Applied: hubcap chained to the right calf, teddy bear (a little bigger) caged in fencing on the left calf, pan on the right thigh, street sign stays on the left thigh, chest sign conformed to the surface under it. Faults: the middle of the street sign sinks into the thigh. Previous picture `harness_suit_v1.png`. Not yet judged.
- Harness, third version (owner: do the touch-ups, and put the leg items at different places round the leg). Applied: right thigh pan on the outer side, right calf hubcap toward the front, left thigh sign toward the front, left calf bear on the outer side; street sign stood off so all of it shows; fencing top edge ragged, upper wire band removed. Faults: the street sign now stands off with a visible gap at its ends. Previous picture `harness_suit_v2.png`. Not yet judged.
- Harness, fourth version (owner: close the sign gap, bending is fine): the street sign is now beaten to the thigh like the chest sign. In the whole-set picture its lower end looks crumpled.
- Whole set on one suit: `scripts/nif/placeset.py`, picture `raider_set.png` (offline, not yet judged). Not checked: movement and clipping between pieces and arms, textures, first person.
- Back piece (owner): something recognisably odd for third person; loved the **lawn flamingo**, on condition it does not block the fusion core. Applied in `placeharness.py`: `setdressing\flamingo\lawnflamingo02static` without its stake, slanted across the upper back with its head past the wearer's right shoulder, two crossed chain runs; lowest point 123 high near the middle of the back (the core port reads as about 111 in the pictures, not measured). Previous picture `raider_set_v1.png`. Seen from the side it stands a little off the back. Not yet judged or committed.
- Flamingo snugged to the back and the chain tidied (no stray link). Its tail is now partly hidden in the back housing. Committed on the owner's say.

## How the harness is delivered (owner, 2026-11-27)
- "If you craft the scrap-enhanced torso and legs, this is what you get": crafted pieces that come with the junk already on them, carrying the extra durability and protection.
- Assistant reading, to confirm: three new armor pieces (torso, left leg, right leg), each with its own model, so no body slot and no script apart from the SPECIAL cost. Torso: chest sign and flamingo. Left leg: street sign and caged bear. Right leg: frying pan and chained hubcap. Lining and misc mods are refitted at the station; a legendary on the old piece does not carry over; the rack then sits in the new torso's jetpack slot. Unproven: a crafted piece taking our model from its template, and a model that merges our parts with the vanilla piece.
- **Arms follow the same pattern (owner, 2026-11-27):** crafted arm pieces with the weapons on them, giving a minor melee damage boost and the same durability and protection increase as the torso and legs. This replaces the upgrade-your-own-arm idea ("any Raider arm", Tessa's Fist keeping its ability). Arm upgrades still take no misc or lining slot.
- Open: whether the claw's bleed and poison and the brick's armor penetration stay on top of the damage boost (assumed yes, kept small); amounts of protection and damage; whether the helmet gets a piece.

- Durability (owner, 2026-11-27): **double**, not the four times of "Almost Unbreakable", which stays a legendary effect.
- Effects (assistant's choice, the owner left it open to the assistant): the claw keeps bleed and poison and the brick armor penetration, all small, beside the minor damage boost.

### Crafted piece spike (built and installed 2026-11-27, not yet tested)
- In `PAXTest1.esp`: "PAX Scrap Left Leg (spike)" `xx000861`, a copy of the Raider left leg `00140C55` with health 100 (vanilla 50), armor 60 (50), energy 30 (25), radiation unchanged; one combination: our model mod `xx000860` (Overboss left leg model path, no new master), `PA_Raider_Leg_Lining_A` `0007859A` and `00077D3A`. Chemistry station recipe `xx000862`, one steel. Shape choice: Overboss, because it is raider-style, visibly different and needs no new model; fitting Raider mods comes from the keywords, not the shape.
- To answer: crafting without a crash; does the piece show our model; stats; do lining and misc mods fit; save and reload.
- Previous plugin kept as `~/Downloads/PAXTest1.esp.before-scrap-leg`.
- In game (owner, 2026-11-27): the spike leg **crafted** at the chemistry station and **shows the Overboss shape**, so a crafted piece takes our model mod from its template. Stats, lining and misc, walking, save and reload not yet reported.
- Spike results (in game, owner screenshots): moves and looks good; correct after save and reload. The power armor screen shows armor 60, energy 30, radiation 150, health 100/100. The item shows as **"Raider Power Left Leg"**, not our name (inferred: the naming rules). Lining and misc at the station not reported.
- **Stat target (owner, 2026-11-27): above Raider II and just below Overboss.**
- Records read: "Welded Plate" linings add health +50 (torso +100) and armor +20 and no energy; Standard Plate adds none. So with standard plate, a limb: Raider 50 health / 50 armor / 25 energy; welded 100 / 70 / 25; Overboss 80 / 170 / 170. Overboss health is **below** welded Raider, so health cannot satisfy both ends.
- Assistant proposal, awaiting the owner: limbs 110 health, 150 armor, 150 energy; torso 250, 290, 290 (standard plate; welded adds on top).
- Owner (2026-11-27): linked wiki table (screenshot) shows Raider II stats matching the records (limb 70/25/150, 100 health; torso 220/100/300, 200 health). Raider II is an upgrade, like the T-60 tiers. If our crafted piece cannot be upgraded at the station (test), it should come upgraded as part of the add.
- In game (owner, 2026-11-27): the crafted spike leg **is offered Welded Plate** at the station and becomes Raider II. Crafted pieces upgrade the normal way, so the upgrade need not be built in.
- Assistant proposal, awaiting the owner (replaces the earlier one): crafted base above Raider II, upgraded just below Overboss armor. Limb 110 / 130 / 150 (health / armor / energy), upgraded 160 / 150 / 150. Torso 220 / 270 / 290, upgraded 320 / 290 / 290. Limb health upgraded passes Overboss (80 stock, 130 welded).
- Owner approved those numbers (2026-11-27). Applied in `build_test1.py`: the leg is "Scrap Raider Left Leg", 110 / 130 / 150 as crafted, with its own copy of the naming rules `xx000863` (copied from `dn_PowerArmor` `00188160`, words resolved to English at build time; Raider words changed to "Scrap Raider" and "Scrap Raider II"). Built; install waits for the game to be closed. Not tested.
- **Crafted already welded (owner, 2026-11-27):** the scrap pieces come with Welded Plate on them and the recipe charges for it. Final limb 160 / 150 / 150; torso 320 / 290 / 290. Both Raider naming words read "Scrap Raider". Welding components per the records and wiki: arm 3 aluminum, leg 4, torso 6.
- Junk as ingredients (owner "almost ok"). Records read (`Fallout4.esm`, base placements only): teddy bear `00059B14` placed 230 times (also `0022C1F0`, once); frying pan `0003D3A5` 15; hubcap `0007E941` 7, and in vendor and loot lists. No road sign or flamingo inventory item was found (those stay materials). Test leg recipe: aluminum 4, steel 3, one teddy bear (amounts are test values). Installed 2026-11-27, not yet tested; previous plugin kept as `~/Downloads/PAXTest1.esp.before-welded`.
- In game (owner screenshot, 2026-11-27): the welded crafted leg shows **"Scrap Raider Left Leg"**, 150 / 150 / 150, health 160, weight 18.7, value 82, Overboss shape, and the recipe required the teddy bear. Save and reload not reported for this build. Owner: some hunt is fine, 7 seems hard to find; is another cooking pot more plentiful?
- Right leg ingredient (owner: another pot can be used for crafting while the model stays the frying pan): **Cooking Pot** `CookingPot01` `00059ABA`, 88 base placements and in vendor and loot lists (frying pan 15). Other options read: `CookingPan01` `00059AEC` 60, `BigPot` `00059A7A` 37. Hubcap `0007E941`: 7 placements, but also in loot, vendor, auto parts and Sanctuary workshop lists. The right leg is not built yet.
- **Name (owner, 2026-11-27): these raider items are "Scrappy"**, not "Scrap" (for example "Scrappy Raider Left Leg"). Earlier uses of "scrap harness" and "scrap" pieces mean the same set.
- **Backup recipes (owner, 2026-11-27):** a bit of a hunt is fine, with cover for accidental scrapping. Chemistry station: teddy bear from cloth 10, leather 3, adhesive 3; cooking pot from steel 10, copper 3; hubcap from aluminum 8, steel 4, screws 4. Records read, they scrap into cloth 3 + leather 1, steel 2 + copper 1, aluminum 2 + screws 2. Amounts are the assistant's. Not checked: whether workbench crafting can consume the Kremvh's Tooth blade mod.

- Backups and the "Scrappy" name: installed 2026-11-27, not yet tested; previous plugin kept as `~/Downloads/PAXTest1.esp.before-backups`.
- In game (owner, 2026-11-27): all four tests pass (three backup recipes with their costs, each makes the normal item, the stitched bear is accepted by the leg recipe, the leg is named "Scrappy Raider Left Leg"). The leg still shows the Overboss placeholder shape, as built.

### Real junk model, step 1: street sign on the left leg (installed 2026-11-27, not yet tested)
- Plan, in steps: street sign; teddy bear; fencing cage and bolts.
- `scripts/nif/writeleg.py` keeps the vanilla `pa_raider_lleg.nif` blocks byte for byte (one skinned `BSTriShape`, five bones) and appends, for the sign: a skinned `BSTriShape` wholly weighted to `LLeg_Thigh` (stored in bone coordinates, identity skin transform), its skin instance and bone data, the sign's shader, texture set and alpha settings; the root node gains one child and new strings go at the end of the table.
- Read-back checks passed (vanilla blocks unchanged, shader strings in range, shape sits at the mockup position on the skeleton); offline preview `~/Downloads/PAX-claw-previews/leg/step1_sign.png`. The bent board shades unevenly in the preview.
- The plugin's leg model mod now points at `PAX\Armor\ScrappyLeftLeg.nif`.
- Previous plugin kept as `~/Downloads/PAXTest1.esp.before-junk-leg`.
- **Step 1 passed in game (owner screenshot, 2026-11-27):** no crash; the Raider leg shows with the sign on the thigh, textured; the leg and bear crafted; on and off several times; the sign stays on the thigh. **A merged junk model works.** In the screenshot the sign reads as a dark rusty board, no lettering visible. Save and reload and a walk check not separately reported.
- Sign fix and step 2 (installed 2026-11-27, not yet tested; previous model kept as `~/Downloads/ScrappyLeftLeg.step1.nif`): the texture `dmndstreetsigns01_d.dds` (in `Fallout4 - Textures4.ba2`; `baunpack` and `ffmpeg` read it) shows the lettered "First St" on the board's -Y face; the +Y face is a plain rusty strip, which is what faced out. The harness piece now faces -Y. The dirty teddy bear (`setdressing\teddybear\toyteddybeardirty01`, no material file, textures in the model) is merged onto `LLeg_Calf`. Offline preview `step2_bear.png`; read-back checks passed. No cage yet.
- **Step 2 in game (owner screenshots, 2026-11-27):** loads; the sign reads green with white lettering; the dirty bear shows textured on the left calf, also while walking. The owner reported a crash in free camera (TFC) after running around. At 20:22 no crash report existed for that session (started 20:19) and `Fallout4.exe` was still running and using CPU, so it reads as a freeze or is unexplained. Cause unknown; the new model is neither implicated nor cleared.
- Crash logs of the day for reference: 08:50 the old claw model fault (fixed); 11:00 and 20:02 both an access violation in `BGSSaveLoadFile::Write` (while saving), naming PAXTest1 only in the plugin list. The 11:00 one predates all crafted pieces and merged models.
- Retest (owner, 2026-11-27, screenshot): no trouble with the Scrappy leg so far.
- A third `BGSSaveLoadFile::Write` crash at 20:35:56 (uptime 3:22, same stack). No save in the Test profile is newer than 19:40. This fault was first seen at 11:00, before any crafted piece or merged model; main Addictol 1.8.0 was installed that morning (08:43) and appears in the stack scan (weak evidence). Next check: Addictol unticked, crash logger kept, make several saves.
- Owner: the 20:35 crash was while quitting with an exit save. No exit save was written (nothing newer than 19:40 in the Test profile saves).
- **Addictol unticked (owner, 2026-11-27): saves work**, including after reloading the game and trying again. Crash logger and Address Library stayed on. Addictol is the likely cause of the `BGSSaveLoadFile::Write` crashes (inferred from this one session; keep it off). **Step 2 passed**: sign and bear on the leg, nothing found against the model.
- **Step 3** (installed 2026-11-27, not yet tested; previous model kept as `~/Downloads/ScrappyLeftLeg.step2.nif`). Owner: the fence could look like the chain on the Overboss. `ChainLleg:0` on `overboss_lleg.nif` uses the base game's `textures\SetDressing\ChainLink` with no material file. `writeleg.py` builds our own ragged band round the calf and bear (36 columns, 22 to 39.5 high, texture density 0.0176 per unit as on the Overboss) and copies that shader (two-sided; vertex-colour flag cleared) and its alpha settings; two bolt heads on the sign use the leg's own material. Building now needs Nuka-World's mesh archive. Preview `step3_cage.png` (shapes only).
- **Step 3 passed in game (owner screenshots, 2026-11-27): "looks good".** The chain-link cage is see-through with the bear inside; the sign shows on the thigh with "rst" readable (the start of the word is not visible in the screenshot) and a bolt at its end. Save, exit save and reload not separately reported. **The Scrappy left leg model is complete.** Not yet committed.

### Scrappy right leg (installed 2026-11-27, not yet tested)
- `build_test1.py` makes both legs from one table: "Scrappy Raider Right Leg" `xx000865` (from `00140C56`), model mod `xx000864`, recipe `xx000866`: aluminum 4, steel 3, cooking pot, hubcap. Previous plugin kept as `~/Downloads/PAXTest1.esp.before-right-leg`; no earlier records changed.
- `writeleg.py --leg right`: frying pan on `RLeg_Thigh`, hubcap and its chain on `RLeg_Calf`; pan strap, bolts and the generated chain links in the leg's metal. The chain makes the model large (about 730 KB, 6,180 chain triangles); thin it if it matters. The left leg's model rebuilds byte for byte.
- Fixed on the way: the shape reader already applies node transforms and the harness applies them again, so turned sources (the hubcap) need their directions turned twice to match.
- Right leg first look (owner screenshot): hubcap and chain show; pan and hubcap both read small; the pan should lie with its round part over the round part of the knee and the handle up the thigh. Second version (installed, not yet tested; previous model kept as `~/Downloads/ScrappyRightLeg.v1.nif`): pan 30 across its length (was 23), centred on the knee's side, handle up, weighted to `RLeg_Thigh` (its round part sits at the knee pivot); hubcap 20 (was 15). Preview `right_leg_v2.png`.
- **Right leg passed in game (owner screenshot, 2026-11-27):** reads better; walking, running, crouching and jumping all fine. Both Scrappy leg models work. In the screenshot the skillet reads pale pink-white (the house pot set's enamel). Not yet committed.

### Scrappy torso (2026-11-27; installed, not yet tested; previous plugin kept as `~/Downloads/PAXTest1.esp.before-torso`)
- "Scrappy Raider Torso" `xx000868` (from `00140C57`), model mod `xx000867`, recipe `xx000869`: aluminum 6, steel 8, plastic 6 (owner: metal, and plastic for the flamingo). As crafted 220 / 270 / 290 (health / armor / energy) with the torso Welded Plate `0018418E`, so 320 / 290 / 290. One combination only: the vanilla record's two extra non-default combinations (adding `PA_Raider_Torso_2`) are left out, as the legs left theirs.
- `writeleg.py --piece torso`: highway sign (both shapes, cut finer to bend) and bolts on `Chest`; lawn flamingo and its chains on `Tank_Armor`. Model about 540 KB. Offline preview `torso.png`. Both leg models rebuild byte for byte.
- **Torso in game (owner screenshots, 2026-11-27):** "Scrappy Raider Torso", 290 / 290 / 300, health 320, weight 24.2, value 110. Loads; flamingo and chains show ("looks fantastic"); both scrappy legs worn with it; the station offers leg mods and names combine ("Overdriven Scrappy Raider Left Leg"). The reported crash did not happen (no new report since 20:35, game still running, Addictol off). Fusion core, torso mods, movement and save/reload not yet reported.
- **No lettering on the chest sign:** the highway sign model has no text. Its second shape is the white border strip (texture row v 0.97 to 1.0). `highwaysignletters_d.dds` is an alphabet atlas (capitals, lower case, digits, arrows), so lettering can be built from our own flat quads.
- Owner (2026-11-27): checked the fusion core and all movement options on the torso (read as fine). Save, exit save and reload not separately reported. Sign wording not chosen.
- Chest sign (owner: "Employees Only"): swapped to the base game's `setdressing\signage\signemployeesonly01` (green, texture stored sideways), width 27, same four bolts, cut finer and bent to the chest (installed, not yet tested; previous model kept as `~/Downloads/ScrappyTorso.v1.nif`). Preview `torso_v2.png`.
- **Torso passed in game (owner screenshot, 2026-11-27): "looks good".** "Employees Only" reads the right way round with the flamingo over the shoulder; all three scrappy pieces on the frame.

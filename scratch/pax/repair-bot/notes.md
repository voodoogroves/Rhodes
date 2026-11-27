# Repair bot (BARB1E)

Later sections replace earlier ones where they say so. Shared goal and rules: [`../common.md`](../common.md).

## BARB1E, a repair follower (owner, 2026-11-27)
- Considered instead of an auto-repair feature.
- A follower, not a full companion. When a power armor piece is below x%, it repairs it with materials it has on hand or a robot repair kit. The player has to give it the materials.
- Target name: Basic Auto Repair Bot -1E (BARB1E).
- Voice: check for existing voice files that can be re-used.
- Open: the x% threshold, material costs, how it is obtained, and the method (likely needs scripts, *inferred*).

## Voice: Automatron bleeps (2026-11-27)
- Owner listened to the converted clips: all sound good, and any of sets A, B or C would work. No set picked.
- Source: `DLCRobot - Voices_en.ba2`, `sound/voice/dlcrobot.esm/dlc01robotcompanionbleep[a|b|c]/<formid>_1.fuz`.
- Each set has 33 lines, 3 per mood, labelled by subtitle such as `(alarmed bleep)`: affirmative, aggressive, alarmed, cheerful, dying, inquisitive, negative, pained, somber, wary, plus plain `(bleeps)`.
- All are in the shared topic `DLC01MasterQuestShared` (quest `DLC01MasterQuest`). The emotion field reads as unset, so the mood comes from the subtitle.
- These are Automatron robot companion voices. Eyebot voice folders checked (`RobotEyeBot`, `RadioVoiceEyebotAnnouncer`, `DLC01MechanistEyebot`) have no mood sets; `RobotEyeBot` has only three non-verbal lines (hit, death, idle), the rest being spoken lines.
- Using these lines would likely make Automatron a requirement (*inferred*). Not checked: how companion dialogue reuses the shared lines.
- Listening copies are local to the Deck, in `~/Downloads/fo4-bleeps/` (`bleep_a/` to `bleep_c/`, `<mood>_<1-3>.wav`). Game audio: never commit it.

## Commands (owner, 2026-11-27)
A narrow, small set of actions.

| When | Choices |
|---|---|
| Active | Stay, Follow, Dismiss, Trade |
| Not active | Join me, Trade, Nevermind |

- Each set fits the four-choice dialogue wheel (*inferred* from Smelly's scene).

## Job (owner, 2026-11-27)
- BARB1E's job differs from Smelly's: patrolling while hunting is not needed. The job is the repair described above.

## Sample: Dog Companion Smelly (2026-11-27)
A companion that takes no follower slot (Nexus file 51617, version 1.1, going by the file name). Read from its records and disassembled scripts; **not run in game**. One sample: what is common across such mods is not yet known. The mod is someone else's work: learn the shape, copy no files.

Light plugin (ESL flag), master `Fallout4.esm` only, five scripts.

**Why no slot:** it runs its own follow system and its scripts never call the vanilla follower scripts. One quest, one alias on the dog, and a quest script variable `Status` that picks the AI package. On hire it also sets player teammate and adds `CurrentCompanionFaction` and `PlayerFriendFaction`; dismiss removes only `CurrentCompanionFaction`. Other logic could treat it as a companion because of that faction (*inferred*): test before copying it.

| Part | How Smelly does it |
|---|---|
| Start | A placed XMarker's `OnCellLoad` starts the quest and enables itself (the dog's enable parent) |
| Actor | Unique, essential NPC |
| Talk | A perk, added at quest start, gives an activate choice "Talk to" (`GetIsID`) that starts a four-choice scene |
| Commands | Dialogue responses set quest stages (the quest allows repeated stages); each stage fragment calls one script function |
| Packages | Conditions use `GetVMQuestVariable` on `Status`: sandbox near the home marker (99 new, 0 sent home), follow (1), travel to own spot to wait (2), patrol (3, 4) |
| Trade | `OpenInventory(True)` on the dog |
| Job | Takes an item from the player, removes the talk perk, starts a 600 s timer, then adds loot to the dog and restores the perk |
| Home | A toy item's `OnLoad` moves the home marker to wherever it is dropped |
| Voice | Own `.wav` files under the plugin's voice folder |

**For BARB1E:**
- Reusable shape: quest, alias, status variable, packages, talk and trade.
- A timed job that takes materials is close to "give it materials and it repairs".
- Not covered by this sample: reading power armor condition, using materials from the bot's own inventory, repairing a piece, and using the Automatron bleeps for its lines.
- Minor bug seen: dialogue accepts any Gwinnett beer, the script takes only Stout.

**More samples worth comparing:** a robot companion that takes no slot; one that acts on its own when a condition is met; a widely used, maintained one (save and reload, getting stuck, fast travel).

## Repair design (2026-11-27)
Adds to "BARB1E, a repair follower" and "Commands"; replaces the active command set there once the dialogue layout is settled.

**Owner, decided:** there is a repair option. If repair cannot happen in combat, the player can talk to BARB1E out of combat and have it repair their power armor.

**Owner, ideas (not locked):**
- Tie it to an Automatron-themed power armor.
- The resource is a robot repair kit (`DLC01RepairKit` `01004F12` in `DLCRobot.esm`) that the player gives to BARB1E.
- When a piece drops below X durability, BARB1E uses a kit to repair it.
- Every X minutes it finds, makes or scavenges another kit; the player can give it more.
- "Repair my armor" uses one kit for each piece not at full.
- Possibly the automatic repair is a perk on the player while BARB1E is joined, like an auto-stimpak, so the bot itself does not do it.

**Assistant suggestions (not decided):**
- Perk version: "Join me" adds the perk, "Dismiss" removes it (also off while staying elsewhere); kits still come from BARB1E's inventory; BARB1E bleeps affirmative on a repair, alarmed when out of kits, wary when a piece is low. The perk would need a script behind it (*inferred*).
- Cap scavenged kits (say 3 to 5); kits the player hands over may exceed the cap.
- The dialogue wheel has four choices: make Stay and Follow one slot that swaps, giving **Stay/Follow, Repair, Dismiss, Trade**.

**Main unknown:** whether a script can read and repair a worn power armor piece's condition.
- No vanilla function found for a worn piece. `GetItemHealthPercent` is on an object reference (such as an item in the world).
- F4SE's script sources have `InstanceData.GetArmorHealth` / `SetArmorHealth`; their wiki pages are blank, and they may be maximum health rather than wear (*unverified*).
- Related lead: [`../perks/power-armor-durability.md`](../perks/power-armor-durability.md).

## More samples (2026-11-27)
Read from files, **none run in game by the assistant**. Reference only: copy no files.

| | Smelly (dog) | Charity, Trix-E1 | Minka (cat) |
|---|---|---|---|
| Own quest and status variable | Yes | Yes | Yes |
| Packages | Home, follow, wait, hunt | Home, follow, wait | Home, follow, wait, cat control |
| Adds `CurrentCompanionFaction` | Yes | Yes | Yes |
| Talk perk | Yes | None seen | Yes |
| Of note | Timed job | Smallest scripts: hire and fire, called from dialogue | Cat control ends if too far or weapon drawn; movable home |

- Common shape: one quest, one alias, a status variable choosing packages, join and dismiss functions that set player teammate and `CurrentCompanionFaction`. Charity and Trix share an author: one example. Trix-E1 is the best minimal template.
- Since all add that faction, it looks less risky than the Smelly section suggests; the vanilla-follower slot test is still worth running.
- Charity ships its own `Form` and `ScriptObject` base scripts, which could interfere with F4SE if they take priority.

**Automatron EyeBot Companions v1.6a** (th1nk, Nexus 11459, masters `Fallout4.esm` and `DLCRobot.esm`):
- Eyebots added to the Automatron robot workbench, mostly equipment. No NPC, dialogue or voice type of its own.
- Its follow packages check the vanilla follower quest, so it likely takes the follower slot (*inferred*): not a model for no-slot following.
- Useful references: eyebot race variants, a keep-your-distance package, a healing cloak (one effect limited to the player; health, not armor), a restore-on-hit script (`RestoreValue`), radio effects, an install message and maintenance holotape.
- Nothing about armor condition seen in the parts checked (not every script was read).

**Assistant suggestions:** depend on Automatron (bleeps, repair kit, eyebot body); build following ourselves in the Trix-E1 / Minka shape; do not require the eyebot mod. Open: whether the plain `DLCRobot.esm` eyebot works as a follower body (race and animations unchecked).

## Next
- A small test script: read a worn power armor piece's condition and repair it.

## Obtaining BARB1E (owner, 2026-11-27)
- **Decided: find and repair.** The player finds a broken eyebot and repairs it; it is not constructed.
- Assistant suggestion: place the wreck near the Rust Devil with the Tesla T-60; activating it asks for a robot repair kit and a few components (such as circuitry), then BARB1E powers up and offers Join me. One placed, unique actor.
- Placing it means a world cell override: check for conflicts (Alexandria `memory/fo4-mod/fo4-world-placement.md`).

## Dialogue tree (2026-11-27; replaces the command table in "Commands")
Assistant proposal, noted at the owner's request. No lines are final.

```
NOT ACTIVE (waiting where found or left)
├─ Join me     -> affirmative bleep -> FOLLOWING
├─ Trade       -> open inventory
├─ Repair      -> see REPAIR
└─ Nevermind   -> generic bleep

FOLLOWING or STAYING
├─ Stay / Follow (one slot, swaps)
│     Stay     -> affirmative -> STAYING
│     Follow   -> cheerful    -> FOLLOWING
├─ Repair      -> see REPAIR
├─ Trade       -> open inventory
└─ Dismiss     -> somber -> NOT ACTIVE (goes home)

REPAIR (1 kit per damaged piece)
├─ Not in power armor, or nothing damaged -> negative
├─ No kits                                -> alarmed
├─ Too few kits: repair worst pieces first -> wary
└─ Enough kits: repair all                 -> cheerful
```

- Repair while not active uses the fourth slot (home repair station); drop it if repairs should require bringing BARB1E along.
- The armor repair test should cover repairing in and out of the suit; the result may change the "not in power armor" branch.

## Player voice (owner, 2026-11-27)
- Find existing player character voice files to use for the player's choices, later; there are plenty of stock ones. Both player voices (male and female) would need a line (*inferred*). Reference them without copying audio into the repo.

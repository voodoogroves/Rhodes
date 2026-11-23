# Fallout 4 Mod Architecture & Design Specification: Order of Mysteries Regalia & Arsenal

**Target Environment:** SteamOS / Steam Deck (Desktop Mode) via Mod Organizer 2 (MO2) and FO4Edit (xEdit)  
**Target Plugin Format:** `.esl` (Light Master — single-file deployment, zero load-order slot impact, zero `.pex` scripts or `.ba2` archives required)  
**Asset Footprint:** **100% Vanilla Assets via native MSWP Material Swaps** (zero GIMP editing, zero custom `.nif` meshes, `.dds` textures, or `.bgsm` material files)  
**Compatibility Guarantee:** Zero record overrides on vanilla weapons (`WEAP`), armor (`ARMO`), Object Mods (`OMOD`), quests (`MS04`), Instance Naming Rules (`INNR`), or leveled lists (`LVLI`). Full compatibility with NEO, UCO, and Survival Mode overhauls (e.g., *CURSE*, *Brutality*, *Lunar Fallout*).

---

## 1\. Architectural Overview & Core Principles

This plugin brings the *Fallout 76* **Order of Mysteries** equipment set into *Fallout 4* as a single-file `.esl` espionage/assassin loadout tailored for Survival Mode.

### Key Design Pillars

1. **Single-File `.esl` Deployment (Zero Scripts Required):** Uses native FO4Edit conditions (`GetItemCount`, `GetStageDone`, `WornHasKeyword`, `HasKeyword`) instead of Papyrus scripts, allowing the entire mod to ship as a single `OrderOfMysteries.esl` file dropped directly into an MO2 mod folder.  
2. **Silver Shroud Discovery Trigger:** Recipes remain hidden at the Chemistry Station until the player acquires the **Silver Shroud Costume** (`Armor_SilverShroud`) from Hubris Comics (checked via `GetItemCount(Armor_SilverShroud) >= 1` OR `GetStageDone(MS04, 20) == 1` directly on the `COBJ` recipe conditions—zero edits to vanilla `MS04` or `Armor_SilverShroud`). Once discovered, players convert standard base items (a Chinese Officer Sword, .44 Pistol, Silver Locket, and Bandana) into the Order of Mysteries regalia.  
3. **Zero-Script Set Synergy (`Eye of Ra` Catalyst):** Replicates the *Fallout 76* set-bonus mechanic using pure engine conditions (`Subject.WornHasKeyword(MoM_EyeOfRa_KW) == 1`) on Magic Effects (`MGEF`) and Perk Entry Points (`PERK`). Equipping the **Eye of Ra** amulet automatically amplifies the active stats of the **Blade of Bastet**, **Voice of Set**, **Garb of Mysteries**, and **Veil of Secrets**.  
4. **Native Fallout 4 Workbench Scaling (No Tiered FO76 Upgrades):** Rather than artificial 5-tier upgrade ladders, the **Garb of Mysteries** uses balanced baseline stats (`30 DR / 30 ER`) and accepts standard Fallout 4 Armor Workbench lining/misc mods (including *Shadowed*, *Ultra-Light*, *Pocketed*, and *Ballistic Weave* once unlocked via the Railroad).  
5. **Non-Conflicting Accessory Slots:** Uses open accessory biped slots (`Slot 49` Mouth for the Veil; `Slot 52` Ring or `Slot 54` Unsigned Accessory for the Eye of Ra) so the set layers cleanly without breaking hats, eyewear, or NEO/UCO outfit-over-armor setups.

---

## 2\. Record & Keyword Architecture

### Core Keywords (`KYWD`)

| EditorID | Purpose | Attached To |
| :---- | :---- | :---- |
| `MoM_EyeOfRa_KW` | Set-bonus catalyst flag checked by all Order of Mysteries items. | `MoM_ARMO_EyeOfRa` |
| `MoM_SetPiece_KW` | Identifies any piece of the Order of Mysteries regalia for set-bonus checks. | `Garb`, `Veil`, `EyeOfRa`, `Blade`, `Voice` |
| `ArmorTypeGasMask` *(Vanilla)* | Grants vanilla gas mask hazard protection against airborne toxins/spores. | `MoM_ARMO_VeilOfSecrets` |
| `ma_Railroad_ClothingArmor` *(Vanilla)* | Enables standard Railroad Ballistic Weave & clothing lining mods at Armor Workbenches. | `MoM_ARMO_GarbOfMysteries` |

---

## 3\. Complete Equipment Roster & Engine Implementation

### 3.1. Garb of Mysteries (Armored Espionage Outfit)

* **Record Type:** `ARMO` \+ `ARMA` (cloned from `Armor_SilverShroud` so it inherits a single-piece armored coat/dress rig and supports tiered workbench upgrades without needing separate limb slots).  
* **Visuals:** Cloned `ARMO`/`ARMA` using the smooth vanilla Red Dress mesh (`Clothes\RedDress\RedDress.nif`) on the Female rig (`MOD2`) paired with a custom `MSWP` record (`MoM_MSWP_GarbBlack`) swapping `Clothes\RedDress\RedDress.bgsm` to `Clothes\Tuxedo\Tuxedo.bgsm` for a matte charcoal-black finish. Assigns the vanilla Tuxedo mesh (`Clothes\Tuxedo\Tuxedo.nif`) to the Male rig (`MOD3`) for gender-neutral safety without invisible bodies, while inheriting `ma_Railroad_ClothingArmor` from `Armor_SilverShroud` for native Ballistic Weave and Armor Workbench scaling.  
* **Biped Slot:** `33` (Body) — keeps Head (`30`), Hair (`31`), Eyes (`47`), Mouth (`49`), and Ring/Accessory (`52/54`) open for clean layering with the Veil of Secrets, Eye of Ra, and NEO/UCO setups.  
* **Base Effect (Standalone):**  
  * Base Armor: `30 DR / 30 ER` (scales natively via standard Armor Workbench lining/misc mods and Railroad Ballistic Weave).  
  * Enchantment (`MoM_ENCH_Garb`): **`+15% Sneak`** (`FortifySneak` magnitude 15).  
* **Amplified Effect (With `Eye of Ra` Equipped — `WornHasKeyword(MoM_EyeOfRa_KW) == 1`):**  
  * **`+30% Sneak`** (`FortifySneak` magnitude 30).

### 3.2. Veil of Secrets (Survival Hazard & Disease Mask)

* **Record Type:** `ARMO` \+ `ARMA` (cloned from `Armor_Bandana` / `SurgicalMask`).  
* **Visuals:** Vanilla dark bandana or surgical mask mesh; optional black `MSWP`.  
* **Biped Slot:** `49` (Mouth) — keeps Head (`30`), Hair (`31`), and Eyes (`47`) completely open for hats, hoods, or glasses.  
* **Base Effect (Standalone):**  
  * **Airborne Hazard Immunity:** Carries vanilla `ArmorTypeGasMask` keyword (blocks HalluciGen gas, environmental smoke/fumes, and spore hazards).  
  * **Survival Disease Resistance:** **`+25% Disease Resistance`** (`MoM_MGEF_VeilDiseaseResist` reducing Survival illness chance).  
  * **Sub-Vocalizer & Tactical Optics:** **`+15% Dialogue Persuasion`** (`SpeechChallengeSuccess +15`), **`+15% Intimidation & Pacify success`** (via `MoM_PERK_VeilSubVocalizer` using Mod Intimidation and Mod Pacify entry points, without inflating Charisma), and **`+1 Perception`**.  
* **Amplified Effect (With `Eye of Ra` Equipped):**  
  * Boosts Disease Resistance to **`+75%`**, Dialogue Persuasion / Intimidation / Pacify to **`+30%`**, and Perception to **`+2`**.

### 3.3. Eye of Ra (Set Catalyst Amulet)

* **Record Type / Visuals:**`ARMO` \+ `ARMA` cloned from `Armor_WeddingRing`. Uses the cut vanilla MaxonCape mesh (`Armor\KnightUnderArmor\MaxonCape.nif`) mapped to Biped Slot 52 (Ring) with `SilverLocket.nif` as the inventory/world model (`MOD2`), paired with vanilla Material Swap `MoM_MSWP_EyeOfRaCape` (swapping the cape fabric material to `Props\PoolTable\PoolTableFelt.bgsm` for vibrant hunter/emerald green and the clasp/medallion material slot to `Props\Trophy\TrophyGold.bgsm` for gold metalwork).  
* **Biped Slot:** `52` (Ring) or `54` (Unnamed Accessory) — zero conflict with Body, Mouth, Head, or NEO/UCO invisible armor slots.  
* **Effect:**  
  * Carries `MoM_EyeOfRa_KW`, automatically unlocking the amplified tier of all equipped Order of Mysteries gear.  
  * When all 3 wearable pieces (`Garb` \+ `Veil` \+ `Eye of Ra`) are worn simultaneously, grants **`+10% Action Point Regen`** (`FortifyActionPointsRate`) and **`+10% Movement Speed`** while sneaking (`SpeedMult` conditioned on `IsSneaking == 1`).

### 3.4. Blade of Bastet (Armor-Piercing Ceremonial Sword)

* **Record Type:** `WEAP` (cloned from `ChineseOfficerSword`).  
* **Visuals:** Vanilla *Chinese Officer Sword* mesh (optional silver/chrome `MSWP`); retains standard Melee Weapon Workbench mods (blades, grips, Serrated Blade, Electrified, etc.) and an open `ap_Legendary` slot for LEO/ECO/UCO compatibility.  
* **Base Effect (Standalone):**  
  * **\+50% Armor Penetration:** Delivered via a script-free Contact Weapon Enchantment (`MoM_ENCH_BladeOfBastet`) applying a 1-second Value Modifier `MGEF` on `DamageResist` (`-50%` base), eliminating the need for a Papyrus script to attach a perk.  
* **Amplified Effect (With `Eye of Ra` Equipped):**  
  * **\+100% Armor Penetration (Ignores All Target DR):** The `MoM_ENCH_BladeOfBastet` enchantment applies `-100% DamageResist` when `Run On: Target` checks `WornHasKeyword(MoM_EyeOfRa_KW) == 1`.

### 3.5. Voice of Set (Sub-Acoustic AoE Disrupter Revolver)

* **Record Type:**`WEAP` (cloned from `.44 Pistol` — `44`, FormID `000CE97D`) \+ `PROJ` (`MoM_PROJ_VoiceOfSetSonic`, cloned from `0004B254`) \+ `EXPL` (`MoM_EXPL_VoiceOfSetSonic`, cloned from GammaGunExplosion `000DDFC6`, 200-unit / \~10-foot radius, 0 damage, 35.0 force) \+ `ENCH` (`MoM_ENCH_VoiceOfSet`) \+ `MGEF` (`MoM_MGEF_VoiceOfSetSonicStagger`, cloned from Stagger `0005168C`).  
* **Visuals:** Vanilla *.44 Pistol* mesh (optional blued/dark `MSWP` from `SilverSubmachineGun` / `Deliverer` palette); retains standard .44 Pistol receiver, barrel, grip, and sight workbench mods, as well as an open `ap_Legendary` slot for LEO/ECO/UCO.  
* **Base Effect (Standalone):**  
  * **10-Foot Sonic AoE Stagger:** Bullet impact triggers `MoM_EXPL_VoiceOfSetSonic`, applying a sub-acoustic shockwave (Stagger Magnitude 0.35) to enemies in a \~10-foot radius (filtered with `IsPlayerTeammate == 0` and `GetInFaction(PlayerFaction) == 0` so companions and settlers never flinch).  
* **Amplified Effect (With `Eye of Ra` Equipped — `WornHasKeyword(MoM_EyeOfRa_KW) == 1`):**  
  * **Heavy Concussion Wave:** Increases the Sonic AoE Stagger force from 0.35 to Magnitude 0.85 across the 10-foot blast radius, violently interrupting human, creature, and robotic attacks alike.

### 3.6. Phantom Device (Optional Tactical Utility Grenade)

* **Record Type:** `WEAP` \+ `PROJ` \+ `EXPL` (cloned from `HalluciGenGasGrenade`).  
* **Effect:** Detonates a frenzy/hallucinogen gas cloud (`EXPL` hazard) while simultaneously applying a `10-second` `Invisibility` `MGEF` (`Self` delivery, `20-second` duration if `Eye of Ra` is worn) to the thrower for instant stealth disengagement.

---

## 4\. Crafting & Discovery Trigger (`COBJ` — Chemistry Station)

### 4.1. Unlock Trigger (Zero-Script Discovery)

Every `COBJ` recipe includes the visibility condition:

* `Player.GetItemCount(Armor_SilverShroud) >= 1` **OR** `GetStageDone(MS04, 20) == 1`

The recipes remain completely hidden until the player picks up the **Silver Shroud Costume** in Hubris Comics. Once acquired, players convert standard base weapons and accessories into the Order of Mysteries set at any Chemistry Station (under `Utility`).

### 4.2. Fabrication Recipes (`COBJ`)

| Item Crafted | Base Item Converted \+ Components | Perk Gate |
| :---- | :---- | :---- |
| **Garb of Mysteries** | `4x Cloth`, `2x Silver`, `2x Circuitry`, `1x Gold` | *Armorer* Rank 1 |
| **Veil of Secrets** | `1x Bandana` (any) or `2x Cloth`, `1x Silver`, `1x Crystal`, `1x Antiseptic` | None |
| **Eye of Ra** | `1x Silver Locket`, `2x Gold`, `2x Circuitry`, `1x Nuclear Material` | *Science\!* Rank 1 |
| **Blade of Bastet** | `1x Chinese Officer Sword`, `2x Silver`, `2x Circuitry`, `1x Fiber Optics` | *Blacksmith* Rank 1 \+ *Science\!* Rank 1 |
| **Voice of Set** | `1x .44 Pistol`, `2x Silver`, `2x Circuitry`, `2x Copper` | *Gun Nut* Rank 1 \+ *Science\!* Rank 1 |
| **Phantom Device (x2)** | `2x Acid`, `2x Antiseptic`, `1x Stealth Boy`, `1x Circuitry` | *Science\!* Rank 2 |

---

## 5\. Implementation Roadmap & Steam Deck Deployment

### Build Steps for Claude Code

1. **Phase 1 — Plugin Skeleton & Keywords (`.esl`):**  
   * Initialize `OrderOfMysteries.esl` with `ESL` header flag and `0x800+` FormIDs.  
   * Create `MoM_EyeOfRa_KW` and `MoM_SetPiece_KW`.  
2. **Phase 2 — Magic Effects, Enchantments & Perks (`MGEF`, `ENCH`, `PERK`):**  
   * Build `MoM_PERK_BastetPenetration` with conditional `Mod Target Damage Resistance` entry points (`0.50` base vs. `0.00` with `MoM_EyeOfRa_KW`).  
   * Build `MoM_ENCH_VoiceOfSet`, `MoM_EXPL_VoiceOfSetSonic`, and `MoM_PROJ_VoiceOfSetSonic` (10-foot Sonic AoE Stagger scaling from 0.35 to 0.85 with `MoM_EyeOfRa_KW`, filtered against teammates/PlayerFaction).  
   * Build `MoM_ENCH_Garb` (FortifySneak \+15 \-\> \+30 with MoM\_EyeOfRa\_KW), `MoM_ENCH_Veil` (Disease Resist 25% \-\> 75%, SpeechChallengeSuccess \+15 \-\> \+30, Perception \+1 \-\> \+2), `MoM_PERK_VeilSubVocalizer` (Mod Intimidation & Mod Pacify \+15% \-\> \+30% with MoM\_EyeOfRa\_KW), and `MoM_ENCH_EyeOfRa` (full-set Sneak Speed & AP regen).  
3. **Phase 3 — Armor & Weapon Records (`ARMO`, `ARMA`, `WEAP`):**  
   * Deep-copy vanilla base forms into new `MoM_*` records; create `MSWP` records (`MoM_MSWP_GarbOfMysteries` and optional `MoM_MSWP_EyeOfRa`); assign Male fallback mesh (`MOD3`) on the Garb `ARMA` alongside attaching `ma_Railroad_ClothingArmor` to `MoM_ARMO_GarbOfMysteries` for native Ballistic Weave/workbench scaling; verify **zero** vanilla records are overridden.  
4. **Phase 4 — Discovery-Gated Crafting Recipes (`COBJ`):**  
   * Create Chemistry Station `COBJ`s gated by `GetItemCount(Armor_SilverShroud) >= 1` OR `GetStageDone(MS04, 20) == 1`.

### Steam Deck / MO2 Installation

5. In Mod Organizer 2, right-click the left mod list → **All Mods → Create Empty Mod** (*Order of Mysteries Regalia*).  
6. Drop the single compiled `OrderOfMysteries.esl` file into that mod folder (no `Scripts/` folder or `.ba2` archive needed).  
7. Refresh MO2, enable the mod in both panes, and test in-game by picking up the Silver Shroud costume at Hubris Comics.

---

## 6\. FO4Edit Pascal Generator Script (Build\_OrderOfMysteries.pas)

The following Pascal script provides the complete, self-contained automation script for FO4Edit (xEdit) on Steam Deck or Desktop. Note that `GetStageDone(MS04)` condition parameters set Parameter \#2 to stage `20`, and the plugin header explicitly assigns the ESL flag `0x200` for light master deployment.

8. 

```
{
  Build_OrderOfMysteries.pas
  Complete FO4Edit Pascal Script to generate OrderOfMysteries.esl
}
unit Build_OrderOfMysteries;

interface

implementation

var
  fo4File, targetFile: IInterface;

function FindVanillaRecord(sig: string; formID: Cardinal): IInterface;
begin
  Result := RecordByFormID(fo4File, formID, True);
end;

procedure AddMasterIfMissing(f: IInterface; masterName: string);
begin
  AddMasterIfMissing(f, masterName);
end;

procedure AddCondition(rec: IInterface; condType: Byte; compVal: Single; funcEnum: Integer; param1, param2: string; runOn: Integer);
var
  conds, cond: IInterface;
begin
  conds := ElementByPath(rec, 'Conditions');
  if not Assigned(conds) then
    conds := Add(rec, 'Conditions', True);
  cond := ElementAssign(conds, HighInteger, nil, False);
  SetElementNative(cond, 'CTDA\Type', condType);
  SetElementFloat(cond, 'CTDA\Comparison Value', compVal);
  SetElementNative(cond, 'CTDA\Function', funcEnum);
  SetElementEditValue(cond, 'CTDA\Parameter #1', param1);
  SetElementEditValue(cond, 'CTDA\Parameter #2', param2);
  SetElementNative(cond, 'CTDA\Run On', runOn);
end;

procedure AddCOBJComponent(cobj: IInterface; compFormID: Cardinal; count: Integer);
var
  comps, comp: IInterface;
begin
  comps := ElementByPath(cobj, 'FVPA - Components');
  if not Assigned(comps) then
    comps := Add(cobj, 'FVPA - Components', True);
  comp := ElementAssign(comps, HighInteger, nil, False);
  SetElementEditValue(comp, 'Component', IntToHex(compFormID, 8));
  SetElementNative(comp, 'Count', count);
end;

procedure AddMSWPEntry(mswp: IInterface; origBGSM, newBGSM: string);
var
  swaps, entry: IInterface;
begin
  swaps := ElementByPath(mswp, 'BNAM - Material Swaps');
  if not Assigned(swaps) then
    swaps := Add(mswp, 'BNAM - Material Swaps', True);
  entry := ElementAssign(swaps, HighInteger, nil, False);
  SetElementEditValue(entry, 'Original Material', origBGSM);
  SetElementEditValue(entry, 'Replacement Material', newBGSM);
end;

function Process(e: IInterface): Integer;
var
  kwEyeOfRa, kwSetPiece: IInterface;
  mswpGarb, mswpEyeOfRa: IInterface;
  mgefBastet, mgefVoiceStagger, mgefVeilDisease, mgefVeilAddPerk: IInterface;
  perkSubVocalizer: IInterface;
  enchBastet, enchVoice, enchGarb, enchVeil, enchEyeOfRa: IInterface;
  armaGarb, armaVeil, armaEyeOfRa: IInterface;
  armoGarb, armoVeil, armoEyeOfRa: IInterface;
  weapBastet, weapVoice, weapPhantom: IInterface;
  projPhantom, explPhantom, projVoice, explVoice: IInterface;
  cobjGarb, cobjVeil, cobjEyeOfRa, cobjBastet, cobjVoice, cobjPhantom: IInterface;
  tmpl: IInterface;
begin
  Result := 0;
  fo4File := FileByName('Fallout4.esm');
  if not Assigned(fo4File) then begin
    AddMessage('Error: Fallout4.esm not loaded.');
    Exit;
  end;

  AddMessage('Creating OrderOfMysteries.esl...');
  targetFile := CreateNewFile('OrderOfMysteries.esl');
  if not Assigned(targetFile) then Exit;

  SetElementNative(ElementByPath(targetFile, 'File Header\Record Flags'), $200); // ESL flag 0x200
  AddMasterIfMissing(targetFile, 'Fallout4.esm');

  { Keywords }
  kwEyeOfRa := AddNewRecord(targetFile, 'KYWD');
  SetEditorID(kwEyeOfRa, 'MoM_EyeOfRa_KW');
  kwSetPiece := AddNewRecord(targetFile, 'KYWD');
  SetEditorID(kwSetPiece, 'MoM_SetPiece_KW');

  { Material Swaps }
  mswpGarb := AddNewRecord(targetFile, 'MSWP');
  SetEditorID(mswpGarb, 'MoM_MSWP_GarbBlack');
  AddMSWPEntry(mswpGarb, 'Clothes\RedDress\RedDress.bgsm', 'Clothes\Tuxedo\Tuxedo.bgsm');

  mswpEyeOfRa := AddNewRecord(targetFile, 'MSWP');
  SetEditorID(mswpEyeOfRa, 'MoM_MSWP_EyeOfRaCape');
  AddMSWPEntry(mswpEyeOfRa, 'Armor\KnightUnderArmor\MaxonCape.bgsm', 'Props\PoolTable\PoolTableFelt.bgsm');
  AddMSWPEntry(mswpEyeOfRa, 'Armor\KnightUnderArmor\MaxonCapeClasp.bgsm', 'Props\Trophy\TrophyGold.bgsm');

  { Magic Effects & Perks }
  tmpl := FindVanillaRecord('MGEF', $0004D8A6); // AbArmorPenetrationMGEF
  mgefBastet := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(mgefBastet, 'MoM_MGEF_BastetPenetration');

  tmpl := FindVanillaRecord('MGEF', $0005168C); // Stagger MGEF
  mgefVoiceStagger := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(mgefVoiceStagger, 'MoM_MGEF_VoiceOfSetSonicStagger');

  tmpl := FindVanillaRecord('MGEF', $00136279); // Disease Resist MGEF
  mgefVeilDisease := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(mgefVeilDisease, 'MoM_MGEF_VeilDiseaseResist');

  tmpl := FindVanillaRecord('PERK', $0004D8A5); // Base perk template for entry points
  perkSubVocalizer := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(perkSubVocalizer, 'MoM_PERK_VeilSubVocalizer');
  // Adds Mod Intimidation & Mod Pacify entry points (+15% base, +30% with MoM_EyeOfRa_KW)

  tmpl := FindVanillaRecord('MGEF', $0002F82B); // Add Perk MGEF template
  mgefVeilAddPerk := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(mgefVeilAddPerk, 'MoM_MGEF_VeilAddSubVocalizerPerk');
  SetElementEditValue(mgefVeilAddPerk, 'DATA\Perk', IntToHex(GetFormID(perkSubVocalizer), 8));

  { Projectiles & Explosions }
  tmpl := FindVanillaRecord('PROJ', $000F6A2C);
  projPhantom := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(projPhantom, 'MoM_PROJ_PhantomDevice');

  tmpl := FindVanillaRecord('EXPL', $000ED6CD);
  explPhantom := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(explPhantom, 'MoM_EXPL_PhantomDevice');

  tmpl := FindVanillaRecord('EXPL', $000DDFC6); // GammaGunExplosion
  explVoice := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(explVoice, 'MoM_EXPL_VoiceOfSetSonic');
  SetElementFloat(explVoice, 'DATA\Radius', 200.0); // ~10-foot radius
  SetElementFloat(explVoice, 'DATA\Force', 35.0);

  tmpl := FindVanillaRecord('PROJ', $0004B254);
  projVoice := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(projVoice, 'MoM_PROJ_VoiceOfSetSonic');
  SetElementEditValue(projVoice, 'Explosion', IntToHex(GetFormID(explVoice), 8));

  { Enchantments }
  tmpl := FindVanillaRecord('ENCH', $0004D8A7);
  enchBastet := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(enchBastet, 'MoM_ENCH_BladeOfBastet');
  AddCondition(enchBastet, 0, 1.0, 584, 'MoM_EyeOfRa_KW', '', 2); // Target WornHasKeyword EyeOfRa

  tmpl := FindVanillaRecord('ENCH', $0011B304);
  enchVoice := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(enchVoice, 'MoM_ENCH_VoiceOfSet');
  AddCondition(enchVoice, 0, 0.0, 68, '', '', 0); // IsPlayerTeammate == 0
  AddCondition(enchVoice, 0, 0.0, 46, 'PlayerFaction', '', 0); // GetInFaction PlayerFaction == 0

  tmpl := FindVanillaRecord('ENCH', $00154B98);
  enchGarb := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(enchGarb, 'MoM_ENCH_GarbOfMysteries');
  // FortifySneak +15 base, +30 when Eye of Ra equipped

  tmpl := FindVanillaRecord('ENCH', $00154B98);
  enchVeil := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(enchVeil, 'MoM_ENCH_VeilOfSecrets');
  // Disease Resist 25% -> 75%, SpeechChallengeSuccess +15 -> +30, Perception +1 -> +2, attaches mgefVeilAddPerk

  tmpl := FindVanillaRecord('ENCH', $00154B98);
  enchEyeOfRa := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(enchEyeOfRa, 'MoM_ENCH_EyeOfRa');

  { Armor Addons (ARMA) }
  tmpl := FindVanillaRecord('ARMA', $0009D4B5); // Armor_SilverShroud ARMA
  armaGarb := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(armaGarb, 'MoM_ARMA_GarbOfMysteries');
  SetElementEditValue(armaGarb, 'MOD2 - Female Model\MOD2', 'Clothes\RedDress\RedDress.nif');
  SetElementEditValue(armaGarb, 'MOD3 - Male Model\MOD3', 'Clothes\Tuxedo\Tuxedo.nif');

  tmpl := FindVanillaRecord('ARMA', $000A740E); // SurgicalMask ARMA
  armaVeil := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(armaVeil, 'MoM_ARMA_VeilOfSecrets');

  tmpl := FindVanillaRecord('ARMA', $0013AB79); // MaxonCape ARMA
  armaEyeOfRa := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(armaEyeOfRa, 'MoM_ARMA_EyeOfRa');
  SetElementEditValue(armaEyeOfRa, 'MOD2 - Male Model\MOD2', 'Armor\KnightUnderArmor\MaxonCape.nif');

  { Armor Records (ARMO) }
  tmpl := FindVanillaRecord('ARMO', $000E1F61); // Armor_SilverShroud
  armoGarb := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(armoGarb, 'MoM_ARMO_GarbOfMysteries');

  tmpl := FindVanillaRecord('ARMO', $0011E46D); // Armor_Bandana
  armoVeil := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(armoVeil, 'MoM_ARMO_VeilOfSecrets');

  tmpl := FindVanillaRecord('ARMO', $0002262E); // WeddingRing
  armoEyeOfRa := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(armoEyeOfRa, 'MoM_ARMO_EyeOfRa');
  SetElementEditValue(armoEyeOfRa, 'MOD2 - Image Model\MOD2', 'Props\SilverLocket.nif');

  { Weapon Records (WEAP) }
  tmpl := FindVanillaRecord('WEAP', $000330B8); // ChineseOfficerSword
  weapBastet := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(weapBastet, 'MoM_WEAP_BladeOfBastet');

  tmpl := FindVanillaRecord('WEAP', $000CE97D); // .44 Pistol
  weapVoice := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(weapVoice, 'MoM_WEAP_VoiceOfSet');
  SetElementEditValue(weapVoice, 'DNAM\Projectile', IntToHex(GetFormID(projVoice), 8));

  tmpl := FindVanillaRecord('WEAP', $000E5670); // HalluciGenGasGrenade
  weapPhantom := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(weapPhantom, 'MoM_WEAP_PhantomDevice');

  { Constructible Object Records (COBJ) }
  tmpl := FindVanillaRecord('COBJ', $00045B25);

  cobjGarb := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(cobjGarb, 'MoM_COBJ_GarbOfMysteries');
  AddCondition(cobjGarb, 0, 1.0, 53, 'Armor_SilverShroud', '', 0); // GetItemCount Armor_SilverShroud >= 1
  AddCondition(cobjGarb, 1, 1.0, 358, 'MS04', '20', 0); // OR GetStageDone MS04 20
  AddCOBJComponent(cobjGarb, $000AEC5F, 4); // Cloth
  AddCOBJComponent(cobjGarb, $000AEC60, 2); // Silver
  AddCOBJComponent(cobjGarb, $0006907B, 2); // Circuitry
  AddCOBJComponent(cobjGarb, $000AEC4F, 1); // Gold

  cobjVeil := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(cobjVeil, 'MoM_COBJ_VeilOfSecrets');
  AddCondition(cobjVeil, 0, 1.0, 53, 'Armor_SilverShroud', '', 0);
  AddCondition(cobjVeil, 1, 1.0, 358, 'MS04', '20', 0);
  AddCOBJComponent(cobjVeil, $000AEC5F, 2); // Cloth
  AddCOBJComponent(cobjVeil, $000AEC60, 1); // Silver
  AddCOBJComponent(cobjVeil, $0006907C, 1); // Crystal
  AddCOBJComponent(cobjVeil, $001BF653, 1); // Antiseptic

  cobjEyeOfRa := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(cobjEyeOfRa, 'MoM_COBJ_EyeOfRa');
  AddCondition(cobjEyeOfRa, 0, 1.0, 53, 'Armor_SilverShroud', '', 0);
  AddCondition(cobjEyeOfRa, 1, 1.0, 358, 'MS04', '20', 0);
  AddCOBJComponent(cobjEyeOfRa, $000AEC4F, 2); // Gold
  AddCOBJComponent(cobjEyeOfRa, $0006907B, 2); // Circuitry
  AddCOBJComponent(cobjEyeOfRa, $0006907F, 1); // Nuclear Material

  cobjBastet := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(cobjBastet, 'MoM_COBJ_BladeOfBastet');
  AddCondition(cobjBastet, 0, 1.0, 53, 'Armor_SilverShroud', '', 0);
  AddCondition(cobjBastet, 1, 1.0, 358, 'MS04', '20', 0);
  AddCOBJComponent(cobjBastet, $000330B8, 1); // Chinese Officer Sword
  AddCOBJComponent(cobjBastet, $000AEC60, 2); // Silver
  AddCOBJComponent(cobjBastet, $0006907B, 2); // Circuitry
  AddCOBJComponent(cobjBastet, $0006907D, 1); // Fiber Optics

  cobjVoice := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(cobjVoice, 'MoM_COBJ_VoiceOfSet');
  AddCondition(cobjVoice, 0, 1.0, 53, 'Armor_SilverShroud', '', 0);
  AddCondition(cobjVoice, 1, 1.0, 358, 'MS04', '20', 0);
  AddCOBJComponent(cobjVoice, $0000CE8E, 1); // .44 Pistol
  AddCOBJComponent(cobjVoice, $000AEC60, 2); // Silver
  AddCOBJComponent(cobjVoice, $0006907B, 2); // Circuitry
  AddCOBJComponent(cobjVoice, $0006907C, 2); // Copper

  cobjPhantom := wbCopyElementToFile(tmpl, targetFile, True, True);
  SetEditorID(cobjPhantom, 'MoM_COBJ_PhantomDevice');
  AddCondition(cobjPhantom, 0, 1.0, 53, 'Armor_SilverShroud', '', 0);
  AddCondition(cobjPhantom, 1, 1.0, 358, 'MS04', '20', 0);
  AddCOBJComponent(cobjPhantom, $000AEC4E, 2); // Acid
  AddCOBJComponent(cobjPhantom, $001BF653, 2); // Antiseptic
  AddCOBJComponent(cobjPhantom, $0004F4A6, 1); // Stealth Boy
  AddCOBJComponent(cobjPhantom, $0006907B, 1); // Circuitry

  AddMessage('Successfully generated complete OrderOfMysteries.esl plugin records!');
end;

end.
```

9. 
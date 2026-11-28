#!/usr/bin/env python3
"""Build the PAX attachment test plugin: wearables that should show on power armor.

A and B are plain apparel; in game the suit refuses them ("you can not equip that in power
armor"). C and D are the same models marked as power armor pieces (ArmorTypePower, with
health). E is the shield itself (PA piece, slot 56): its model is not in the zip; build it with
scripts/nif/placeshield.py --mounts --write and put it at Meshes\\PAX\\Test\\ShieldE.nif in the mod.

    python3 -B build_test1.py [OUT.zip]        default ~/Downloads/PAX-Test1.zip

Round 2, proofs of concept with no scripts:
  F "PAX Shield (proof)": E with armor rating 50, energy 30 and -1 Agility while worn
  Perk PAXSprintProof: sprinting costs no AP while in power armor
  Perk PAXLockProof: in power armor, a locked object offers "PAX: Force Lock" (does nothing)
  Chemistry station recipe: F from a Super Mutant Heavy Gauntlet and one steel

Round 3, ritual claw gauntlet (right arm, slot 53), no scripts:
  "PAX Claw In / Out / Angled": two ritual blades rolled three ways. Build each model with
      scripts/nif/writeclaw.py MESHES ClawRitual<In|Out|Angled>.nif --roll <-90|90|45>
  "PAX Claw Officer" and "PAX Claw Assaultron" (electrified, looks only so far):
      scripts/nif/writeclaw.py MESHES ClawOfficer.nif --claw officer
      scripts/nif/writeclaw.py MESHES ClawAssaultron.nif --claw assaultron_shock
    Put the models at Meshes\\PAX\\Test\\ in the mod.
  While one is worn, a perk doubles unarmed and bash damage (an obvious value, for testing).
  Chemistry station recipe: Claw In from a machete and one steel, gated on the perk
  PAXClawResearch (add it by console; the real research and SPECIAL cost need a script).

Round 4, Raider right arm swap spike, no scripts and no new models:
  Two arm model mods of our own on the vanilla arm model attach point, offered only on items with
  ma_PA_Raider_RArm (the plain Raider right arm and the Overboss one carry it):
  "PAX Spike Arm (T-60 look)" points at the vanilla T-60 right arm so a swap is obvious, and
  "PAX Raider Arm" points back at the vanilla Raider model. Each has a one-steel recipe. The
  question is whether the power armor station offers the slot and what the swap keeps.

Round 5, crafted power armor piece spike, no scripts:
  "Scrappy Raider Left Leg": a new armor piece copied from the vanilla Raider left leg, crafted with
  Welded Plate already on it. Its own values are health 110, armor 130 and energy resistance 150,
  so it comes out at 160 / 150 / 150 (above Raider II, armor just under Overboss). The recipe
  charges the vanilla welding components, steel and a teddy bear. It has its own copy of the power armor naming
  rules so it reads "Scrappy Raider" (English only, read from the game's string table at build time),
  and one combination that fits our own
  leg model mod. That mod points at our own model, the Raider left leg with junk merged in
  (scripts/nif/writeleg.py), put at Meshes\\PAX\\Armor\\ScrappyLeftLeg.nif in the mod.
  Chemistry station recipe.

  "Scrappy Raider Right Leg" is the same from the Raider right leg, its recipe asking for a cooking
  pot and a hubcap; its model goes at Meshes\\PAX\\Armor\\ScrappyRightLeg.nif.

  "Scrappy Raider Torso" likewise from the Raider torso (320 / 290 / 290 welded; six aluminum and
  eight steel and six plastic); its model goes at Meshes\\PAX\\Armor\\ScrappyTorso.nif.

  Backup recipes at the chemistry station make a teddy bear, a cooking pot or a hubcap from many
  more components than they scrap into.

Writes PAXTest1.esp (light; master Fallout4.esm) in a zip that MO2 can install. It holds only
records that point at base game models; the add-perk magic effect's data is copied from
Fallout4.esm at build time. The zip is build output: do not commit it.
"""
import struct
import sys
import zipfile
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts/esp"))
import esp  # noqa: E402

GAME = Path.home() / ".local/share/Steam/steamapps/common/Fallout 4/Data/Fallout4.esm"

FORM_VERSION = 131
HUMAN_RACE, POWER_ARMOR_RACE = 0x00013746, 0x0001D31E
ARMOR_TYPE_POWER = 0x0004D8A1                       # keyword
REDUCE_AGILITY = 0x0004BAD7                         # magic effect abReduceAgility
GAUNTLET, STEEL = 0x00248FD3, 0x0001FABD            # SupermutantArmor0_Arms_Playable, c_Steel
CHEMLAB, RECIPE_UTILITY = 0x00102158, 0x0006980C    # workbench and category keywords
ENERGY = 0x00060A81                                 # damage type
GET_LOCKED, WORN_HAS_KEYWORD = 5, 682               # condition functions
OWN_ENCH, OWN_SPRINT, OWN_LOCK, OWN_RECIPE = 0x01000810, 0x01000811, 0x01000812, 0x01000813
GROUND = r"Actors\Supermutant\CharacterAssets\SMArmor0_ArmsGO.nif"
# The ground model's bounds and preview transform, as on the vanilla item 00248FD3 that uses it.
GROUND_BOUNDS = struct.pack("<6h", -23, -25, -1, 24, 25, 24)
GROUND_PREVIEW = 0x0022FD4B
MUTANT_ARMS = r"Actors\Supermutant\CharacterAssets\SMArmor0_Arms.nif"
X01_ARM = r"Actors\PowerArmor\CharacterAssets\Mods\PA_X1_LArm.nif"
SHIELD = r"PAX\Test\ShieldE.nif"
# The shield items' dropped and preview model: the vanilla one with only the plated gauntlet,
# made with scripts/nif/trimparts.py --keep 1 and put at Meshes\PAX\Test\ShieldGO.nif.
SHIELD_GROUND = r"PAX\Test\ShieldGO.nif"
SHIELD_BOUNDS = struct.pack("<6h", -13, -26, -2, 25, 25, 25)
ITEMS = [  # editor id, name, body slot, worn model, power armor piece; append only (form IDs)
    ("PAXTestA", "PAX Test A (mutant arms)", 56, MUTANT_ARMS, False),
    ("PAXTestB", "PAX Test B (X-01 left arm)", 57, X01_ARM, False),
    ("PAXTestC", "PAX Test C (mutant arms, PA piece)", 56, MUTANT_ARMS, True),
    ("PAXTestD", "PAX Test D (X-01 left arm, PA piece)", 57, X01_ARM, True),
    ("PAXTestE", "PAX Test E (left arm shield)", 56, SHIELD, True),
    ("PAXShieldProof", "PAX Shield (proof)", 56, SHIELD, True),
]
PROOF = "PAXShieldProof"                            # the item with protection and a drawback


def sub(tag, data):
    return tag.encode() + struct.pack("<H", len(data)) + data


def text(tag, value):
    return sub(tag, value.encode("ascii") + b"\0")


def u32(tag, value):
    return sub(tag, struct.pack("<I", value))


def record(tag, formid, body, flags=0):
    return tag.encode() + struct.pack("<IIIIHH", len(body), flags, formid, 0, FORM_VERSION, 0) + body


def group(tag, records):
    body = b"".join(records)
    return b"GRUP" + struct.pack("<I4sIII", len(body) + 24, tag.encode(), 0, 0, 0) + body


def condition(function, parameter):
    """True (== 1) for the object the condition runs on."""
    return sub("CTDA", struct.pack("<B3xfH2xIIIIi", 0, 1.0, function, parameter, 0, 0, 0, -1))


def perk(formid, edid, name, description, entry, function, tabs, value_type, value):
    """A hidden one-rank perk with one entry point. tabs: list of condition lists."""
    body = [text("EDID", edid), text("FULL", name), text("DESC", description),
            sub("DATA", bytes((0, 0, 1, 0, 1))), sub("PRKE", bytes((2, 0, 0))),
            sub("DATA", bytes((entry, function, len(tabs))))]
    for number, conditions in enumerate(tabs):
        if conditions:
            body += [sub("PRKC", bytes((number,)))] + conditions
    body += [sub("EPFT", bytes((value_type,))), sub("EPFB", bytes(2))] + value + [sub("PRKF", b"")]
    return record("PERK", formid, b"".join(body))


def extras():
    drawback = record("ENCH", OWN_ENCH, b"".join([
        text("EDID", "PAXShieldDrawback"), sub("OBND", bytes(12)), text("FULL", "Heavy Shield"),
        sub("ENIT", struct.pack("<9I", 0, 0, 0, 0, 0, 6, 0, 0, 0)),   # as EnchClothingAgility
        u32("EFID", REDUCE_AGILITY), sub("EFIT", struct.pack("<fII", 1.0, 0, 0))]))
    in_suit = [condition(WORN_HAS_KEYWORD, ARMOR_TYPE_POWER)]
    perks = [
        perk(OWN_SPRINT, "PAXSprintProof", "PAX Sprint Proof", "Sprinting costs no AP in power armor.",
             96, 3, [in_suit], 1, [sub("EPFD", struct.pack("<f", 0.0))]),
        perk(OWN_LOCK, "PAXLockProof", "PAX Lock Proof", "Prompt test.",
             14, 9, [in_suit, [condition(GET_LOCKED, 0)]], 4,
             [text("EPF2", "PAX: Force Lock"), sub("EPF3", bytes(2))])]
    shield = 0x01000800 + 2 * [i[0] for i in ITEMS].index(PROOF)
    recipe = record("COBJ", OWN_RECIPE, b"".join([
        text("EDID", "PAXShieldRecipe"), sub("FVPA", struct.pack("<4I", GAUNTLET, 1, STEEL, 1)),
        text("DESC", "A power armor shield cut from a super mutant gauntlet."),
        u32("CNAM", shield), u32("BNAM", CHEMLAB), u32("FNAM", RECIPE_UTILITY),
        u32("INTV", 1)]))
    return drawback, perks, recipe


CLAW_SLOT = 53
CLAWS = [  # name, worn model, dropped model, its bounds; append only (form IDs from 0x820)
    ("In", "ClawRitualIn", None, None),
    ("Out", "ClawRitualOut", None, None),
    ("Angled", "ClawRitualAngled", None, None),
    ("Officer", "ClawOfficer", r"Weapons\ChineseOfficerSword\SerratedBladeShock.nif", (-2, -6, -1, 3, 55, 3)),
    ("Assaultron", "ClawAssaultron", r"DLC01\Weapons\AssaultronBlade\ElectroBlade.nif", (-3, 8, -1, 3, 54, 1)),
]
OWN_CLAW_EFFECT, OWN_CLAW_ENCH, OWN_CLAW_PERK = 0x01000830, 0x01000831, 0x01000832
OWN_RESEARCH, OWN_CLAW_RECIPE = 0x01000833, 0x01000834
UNARMED, MACHETE = 0x0005240E, 0x00033FE0           # WeaponTypeUnarmed, Machete
ATTACK_DAMAGE, BASH_DAMAGE = 35, 26                 # perk entry points, as Iron Fist and Basher
HAS_PERK, HAS_KEYWORD = 448, 560                    # condition functions
ADD_PERK_EFFECT, ADD_PERK_ENCH = 0x001F4423, 0x001F4425   # vanilla chain to copy
VANILLA_PERK = struct.pack("<I", 0x001F4166)
CLAW_GROUND = r"Weapons\Machete\SacrificalBlade.nif"
CLAW_BOUNDS = struct.pack("<6h", -4, -3, -1, 5, 40, 1)
CLAW_PREVIEW = 0x00020D51                           # the machete's preview transform
DAMAGE = 2.0


def claws():
    """Records for the claw items, by type."""
    vanilla = {formid: dict(fields) for _, formid, fields in esp.records(str(GAME), {"MGEF", "ENCH"})
               if formid in (ADD_PERK_EFFECT, ADD_PERK_ENCH)}
    data = vanilla[ADD_PERK_EFFECT]["DATA"]
    if data.count(VANILLA_PERK) != 1:
        raise SystemExit("FAIL: the vanilla add-perk effect is not as expected")
    effect = record("MGEF", OWN_CLAW_EFFECT, b"".join([
        text("EDID", "PAXClawAddPerk"), text("FULL", "PAX Claw"),
        sub("DATA", data.replace(VANILLA_PERK, struct.pack("<I", OWN_CLAW_PERK))),
        sub("SNDD", b""), sub("DNAM", bytes(4))]))
    ench = record("ENCH", OWN_CLAW_ENCH, b"".join([
        text("EDID", "PAXClawEnch"), sub("OBND", bytes(12)), text("FULL", "Claw Gauntlet"),
        sub("ENIT", vanilla[ADD_PERK_ENCH]["ENIT"]),
        u32("EFID", OWN_CLAW_EFFECT), sub("EFIT", struct.pack("<fII", 0.0, 0, 0))]))
    in_suit = [condition(WORN_HAS_KEYWORD, ARMOR_TYPE_POWER)]
    entries = [(ATTACK_DAMAGE, [in_suit, [condition(HAS_KEYWORD, UNARMED)], []]),
               (BASH_DAMAGE, [in_suit, []])]
    body = [text("EDID", "PAXClawPerk"), text("FULL", "PAX Claw"),
            text("DESC", "Punches and bashes hit harder."), sub("DATA", bytes((0, 0, 1, 0, 1)))]
    for number, (entry, tabs) in enumerate(entries):
        body += [sub("PRKE", bytes((2, 0, 0))), sub("DATA", bytes((entry, 3, len(tabs))))]
        for tab, conditions in enumerate(tabs):
            if conditions:
                body += [sub("PRKC", bytes((tab,)))] + conditions
        body += [sub("EPFT", b"\x01"), sub("EPFB", struct.pack("<H", number)),
                 sub("EPFD", struct.pack("<f", DAMAGE)), sub("PRKF", b"")]
    damage = record("PERK", OWN_CLAW_PERK, b"".join(body))
    research = record("PERK", OWN_RESEARCH, b"".join([
        text("EDID", "PAXClawResearch"), text("FULL", "PAX Claw Research"),
        text("DESC", "You know how to build a claw gauntlet."), sub("DATA", bytes((0, 0, 1, 0, 1)))]))
    armor, addons = [], []
    for n, (variant, worn, ground, bounds) in enumerate(CLAWS):
        armo, arma = 0x01000820 + 2 * n, 0x01000821 + 2 * n
        slots = u32("BOD2", 1 << (CLAW_SLOT - 30))
        model = "PAX\\Test\\%s.nif" % worn
        armor.append(record("ARMO", armo, b"".join([
            text("EDID", "PAXClaw" + variant), sub("OBND", struct.pack("<6h", *bounds) if bounds else CLAW_BOUNDS), u32("PTRN", CLAW_PREVIEW),
            text("FULL", "PAX Claw " + variant), u32("EITM", OWN_CLAW_ENCH), text("MOD2", ground or CLAW_GROUND),
            slots, u32("RNAM", HUMAN_RACE), u32("KSIZ", 1) + u32("KWDA", ARMOR_TYPE_POWER),
            text("DESC", ""), sub("INDX", bytes(2)), u32("MODL", arma),
            sub("DATA", struct.pack("<IfI", 0, 0.0, 100)), sub("FNAM", struct.pack("<HHI", 0, 0, 0))])))
        addons.append(record("ARMA", arma, b"".join([
            text("EDID", "PAXClaw%sAA" % variant), slots, u32("RNAM", HUMAN_RACE), sub("DNAM", bytes(12)),
            text("MOD2", model), text("MOD3", model), u32("MODL", POWER_ARMOR_RACE)])))
    recipe = record("COBJ", OWN_CLAW_RECIPE, b"".join([
        text("EDID", "PAXClawRecipe"), sub("FVPA", struct.pack("<4I", MACHETE, 1, STEEL, 1)),
        text("DESC", "A claw gauntlet built around a ritual blade."), condition(HAS_PERK, OWN_RESEARCH),
        u32("CNAM", 0x01000820), u32("BNAM", CHEMLAB), u32("FNAM", RECIPE_UTILITY), u32("INTV", 1)]))
    return {"MGEF": [effect], "ENCH": [ench], "ARMO": armor, "ARMA": addons, "COBJ": [recipe],
            "PERK": [damage, research]}


RAIDER_ARM_MOD, T60_ARM_MOD = 0x00137B7F, 0x00055F93  # OMOD PA_Raider_RArm, PA_T60_RArm
RAIDER_RIGHT_ARM = 0x00184180                       # keyword ma_PA_Raider_RArm
ARM_ATTACH_POINT = 0x00055F8E                       # ap_PowerArmor_RArmMod
ARM_SWAPS = [  # editor id, name, vanilla mod whose model it uses; append only (form IDs from 0x850)
    ("PAXSpikeArm", "PAX Spike Arm (T-60 look)", T60_ARM_MOD),
    ("PAXRaiderArm", "PAX Raider Arm", RAIDER_ARM_MOD),
]


def arm_swaps():
    """Arm model mods and their recipes. DATA is the vanilla Raider arm mod's, unchanged, so the
    attach point, child slots and added keywords match; only the model differs."""
    vanilla = {formid: dict(fields) for _, formid, fields in esp.records(str(GAME), {"OMOD"})
               if formid in (RAIDER_ARM_MOD, T60_ARM_MOD)}
    data = vanilla[RAIDER_ARM_MOD]["DATA"]
    if struct.unpack_from("<I", data, 16)[0] != ARM_ATTACH_POINT:
        raise SystemExit("FAIL: the vanilla Raider arm mod is not on the expected attach point")
    mods, recipes = [], []
    for n, (edid, name, source) in enumerate(ARM_SWAPS):
        omod, cobj = 0x01000850 + 2 * n, 0x01000851 + 2 * n
        mods.append(record("OMOD", omod, b"".join([
            text("EDID", edid), text("FULL", name), text("DESC", "Arm swap test."),
            sub("MODL", vanilla[source]["MODL"]), sub("DATA", data),
            u32("MNAM", RAIDER_RIGHT_ARM)])))
        recipes.append(record("COBJ", cobj, b"".join([
            text("EDID", edid + "Recipe"), sub("FVPA", struct.pack("<2I", STEEL, 1)),
            text("DESC", ""), u32("CNAM", omod), u32("INTV", 1)])))
    return mods, recipes


RAIDER_LEFT_LEG, RAIDER_LEG_MOD = 0x00140C55, 0x00137B7E   # ARMO, OMOD PA_Raider_LLeg
LEG_LINING, LEG_PAINT = 0x0018418B, 0x00077D3A      # Welded Plate, and the vanilla leg's null mod
LEG_STEEL = 3                                       # test amount, beside the welding aluminum
TEDDY_BEAR = 0x00059B14                             # MISC TeddyBear, the junk this leg wears
# Our model: build it with scripts/nif/writeleg.py and put it at this path under Meshes in the mod.
SPIKE_LEG_MODEL = r"PAX\Armor\ScrappyLeftLeg.nif"
OWN_LEG_MOD, OWN_LEG, OWN_LEG_RECIPE = 0x01000860, 0x01000861, 0x01000862
LEG_HEALTH, LEG_ARMOR, LEG_ENERGY = 110, 130, 150  # as crafted, before the lining
LEG_NAME = "Scrappy Raider Left Leg"
PA_NAMING, OWN_NAMING = 0x00188160, 0x01000863     # INNR dn_PowerArmor and our copy of it
NAME_SWAPS = {"Raider Power": "Scrappy Raider", "Raider Power II": "Scrappy Raider"}
INTERFACE = GAME.with_name("Fallout4 - Interface.ba2")


def english_strings():
    """The base game's English string table, {id: text}, read from the interface archive."""
    with open(INTERFACE, "rb") as f:
        magic, _, kind, count, names_at = struct.unpack("<4sI4sIQ", f.read(24))
        if magic != b"BTDX" or kind != b"GNRL":
            raise SystemExit("FAIL: unexpected interface archive")
        entries = [struct.unpack("<I4sIIQIII", f.read(36)) for _ in range(count)]
        f.seek(names_at)
        names = [f.read(struct.unpack("<H", f.read(2))[0]).decode("latin1").lower() for _ in range(count)]
        entry = entries[names.index("strings\\fallout4_en.strings")]
        offset, packed, size = entry[4], entry[5], entry[6]
        f.seek(offset)
        data = zlib.decompress(f.read(packed)) if packed else f.read(size)
    total = struct.unpack_from("<I", data)[0]
    start = 8 + 8 * total
    out = {}
    for i in range(total):
        key, at = struct.unpack_from("<II", data, 8 + 8 * i)
        out[key] = data[start + at:data.index(b"\0", start + at)]
    return out


def naming():
    """Our copy of the power armor naming rules, with the Raider words changed."""
    words = english_strings()
    fields = next(fields for _, formid, fields in esp.records(str(GAME), {"INNR"}) if formid == PA_NAMING)
    body, swapped = [], set()
    for tag, data in fields:
        if tag == "EDID":
            body.append(text("EDID", "PAXScrapNaming"))
        elif tag == "WNAM":
            word = words.get(struct.unpack("<I", data)[0], b"")
            old = word.decode("cp1252")
            if old in NAME_SWAPS:
                swapped.add(old)
                word = NAME_SWAPS[old].encode("cp1252")
            body.append(sub("WNAM", word + b"\0"))
        else:
            body.append(sub(tag, data))
    if swapped != set(NAME_SWAPS):
        raise SystemExit("FAIL: the naming rules do not hold the Raider words")
    return record("INNR", OWN_NAMING, b"".join(body))


RIGHT_LEG_MODEL = r"PAX\Armor\ScrappyRightLeg.nif"
PLASTIC = 0x0001FAB7                                # component, for the flamingo
COOKING_POT, HUBCAP = 0x00059ABA, 0x0007E941        # the right leg's junk (it wears a frying pan)
# health, armor, energy as crafted; welded-lining mod; vanilla welding recipe; extra steel
LIMB = (LEG_HEALTH, LEG_ARMOR, LEG_ENERGY, LEG_LINING, "co_PA_Raider_Leg_Lining_B", LEG_STEEL)
TORSO = (220, 270, 290, 0x0018418E, "co_PA_Raider_Torso_Lining_B", 8)   # 320 / 290 / 290 welded
LEGS = [  # records (model mod, piece, recipe), vanilla piece and its mod, our model, editor ids, name, junk
    ((OWN_LEG_MOD, OWN_LEG, OWN_LEG_RECIPE), RAIDER_LEFT_LEG, RAIDER_LEG_MOD, SPIKE_LEG_MODEL,
     ("PAXScrapLegModel", "PAXScrapLegLeft", "PAXScrapLegRecipe"), LEG_NAME,
     ((TEDDY_BEAR, 1),), LIMB),
    ((0x01000864, 0x01000865, 0x01000866), 0x00140C56, 0x00137B80, RIGHT_LEG_MODEL,
     ("PAXScrapLegModelRight", "PAXScrapLegRight", "PAXScrapLegRecipeRight"),
     "Scrappy Raider Right Leg", ((COOKING_POT, 1), (HUBCAP, 1)), LIMB),
    # The torso wears a road sign and a lawn flamingo, which are no inventory items: metal for the
    # sign and plastic for the bird.
    ((0x01000867, 0x01000868, 0x01000869), 0x00140C57, 0x00137B7C, r"PAX\Armor\ScrappyTorso.nif",
     ("PAXScrapTorsoModel", "PAXScrapTorso", "PAXScrapTorsoRecipe"),
     "Scrappy Raider Torso", ((PLASTIC, 6),), TORSO),
]


def crafted_leg(ids, piece, vanilla_mod, model, edids, name, junk, stats):
    """A new leg or torso, its model mod and its recipe."""
    own_mod, own, own_recipe = ids
    health_, armor_, energy_, lining, weld_recipe, steel = stats
    def vanilla(kind, wanted):
        return next(fields for _, formid, fields in esp.records(str(GAME), {kind}) if formid == wanted)
    mod = dict(vanilla("OMOD", vanilla_mod))
    omod = record("OMOD", own_mod, b"".join([
        text("EDID", edids[0]), text("FULL", "Scrap Leg Frame"), text("DESC", ""),
        text("MODL", model), sub("DATA", mod["DATA"])]))
    # One default combination: no keywords, three included mods (7 bytes each).
    combination = (struct.pack("<II", 3, 0) + bytes(4) + struct.pack("<hBBH", -1, 1, 0, 0)
                   + b"".join(struct.pack("<IBBB", m, 0, 0, 1) for m in (own_mod, lining, LEG_PAINT)))
    body, seen = [], set()
    for tag, data in vanilla("ARMO", piece):
        seen.add(tag)
        if tag == "EDID":
            body.append(text("EDID", edids[1]))
        elif tag == "FULL":
            body.append(text("FULL", name))
        elif tag == "DESC":
            body.append(text("DESC", ""))
        elif tag == "DATA":
            value, weight, health = struct.unpack("<IfI", data)
            body.append(sub(tag, struct.pack("<IfI", value, weight, health_)))
        elif tag == "FNAM":
            body.append(sub(tag, struct.pack("<H", armor_) + data[2:]))
        elif tag == "DAMA":
            pairs = [struct.unpack_from("<II", data, i) for i in range(0, len(data), 8)]
            body.append(sub(tag, b"".join(struct.pack("<II", kind, energy_
                                                      if kind == ENERGY else amount) for kind, amount in pairs)))
        elif tag == "INRD":
            body.append(u32("INRD", OWN_NAMING))
        elif tag == "OBTE":
            body += [u32("OBTE", 1), sub("OBTS", combination)]
        elif tag != "OBTS":
            body.append(sub(tag, data))
    if not {"DATA", "FNAM", "DAMA", "OBTE", "STOP"} <= seen:
        raise SystemExit("FAIL: the vanilla Raider leg record is not as expected")
    armo = record("ARMO", own, b"".join(body))
    # The cost of welding it: the components of the vanilla Welded Plate recipe, plus steel.
    weld = next((dict(fields)["FVPA"] for _, _, fields in esp.records(str(GAME), {"COBJ"})
                 if esp.edid(fields) == weld_recipe), None)
    if weld is None:
        raise SystemExit("FAIL: the vanilla welding recipe was not found")
    parts = struct.pack("<2I", STEEL, steel) + b"".join(struct.pack("<2I", *item) for item in junk)
    recipe = record("COBJ", own_recipe, b"".join([
        text("EDID", edids[2]), sub("FVPA", weld + parts),
        text("DESC", "Spike: a crafted power armor piece."), u32("CNAM", own),
        u32("BNAM", CHEMLAB), u32("FNAM", RECIPE_UTILITY), u32("INTV", 1)]))
    return omod, armo, recipe


COPPER, LEATHER, CLOTH = 0x0001FA9C, 0x0001FAAE, 0x001223C7        # components
ADHESIVE, ALUMINUM, SCREWS = 0x0001FAA5, 0x0001FA91, 0x0003D294
# Backup recipes for the junk the scrappy pieces ask for, in case it gets scrapped. Each costs
# several times what the item scraps into, so finding one stays the better deal.
BACKUPS = [  # editor id, vanilla item made, cost; append only (form IDs from 0x870)
    ("PAXStitchTeddy", TEDDY_BEAR, ((CLOTH, 10), (LEATHER, 3), (ADHESIVE, 3))),   # scraps: cloth 3, leather 1
    ("PAXHammerPot", 0x00059ABA, ((STEEL, 10), (COPPER, 3))),                     # scraps: steel 2, copper 1
    ("PAXHammerHubcap", 0x0007E941, ((ALUMINUM, 8), (STEEL, 4), (SCREWS, 4))),    # scraps: aluminum 2, screws 2
]


def backups():
    return [record("COBJ", 0x01000870 + n, b"".join([
        text("EDID", edid), sub("FVPA", b"".join(struct.pack("<2I", *part) for part in cost)),
        text("DESC", "A stand-in for one lost to the scrap pile."), u32("CNAM", item),
        u32("BNAM", CHEMLAB), u32("FNAM", RECIPE_UTILITY), u32("INTV", 1)]))
        for n, (edid, item, cost) in enumerate(BACKUPS)]


def build():
    armor, addons = [], []
    for n, (edid, name, slot, model, piece) in enumerate(ITEMS):
        armo, arma = 0x01000800 + 2 * n, 0x01000801 + 2 * n   # 01: our own records (one master)
        slots = u32("BOD2", 1 << (slot - 30))
        keywords = u32("KSIZ", 1) + u32("KWDA", ARMOR_TYPE_POWER) if piece else b""
        armor.append(record("ARMO", armo, b"".join([
            text("EDID", edid), sub("OBND", SHIELD_BOUNDS if model == SHIELD else GROUND_BOUNDS), u32("PTRN", GROUND_PREVIEW), text("FULL", name),
            u32("EITM", OWN_ENCH) if edid == PROOF else b"", text("MOD2", SHIELD_GROUND if model == SHIELD else GROUND),
            slots, u32("RNAM", HUMAN_RACE), keywords, text("DESC", ""), sub("INDX", bytes(2)), u32("MODL", arma),
            sub("DATA", struct.pack("<IfI", 0, 0.0, 100 if piece else 0)), sub("FNAM", struct.pack("<HHI", 50 if edid == PROOF else 0, 0, 0)),
            sub("DAMA", struct.pack("<II", ENERGY, 30)) if edid == PROOF else b""])))
        addons.append(record("ARMA", arma, b"".join([
            text("EDID", edid + "AA"), slots, u32("RNAM", HUMAN_RACE), sub("DNAM", bytes(12)),
            text("MOD2", model), text("MOD3", model), u32("MODL", POWER_ARMOR_RACE)])))
    drawback, perks, recipe = extras()
    claw = claws()
    swaps, swap_recipes = arm_swaps()
    leg_mods, legs, leg_recipes = map(list, zip(*(crafted_leg(*spec) for spec in LEGS)))
    groups = [("MGEF", claw["MGEF"]), ("ENCH", [drawback] + claw["ENCH"]), ("ARMO", armor + claw["ARMO"] + legs),
              ("ARMA", addons + claw["ARMA"]), ("COBJ", [recipe] + claw["COBJ"] + swap_recipes + leg_recipes + backups()),
              ("PERK", perks + claw["PERK"]), ("OMOD", swaps + leg_mods), ("INNR", [naming()])]
    count = sum(len(r) for _, r in groups) + len(groups)        # records and groups
    header = record("TES4", 0, b"".join([
        sub("HEDR", struct.pack("<fiI", 1.0, count, 0x880)), text("CNAM", "PAX test"),
        text("MAST", "Fallout4.esm"), sub("DATA", bytes(8))]), flags=0x200)
    return header + b"".join(group(tag, records) for tag, records in groups)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Downloads/PAX-Test1.zip"
    if out.exists():
        sys.exit("%s exists; remove it or name another file" % out)
    with zipfile.ZipFile(out, "x", zipfile.ZIP_DEFLATED) as z:
        z.writestr("PAXTest1.esp", build())
    print(out)

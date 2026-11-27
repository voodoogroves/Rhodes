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

Writes PAXTest1.esp (light; master Fallout4.esm) in a zip that MO2 can install. It holds only
records that point at base game models; the add-perk magic effect's data is copied from
Fallout4.esm at build time. The zip is build output: do not commit it.
"""
import struct
import sys
import zipfile
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
    groups = [("MGEF", claw["MGEF"]), ("ENCH", [drawback] + claw["ENCH"]), ("ARMO", armor + claw["ARMO"]),
              ("ARMA", addons + claw["ARMA"]), ("COBJ", [recipe] + claw["COBJ"]), ("PERK", perks + claw["PERK"])]
    count = sum(len(r) for _, r in groups) + len(groups)        # records and groups
    header = record("TES4", 0, b"".join([
        sub("HEDR", struct.pack("<fiI", 1.0, count, 0x860)), text("CNAM", "PAX test"),
        text("MAST", "Fallout4.esm"), sub("DATA", bytes(8))]), flags=0x200)
    return header + b"".join(group(tag, records) for tag, records in groups)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Downloads/PAX-Test1.zip"
    if out.exists():
        sys.exit("%s exists; remove it or name another file" % out)
    with zipfile.ZipFile(out, "x", zipfile.ZIP_DEFLATED) as z:
        z.writestr("PAXTest1.esp", build())
    print(out)

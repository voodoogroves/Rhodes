#!/usr/bin/env python3
"""Build the PAX attachment test plugin: wearables that should show on power armor.

A and B are plain apparel; in game the suit refuses them ("you can not equip that in power
armor"). C and D are the same models marked as power armor pieces (ArmorTypePower, with
health). E is the shield itself (PA piece, slot 56): its model is not in the zip; build it with
scripts/nif/placeshield.py --write and put it at Meshes\\PAX\\Test\\ShieldE.nif in the mod.

    python3 -B build_test1.py [OUT.zip]        default ~/Downloads/PAX-Test1.zip

Writes PAXTest1.esp (light; master Fallout4.esm) in a zip that MO2 can install. It holds only
records that point at base game models. The zip is build output: do not commit it.
"""
import struct
import sys
import zipfile
from pathlib import Path

FORM_VERSION = 131
HUMAN_RACE, POWER_ARMOR_RACE = 0x00013746, 0x0001D31E
ARMOR_TYPE_POWER = 0x0004D8A1                       # keyword
GROUND = r"Actors\Supermutant\CharacterAssets\SMArmor0_ArmsGO.nif"
MUTANT_ARMS = r"Actors\Supermutant\CharacterAssets\SMArmor0_Arms.nif"
X01_ARM = r"Actors\PowerArmor\CharacterAssets\Mods\PA_X1_LArm.nif"
SHIELD = r"PAX\Test\ShieldE.nif"
ITEMS = [  # editor id, name, body slot, worn model, power armor piece; append only (form IDs)
    ("PAXTestA", "PAX Test A (mutant arms)", 56, MUTANT_ARMS, False),
    ("PAXTestB", "PAX Test B (X-01 left arm)", 57, X01_ARM, False),
    ("PAXTestC", "PAX Test C (mutant arms, PA piece)", 56, MUTANT_ARMS, True),
    ("PAXTestD", "PAX Test D (X-01 left arm, PA piece)", 57, X01_ARM, True),
    ("PAXTestE", "PAX Test E (left arm shield)", 56, SHIELD, True),
]


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


def build():
    armor, addons = [], []
    for n, (edid, name, slot, model, piece) in enumerate(ITEMS):
        armo, arma = 0x01000800 + 2 * n, 0x01000801 + 2 * n   # 01: our own records (one master)
        slots = u32("BOD2", 1 << (slot - 30))
        keywords = u32("KSIZ", 1) + u32("KWDA", ARMOR_TYPE_POWER) if piece else b""
        armor.append(record("ARMO", armo, b"".join([
            text("EDID", edid), sub("OBND", bytes(12)), text("FULL", name), text("MOD2", GROUND),
            slots, u32("RNAM", HUMAN_RACE), keywords, text("DESC", ""), sub("INDX", bytes(2)), u32("MODL", arma),
            sub("DATA", struct.pack("<IfI", 0, 0.0, 100 if piece else 0)), sub("FNAM", bytes(8))])))
        addons.append(record("ARMA", arma, b"".join([
            text("EDID", edid + "AA"), slots, u32("RNAM", HUMAN_RACE), sub("DNAM", bytes(12)),
            text("MOD2", model), text("MOD3", model), u32("MODL", POWER_ARMOR_RACE)])))
    count = len(armor) + len(addons) + 2                        # records and groups
    header = record("TES4", 0, b"".join([
        sub("HEDR", struct.pack("<fiI", 1.0, count, 0x800 + 2 * len(ITEMS))), text("CNAM", "PAX test"),
        text("MAST", "Fallout4.esm"), sub("DATA", bytes(8))]), flags=0x200)
    return header + group("ARMO", armor) + group("ARMA", addons)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Downloads/PAX-Test1.zip"
    if out.exists():
        sys.exit("%s exists; remove it or name another file" % out)
    with zipfile.ZipFile(out, "x", zipfile.ZIP_DEFLATED) as z:
        z.writestr("PAXTest1.esp", build())
    print(out)

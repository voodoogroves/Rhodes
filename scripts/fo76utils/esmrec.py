#!/usr/bin/env python3
"""Print the raw subrecords of records from a Bethesda plugin (.esm/.esp/.esl).

esmdump (fo76utils) prints only the fields it knows (it omits BOOK's DATA/DNAM, for
example). This reads the file directly and shows every subrecord, so unknown fields can be
decoded by hand. Standard library only. Tested 2026-11-24 on Fallout4.esm (BOOK, STAT).

Usage: esmrec.py PLUGIN TYPE KEY [KEY...]
  TYPE  four-letter record type (BOOK, STAT, WEAP, OMOD, ...)
  KEY   a hex form ID (0008E74A or 0x8E74A) or an exact EditorID (PerkMagGrognakTheBarbarian10)
Form IDs print with the plugin's own load-order byte (00 for Fallout4.esm).
"""
import struct
import sys
import zlib

STRING_FIELDS = {"EDID", "MODL", "ICON", "MICO", "CNAM", "FULL", "DESC"}


def subrecords(buf):
    i, big, out = 0, None, []
    while i + 6 <= len(buf):
        tag = buf[i:i + 4].decode("latin1")
        size = struct.unpack("<H", buf[i + 4:i + 6])[0]
        i += 6
        if tag == "XXXX":  # next subrecord's size is held here
            big = struct.unpack("<I", buf[i:i + 4])[0]
            i += 4
            continue
        if big is not None:
            size, big = big, None
        out.append((tag, buf[i:i + size]))
        i += size
    return out


def records(data, rtype):
    """Yield (formid, subrecords) for every record of rtype, descending into all groups."""
    want = rtype.encode()
    stack = [(0, len(data))]
    while stack:
        p, end = stack.pop()
        while p < end:
            tag = data[p:p + 4]
            size = struct.unpack("<I", data[p + 4:p + 8])[0]
            if tag == b"GRUP":
                stack.append((p + 24, p + size))  # group header is 24 bytes, size includes it
                p += size
                continue
            flags, formid = struct.unpack("<II", data[p + 8:p + 16])
            if tag == want:
                body = data[p + 24:p + 24 + size]
                if flags & 0x00040000:  # compressed: u32 raw size, then zlib stream
                    body = zlib.decompress(body[4:])
                yield formid, subrecords(body)
            p += 24 + size


def show(tag, body):
    # Localized plugins store FULL/DESC/CNAM as a 4-byte string ID, so only print real text.
    text = body[:-1]
    if tag in STRING_FIELDS and body.endswith(b"\x00") and text and all(32 <= c < 127 for c in text):
        return repr(text.decode())
    return body.hex()


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    path, rtype, keys = sys.argv[1], sys.argv[2], sys.argv[3:]
    ids, names = set(), set()
    for k in keys:
        try:
            ids.add(int(k, 16))
        except ValueError:
            names.add(k)
    data = open(path, "rb").read()
    for formid, subs in records(data, rtype):
        edid = next((b[:-1].decode() for t, b in subs if t == "EDID"), "")
        if formid in ids or edid in names:
            print(f"{rtype} {formid:08X} {edid}")
            for tag, body in subs:
                print(f"  {tag} {len(body):>4}  {show(tag, body)[:200]}")


if __name__ == "__main__":
    main()

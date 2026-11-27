#!/usr/bin/env python3
"""Hide loose parts of a model, for example one of the two pieces in a dropped-item model.

  python3 -I trimparts.py model.nif out.nif --keep 1

Part numbers are the ones `nifpreview.py info` prints. Triangles of the other parts are
collapsed to nothing and each shape's bounding sphere is fitted to what is left; the file's
size and layout do not change. Collision is left as it was. Prints the bounds of the kept
parts, for the item record. The output is game-derived: keep it out of every repo.
"""
import argparse
import math
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nifpreview  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("model")
    ap.add_argument("out")
    ap.add_argument("--keep", required=True, help="part numbers to keep, e.g. 1,3")
    a = ap.parse_args()
    nif = nifpreview.Nif(a.model)
    parts = nifpreview.all_parts(nif)
    keep = {int(x) for x in a.keep.split(",")}
    if not keep or not keep <= set(range(1, len(parts) + 1)):
        raise SystemExit("--keep takes numbers from 1 to %d" % len(parts))
    kept = [(shape, tris) for n, (shape, tris) in enumerate(parts, 1) if n in keep]
    data = bytearray(nif.d)
    shapes = [i for i, b in enumerate(nif.blocks) if b[0] in nifpreview.SHAPES]
    everything = []
    for block, shape in zip(shapes, nif.shapes()):
        wanted = {t for s, tris in kept if s["verts"] == shape["verts"] for t in tris}
        _, _, at = nif.av_object(block)
        desc = struct.unpack_from("<Q", data, at + 28)[0]
        ntris, nverts = struct.unpack_from("<IH", data, at + 36)
        first = at + 46 + nverts * (desc & 0xF) * 4
        for t, tri in enumerate(shape["tris"]):
            if tri not in wanted:
                struct.pack_into("<3H", data, first + t * 6, 0, 0, 0)
        if not wanted:
            continue
        # Positions as stored (the sphere is in the shape's own coordinates).
        flags = desc >> 44
        raw = [struct.unpack_from("<3f" if flags & 0x400 else "<3e", nif.d,
                                  at + 46 + i * (desc & 0xF) * 4)
               for i in sorted({i for t in wanted for i in t})]
        centre = [(min(p[k] for p in raw) + max(p[k] for p in raw)) / 2 for k in range(3)]
        struct.pack_into("<4f", data, at, *centre, max(math.dist(p, centre) for p in raw))
        everything += [shape["verts"][i] for t in wanted for i in t]
    with open(a.out, "xb") as f:
        f.write(data)
    low = [math.floor(min(p[k] for p in everything)) for k in range(3)]
    high = [math.ceil(max(p[k] for p in everything)) for k in range(3)]
    print("wrote %s: kept %d of %d parts; bounds %s to %s" % (a.out, len(kept), len(parts), low, high))


if __name__ == "__main__":
    main()

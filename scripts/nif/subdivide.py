#!/usr/bin/env python3
"""Split every triangle of a skinned model into four. Standard library only.

  python3 subdivide.py IN.nif OUT.nif [--flat]

New points sit at edge midpoints, rounded along the surface's curve (--flat keeps them on
the old faces). Open edges and sharp creases stay straight. Texture coordinates, normals
and tangents are interpolated; each new point takes the four strongest of its parents'
bone weights. Body segment ranges are scaled to match, so triangle order is kept.
The result is derived from the source model: keep it out of every repo.
"""
import argparse
import struct

from fitbody import cross, dot, norm, sub, vertex_normals
from nifpreview import SHAPES, Nif

LAYOUT = 0x0005B00050430208
STRIDE = 32
SHARP = 0.5                                         # normals further apart than this make a crease


def key(p):
    return tuple(round(c, 2) for c in p)


def unit(b):
    return tuple(x / 127.5 - 1 for x in b)


def packed(v):
    return bytes(max(0, min(255, round((c + 1) * 127.5))) for c in v)


def midpoint(a, b, place):
    """One 32 byte vertex between a and b, at position place."""
    f = lambda raw: (struct.unpack_from("<e", raw, 6)[0], raw[15] / 127.5 - 1, raw[19] / 127.5 - 1)
    mean = lambda u, v: tuple((x + y) / 2 for x, y in zip(u, v))
    n = norm(mean(unit(a[12:15]), unit(b[12:15])))
    t = mean(unit(a[16:19]), unit(b[16:19]))
    t = norm(sub(t, tuple(dot(t, n) * c for c in n)))
    bit = mean(f(a), f(b))
    bit = norm(sub(bit, tuple(dot(bit, n) * c for c in n)))
    uv = mean(struct.unpack_from("<2e", a, 8), struct.unpack_from("<2e", b, 8))
    weights = {}
    for raw in (a, b):
        for w, bone in zip(struct.unpack_from("<4e", raw, 20), raw[28:32]):
            if w > 0:
                weights[bone] = weights.get(bone, 0) + w / 2
    top = sorted(weights.items(), key=lambda x: -x[1])[:4]
    total = sum(w for _, w in top) or 1
    top += [(0, 0)] * (4 - len(top))
    return (struct.pack("<4e2e", *place, bit[0], *uv)
            + packed(n) + packed(bit[1:2]) + packed(t) + packed(bit[2:3])
            + struct.pack("<4e4B", *(w / total for _, w in top), *(bone for bone, _ in top)))


def split(raw, tris, flat):
    verts = [struct.unpack_from("<3e", r, 0) for r in raw]
    normals = vertex_normals(verts, tris, key)
    edges = {}
    for t in tris:
        for i, j in ((0, 1), (1, 2), (2, 0)):
            e = frozenset((key(verts[t[i]]), key(verts[t[j]])))
            edges[e] = edges.get(e, 0) + 1
    out, made = list(raw), {}

    def middle(i, j):
        pair = (min(i, j), max(i, j))
        if pair not in made:
            a, b = verts[pair[0]], verts[pair[1]]
            place = tuple((x + y) / 2 for x, y in zip(a, b))
            na, nb = normals.get(key(a)), normals.get(key(b))
            if (not flat and na and nb and dot(na, nb) > SHARP
                    and edges[frozenset((key(a), key(b)))] > 1):
                # curved point-normal triangle, evaluated halfway along the edge
                wa, wb = dot(sub(b, a), na), dot(sub(a, b), nb)
                place = tuple(place[k] - (wa * na[k] + wb * nb[k]) / 8 for k in range(3))
            made[pair] = len(out)
            out.append(midpoint(raw[pair[0]], raw[pair[1]], place))
        return made[pair]

    faces = []
    for a, b, c in tris:
        ab, bc, ca = middle(a, b), middle(b, c), middle(c, a)
        faces += [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]
    return out, faces


def scaled_segments(tail, ntris):
    tail = bytearray(tail)
    prims, count, total = struct.unpack_from("<3I", tail, 0)
    if prims != ntris:
        raise SystemExit("segment table does not match the triangle count")
    struct.pack_into("<I", tail, 0, prims * 4)

    def scale(at):
        start, n = struct.unpack_from("<II", tail, at)
        struct.pack_into("<II", tail, at, start * 4, n * 4)

    p = 12
    for _ in range(count):
        scale(p)
        subs = struct.unpack_from("<I", tail, p + 12)[0]
        p += 16
        for _ in range(subs):
            scale(p)
            p += 16
    return bytes(tail)


def subdivide(source, target, flat=False):
    nif = Nif(source)
    d = nif.d
    blocks = [d[o:o + size] for _, o, size in nif.blocks]
    for i, (kind, offset, size) in enumerate(nif.blocks):
        if kind not in SHAPES:
            continue
        name = nif.av_object(i)[0]
        nif._u("4f")
        nif._u("i"), nif._u("i"), nif._u("i")
        desc_at = nif.p
        desc, ntris, nverts, data = nif._u("Q"), nif._u("I"), nif._u("H"), nif._u("I")
        if kind != "BSSubIndexTriShape" or desc != LAYOUT or data != nverts * STRIDE + ntris * 6:
            raise SystemExit("unexpected layout in shape " + name)
        start = nif.p
        raw = [d[start + v * STRIDE:start + (v + 1) * STRIDE] for v in range(nverts)]
        at = start + nverts * STRIDE
        tris = [struct.unpack_from("<3H", d, at + t * 6) for t in range(ntris)]
        out, faces = split(raw, tris, flat)
        if len(out) > 65535:
            raise SystemExit("too many vertices for one shape: " + name)
        body = b"".join(out) + b"".join(struct.pack("<3H", *f) for f in faces)
        blocks[i] = (d[offset:desc_at + 8] + struct.pack("<IHI", len(faces), len(out), len(body)) + body
                     + scaled_segments(d[at + ntris * 6:offset + size], ntris))
        print("  %-24s vertices %5d -> %5d, triangles %5d -> %5d" % (name, nverts, len(out), ntris, len(faces)))
    old = struct.pack("<%dI" % len(nif.blocks), *(size for _, _, size in nif.blocks))
    first = nif.blocks[0][1]
    at = d.find(old)
    if at < 0 or at > first:
        raise SystemExit("block size table not found")
    head = d[:at] + struct.pack("<%dI" % len(blocks), *map(len, blocks)) + d[at + len(old):first]
    footer = d[nif.blocks[-1][1] + nif.blocks[-1][2]:]
    with open(target, "wb") as f:
        f.write(head + b"".join(blocks) + footer)
    print("wrote", target)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("source")
    ap.add_argument("target")
    ap.add_argument("--flat", action="store_true")
    a = ap.parse_args()
    if a.source == a.target:
        raise SystemExit("give a different output file")
    subdivide(a.source, a.target, a.flat)


if __name__ == "__main__":
    main()

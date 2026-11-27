#!/usr/bin/env python3
"""Measure how a worn model sits on a body, push out what sinks in, or pull it closer. Standard library only.

  python3 fitbody.py measure BODY.nif OUTFIT.nif [...] [--ref SKELETON_BODY.nif]
  python3 fitbody.py push    BODY.nif IN.nif OUT.nif [--ref ...] [--clearance 0.0] [--spread 3.0] [--core 1.0] [--smooth 0] [--above Z]
  python3 fitbody.py hug     BODY.nif IN.nif OUT.nif [--ref ...] [--offset 0.2] [--keep 0.35] [--reach 4] [--smooth 2] [--above Z] [--carry N]

hug pulls cloth further than --offset from the body inward, keeping the share --keep of
the extra distance, so layers stay in order. Cloth near --reach units out is left (packs,
collars), fading over 1.5 units. It also turns the stored normals with the new surface. --carry makes loose parts under N
triangles (cables, pockets, badges) ride with the nearest cloth of a larger part, so
they keep their depth instead of being flattened.
BODY is the body to fit; its first shape is used. --ref is a body stored in the same
coordinates as the outfits (the vanilla femalebody.nif): needed when BODY is stored
elsewhere, as some replacers are; the offset is read from the bones they share.
Distances are signed, in game units: negative is inside the body. Bind pose only, so
clipping that appears in animation is not seen. Vertices nearest an open edge of the
body (neck, wrists) or further than 6 units from it are not judged.
--above leaves everything below that height (outfit coordinates) alone, fading in over
4 units: use it where boots already fit, or the leg tucked inside them pushes through.
--smooth evens the moves out along the mesh, to remove bumps. push and hug leave weights, segments and materials as they were; push leaves normals too.
Models are game-derived or other people's work: keep them out of every repo.
"""
import argparse
import math
import struct
import sys

from nifpreview import SHAPES, Nif, loose_parts

REACH = 6.0
CELL = 2.0


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a):
    n = math.sqrt(dot(a, a))
    return (a[0] / n, a[1] / n, a[2] / n) if n else (0.0, 0.0, 0.0)


def bone_transforms(nif, shape):
    """name -> (rotation rows, translation) taking model coordinates to bone coordinates."""
    for i, (kind, offset, _) in enumerate(nif.blocks):
        if kind == "BSSkin::BoneData":
            count = struct.unpack_from("<I", nif.d, offset)[0]
            if count == len(shape["bones"]):
                out = {}
                for b, name in enumerate(shape["bones"]):
                    f = struct.unpack_from("<13f", nif.d, offset + 4 + 68 * b + 16)
                    out[name] = (f[:9], f[9:12])
                return out
    raise SystemExit("no bone data for " + shape["name"])


def frame_offset(body_nif, body, ref_path):
    """What to add to BODY's vertices to put them in the reference's coordinates."""
    ref_nif = Nif(ref_path)
    ref = next(ref_nif.shapes())
    mine, theirs = bone_transforms(body_nif, body), bone_transforms(ref_nif, ref)
    offsets = []
    for name in set(mine) & set(theirs):
        r, t = mine[name]
        rr, tr = theirs[name]
        if max(abs(a - b) for a, b in zip(r, rr)) < 1e-3:
            d = sub(t, tr)
            offsets.append(tuple(dot((r[k], r[3 + k], r[6 + k]), d) for k in range(3)))
    if not offsets:
        raise SystemExit("no shared bones with matching rotation")
    mid = tuple(sorted(o[k] for o in offsets)[len(offsets) // 2] for k in range(3))
    close = sum(math.dist(o, mid) < 0.2 for o in offsets)
    print("body offset %s, agreed by %d of %d shared bones"
          % (tuple(round(c, 2) for c in mid), close, len(offsets)))
    if close < 0.8 * len(offsets):
        raise SystemExit("bones disagree on the offset")
    return mid


class Body:
    def __init__(self, path, ref=None):
        nif = Nif(path)
        shape = next(nif.shapes())
        off = frame_offset(nif, shape, ref) if ref else (0, 0, 0)
        ids, self.points, remap = {}, [], []
        for v in shape["verts"]:                    # weld texture seams
            p = (v[0] + off[0], v[1] + off[1], v[2] + off[2])
            key = tuple(round(c, 2) for c in p)
            if key not in ids:
                ids[key] = len(self.points)
                self.points.append(p)
            remap.append(ids[key])
        self.tris = [t for t in (tuple(remap[i] for i in t) for t in shape["tris"]) if len(set(t)) == 3]
        sums = [[0.0, 0.0, 0.0] for _ in self.points]
        edges = {}
        for t in self.tris:
            a, b, c = (self.points[i] for i in t)
            n = cross(sub(b, a), sub(c, a))
            for i in t:
                for k in range(3):
                    sums[i][k] += n[k]
            for e in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                key = tuple(sorted(e))
                edges[key] = edges.get(key, 0) + 1
        self.normals = [norm(s) for s in sums]
        self.open = {i for e, n in edges.items() if n == 1 for i in e}
        self.grid = {}
        for n, t in enumerate(self.tris):
            pts = [self.points[i] for i in t]
            lo = [int(min(p[k] for p in pts) // CELL) for k in range(3)]
            hi = [int(max(p[k] for p in pts) // CELL) for k in range(3)]
            for x in range(lo[0], hi[0] + 1):
                for y in range(lo[1], hi[1] + 1):
                    for z in range(lo[2], hi[2] + 1):
                        self.grid.setdefault((x, y, z), []).append(n)

    def closest(self, p, t):
        """Closest point of triangle t to p, as barycentric weights (Ericson)."""
        a, b, c = (self.points[i] for i in t)
        ab, ac, ap = sub(b, a), sub(c, a), sub(p, a)
        d1, d2 = dot(ab, ap), dot(ac, ap)
        if d1 <= 0 and d2 <= 0:
            return (1, 0, 0)
        bp = sub(p, b)
        d3, d4 = dot(ab, bp), dot(ac, bp)
        if d3 >= 0 and d4 <= d3:
            return (0, 1, 0)
        vc = d1 * d4 - d3 * d2
        if vc <= 0 and d1 >= 0 and d3 <= 0:
            v = d1 / (d1 - d3)
            return (1 - v, v, 0)
        cp = sub(p, c)
        d5, d6 = dot(ab, cp), dot(ac, cp)
        if d6 >= 0 and d5 <= d6:
            return (0, 0, 1)
        vb = d5 * d2 - d1 * d6
        if vb <= 0 and d2 >= 0 and d6 <= 0:
            w = d2 / (d2 - d6)
            return (1 - w, 0, w)
        va = d3 * d6 - d5 * d4
        if va <= 0 and d4 - d3 >= 0 and d5 - d6 >= 0:
            w = (d4 - d3) / ((d4 - d3) + (d5 - d6))
            return (0, 1 - w, w)
        s = va + vb + vc
        return (va / s, vb / s, vc / s)

    def signed(self, p):
        """(signed distance, outward direction), or None where the body cannot judge."""
        home = [int(c // CELL) for c in p]
        r = int(REACH // CELL) + 1
        cells = sorted(((x, y, z) for x in range(-r, r + 1) for y in range(-r, r + 1)
                        for z in range(-r, r + 1)), key=lambda o: max(map(abs, o)))
        best, seen, ring = None, set(), 0
        for o in cells:
            if max(map(abs, o)) != ring:
                ring = max(map(abs, o))
                if best and best[0] <= (ring - 1) * CELL:
                    break
            for n in self.grid.get((home[0] + o[0], home[1] + o[1], home[2] + o[2]), ()):
                if n in seen:
                    continue
                seen.add(n)
                t = self.tris[n]
                w = self.closest(p, t)
                q = tuple(sum(w[j] * self.points[t[j]][k] for j in range(3)) for k in range(3))
                d = math.dist(p, q)
                if best is None or d < best[0]:
                    best = (d, t, w, q)
        if best is None or best[0] > REACH:
            return None
        d, t, w, q = best
        if all(t[j] in self.open for j in range(3) if w[j] > 1e-6):
            return None
        normal = norm(tuple(sum(w[j] * self.normals[t[j]][k] for j in range(3)) for k in range(3)))
        return (d if dot(sub(p, q), normal) >= 0 else -d), normal


def summary(values, limit):
    if not values:
        return "none judged"
    v = sorted(values)
    at = lambda f: v[int(f * (len(v) - 1))]
    deep = sum(x < -limit for x in v)
    return ("%5d judged  5%% %6.2f  median %6.2f  95%% %6.2f  deepest %6.2f  inside by >%.2f: %4.1f%%"
            % (len(v), at(.05), at(.5), at(.95), v[0], limit, 100 * deep / len(v)))


def measure(body, path):
    print("==", path.split("/")[-1])
    for s in Nif(path).shapes():
        judged = [r[0] for r in map(body.signed, s["verts"]) if r]
        print("  %-18s %s" % (s["name"][:18], summary(judged, 0.1)))


def push(body, source, target, clearance, spread, core, smooth=0, above=None):
    nif = Nif(source)
    shapes = list(nif.shapes())
    need = []                                       # (position, outward move)
    for s in shapes:
        for p in s["verts"]:
            r = body.signed(p)
            if r and r[0] < clearance:
                need.append((p, tuple((clearance - r[0]) * c for c in r[1])))
    near = {}
    for p, move in need:
        near.setdefault(tuple(int(c // spread) for c in p), []).append((p, move))

    def displacement(p):
        """The largest nearby move: whole within core, fading out by spread, so layers and
        seams travel together."""
        home = [int(c // spread) for c in p]
        best, size = (0.0, 0.0, 0.0), 0.0
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                for z in (-1, 0, 1):
                    for q, move in near.get((home[0] + x, home[1] + y, home[2] + z), ()):
                        f = min(1.0, (spread - math.dist(p, q)) / (spread - core))
                        if f > 0:
                            f = f * f * (3 - 2 * f)
                            m = f * math.sqrt(dot(move, move))
                            if m > size:
                                best, size = tuple(f * c for c in move), m
        return best

    apply(nif, source, target, displacement, smooth, above)


def vertex_normals(verts, tris, key):
    sums = {}
    for t in tris:
        a, b, c = (verts[i] for i in t)
        n = cross(sub(b, a), sub(c, a))
        for i in t:
            old = sums.get(key(verts[i]), (0, 0, 0))
            sums[key(verts[i])] = tuple(old[k] + n[k] for k in range(3))
    return {k: norm(v) for k, v in sums.items()}


def turn_normals(data, s, desc, start, stride, moves, key):
    """Add the change in surface direction to each stored normal; square the tangents to it."""
    if desc != 0x0005B00050430208:
        raise SystemExit("unexpected vertex layout %x: normals not handled" % desc)
    verts, tris = s["verts"], s["tris"]
    after = [tuple(p[k] + moves[key(p)][k] for k in range(3)) for p in verts]
    ids = [key(p) for p in verts]
    old = vertex_normals(verts, tris, key)
    names = dict(zip(map(key, after), ids))
    new = {names[k]: v for k, v in vertex_normals(after, tris, key).items()}
    unit = lambda at: tuple(data[at + k] / 127.5 - 1 for k in range(3))
    pack = lambda v: [max(0, min(255, round((c + 1) * 127.5))) for c in v]
    agree = sum(dot(old[i], unit(start + v * stride + 12)) for v, i in enumerate(ids) if i in old)
    sign = 1 if agree >= 0 else -1
    for v, i in enumerate(ids):
        if i not in old or i not in new:
            continue
        o = start + v * stride
        n = unit(o + 12)
        n = norm(tuple(n[k] + sign * (new[i][k] - old[i][k]) for k in range(3)))
        data[o + 12:o + 15] = bytes(pack(n))
        bit = (struct.unpack_from("<e", data, o + 6)[0], data[o + 15] / 127.5 - 1, data[o + 19] / 127.5 - 1)
        square = lambda t: norm(tuple(t[k] - dot(t, n) * n[k] for k in range(3)))
        data[o + 16:o + 19] = bytes(pack(square(unit(o + 16))))
        bit = square(bit)
        struct.pack_into("<e", data, o + 6, bit[0])
        data[o + 15], data[o + 19] = pack(bit[1:])


def apply(nif, source, target, wanted, smooth=0, above=None, turn=False, carry=0):
    """Write target: source with wanted(position) added to each vertex, evened along the mesh."""
    data = bytearray(nif.d)
    shapes = list(nif.shapes())
    key = lambda p: tuple(round(c, 2) for c in p)      # seams and layers sharing a point agree
    moves, links = {}, {}
    for s in shapes:
        for p in s["verts"]:
            fade = 1.0 if above is None else max(0.0, min(1.0, (p[2] - above) / 4))
            moves[key(p)] = tuple(fade * c for c in wanted(p))
        for t in s["tris"]:
            ks = [key(s["verts"][i]) for i in t]
            for a in ks:
                links.setdefault(a, set()).update(k for k in ks if k != a)
    for _ in range(smooth):
        moves = {a: tuple((m[k] + sum(moves[b][k] for b in links[a]) / len(links[a])) / 2
                          for k in range(3)) if links.get(a) else m for a, m in moves.items()}

    if carry:
        small, large = set(), set()
        for s in shapes:
            for part in loose_parts(s):
                (small if len(part) < carry else large).update(key(s["verts"][i]) for t in part for i in t)
        small -= large
        if not large:
            raise SystemExit("--carry leaves no larger part to ride on")
        anchors = list(large)
        for k in small:
            moves[k] = moves[min(anchors, key=lambda a: math.dist(a, k))]
        print("  carried %d points on small parts" % len(small))

    shape_blocks = [i for i, b in enumerate(nif.blocks) if b[0] in SHAPES]
    stored = iter(shapes)
    for i in shape_blocks:
        _, local, _ = nif.av_object(i)
        sphere_at = nif.p
        nif._u("4f")
        nif._u("i"), nif._u("i"), nif._u("i")
        desc, _, count = nif._u("Q"), nif._u("I"), nif._u("H")
        if not nif._u("I"):
            continue
        start, stride = nif.p, (desc & 0xF) * 4
        s = next(stored)
        if any(abs(c) > 1e-6 for c in local[0]) or any(
                abs(a - b) > 1e-6 for a, b in zip(local[1], (1, 0, 0, 0, 1, 0, 0, 0, 1))):
            raise SystemExit("shape %s has its own transform; not handled" % s["name"])
        fmt = "<3f" if (desc >> 44) & 0x400 else "<3e"
        moved, largest = 0, 0.0
        for v, p in enumerate(s["verts"]):
            m = moves[key(p)]
            size = math.sqrt(dot(m, m))
            if size > 0.01:
                struct.pack_into(fmt, data, start + v * stride, *(p[k] + m[k] for k in range(3)))
                moved, largest = moved + 1, max(largest, size)
        if turn:
            turn_normals(data, s, desc, start, stride, moves, key)
        radius = struct.unpack_from("<f", data, sphere_at + 12)[0]
        struct.pack_into("<f", data, sphere_at + 12, radius + largest)
        print("  %-18s moved %5d of %5d vertices, largest %.2f" % (s["name"][:18], moved, count, largest))
    with open(target, "wb") as f:
        f.write(data)
    print("wrote", target)


def hug(body, source, target, offset, keep, reach, smooth, above, carry=0):
    def inward(p):
        r = body.signed(p)
        if not r or r[0] <= offset:
            return (0.0, 0.0, 0.0)
        weight = max(0.0, min(1.0, (reach - r[0]) / 1.5))
        return tuple(-weight * (1 - keep) * (r[0] - offset) * c for c in r[1])

    apply(Nif(source), source, target, inward, smooth, above, turn=True, carry=carry)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("command", choices=("measure", "push", "hug"))
    ap.add_argument("body")
    ap.add_argument("models", nargs="+")
    ap.add_argument("--ref")
    ap.add_argument("--clearance", type=float, default=0.0)
    ap.add_argument("--spread", type=float, default=3.0)
    ap.add_argument("--core", type=float, default=1.0)
    ap.add_argument("--smooth", type=int)
    ap.add_argument("--offset", type=float, default=0.2)
    ap.add_argument("--keep", type=float, default=0.35)
    ap.add_argument("--reach", type=float, default=4.0)
    ap.add_argument("--above", type=float)
    ap.add_argument("--carry", type=int, default=0)
    a = ap.parse_args()
    if not 0 <= a.core < a.spread:
        raise SystemExit("--core must be at least 0 and under --spread")
    body = Body(a.body, a.ref)
    if a.command == "measure":
        for path in a.models:
            measure(body, path)
    else:
        if len(a.models) != 2 or a.models[0] == a.models[1]:
            raise SystemExit(a.command + " needs IN.nif and a different OUT.nif")
        if a.command == "push":
            push(body, a.models[0], a.models[1], a.clearance, a.spread, a.core, a.smooth or 0, a.above)
        else:
            if not 0 <= a.keep <= 1 or a.reach > REACH:
                raise SystemExit("--keep is 0 to 1; --reach at most %g" % REACH)
            smooth = 2 if a.smooth is None else a.smooth
            hug(body, a.models[0], a.models[1], a.offset, a.keep, a.reach, smooth, a.above, a.carry)


if __name__ == "__main__":
    sys.exit(main())

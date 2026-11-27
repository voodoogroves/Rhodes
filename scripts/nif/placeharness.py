#!/usr/bin/env python3
"""Mock up the Raider scrap harness: junk bolted to the torso and legs. Standard library only.

  python3 -I placeharness.py MESHES OUTDIR

MESHES holds these, extracted with baunpack from "Fallout4 - Meshes.ba2" (paths start meshes/ or
at the folders below):
  actors/powerarmor/characterassets/{skeleton.nif, frame.nif, mods/pa_raider_*.nif}
  setdressing/signage/highwaysign01.nif, setdressing/dmndclutter/dmndstreetsign01.nif,
  vehicles/automotive/automotivehubcap01.nif, setdressing/playerhouse/playerhouse_potsfryingpan01.nif,
  setdressing/teddybear/toyteddybeardirty01.nif, setdressing/flamingo/lawnflamingo02static.nif

Writes harness_suit.png: a highway sign beaten to the chest, a street sign on the left thigh, a
frying pan on the right thigh, a hubcap chained to the right calf and a teddy bear caged in
fencing on the left calf, and a lawn flamingo chained across the upper back above the fusion core. Model coordinates: X to the wearer's right, Y forward, Z up. Previews
only: no game model is written. The pictures are
derived from game files: keep them out of every repo.
"""
import argparse
import math
import os
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))
rack = runpy.run_path(os.path.join(HERE, "placerack.py"))
place, nifpreview, Nif, render = rack["place"], rack["nifpreview"], rack["Nif"], rack["render"]
moved, box_tris, unit, cross = rack["moved"], rack["box_tris"], rack["unit"], rack["cross"]

# Preview colours (nifpreview part numbers).
SIGN, PAN, CAP, BEAR, STREET, BAND, BOLT, CHAIN, SUIT = 1, 4, 3, 9, 7, 2, 5, 6, 10

# The back's flamingo: size, middle across the back, slant (degrees, head up), colour; the box
# over the fusion core that it and its chains keep out of (half width, top); chain runs as (x, z).
BIRD, BIRD_X, SLANT, BIRD_COLOUR = 0.72, 6.0, 28.0, 8
CORE_HALF, CORE_TOP = 11.0, 123.0
CHAINS = (((-15.0, 142.0), (15.0, 125.0)), ((-13.0, 125.0), (12.0, 146.0)))
# Each piece: colour, model, the model's own facing and up axes, then on the suit: a point inside
# the body or leg (the piece is slid out from it to the surface), facing, up, largest size, how far
# it sinks in, where the bolts go (fractions of half width and half height), strap heights
# (fractions), and what else holds it: None, "chain" or "fence".
PIECES = (
    (SIGN, "setdressing/signage/highwaysign01", (0, 1, 0), (0, 0, 1),
     (2.0, 0.0, 118.0), (0.08, 1.0, 0.04), (0.14, 0.0, 1.0), 25.0, -0.5,
     ((-0.82, 0.74), (0.84, 0.7), (-0.8, -0.72), (0.82, -0.76)), (), None),
    (STREET, "setdressing/dmndclutter/dmndstreetsign01", (0, 1, 0), (0, 0, 1),
     (-13.0, -2.0, 67.0), (-0.3, 0.95, 0.0), (-0.65, -0.2, 0.73), 27.0, -0.3,
     ((-0.85, 0.0), (0.85, 0.0)), (), None),
    (PAN, "setdressing/playerhouse/playerhouse_potsfryingpan01", (0, 0, -1), (0, 1, 0),
     (13.0, -2.0, 67.0), (0.99, 0.12, 0.0), (0.02, -0.2, 1.0), 23.0, 1.0,
     ((0.0, 0.62),), (0.3,), None),
    (CAP, "vehicles/automotive/automotivehubcap01", None, None,
     (15.0, -3.0, 30.0), (0.36, 0.93, 0.0), (0.0, 0.0, 1.0), 15.0, 1.4,
     ((0.0, 0.0),), (), "chain"),
    (BEAR, "setdressing/teddybear/toyteddybeardirty01", (0, -1, 0), (0, 0, 1),
     (-16.0, -4.0, 30.0), (-0.97, 0.22, 0.0), (-0.02, -0.08, 1.0), 20.0, 2.5,
     (), (), "fence"),
)


def dot(a, b):
    return sum(a[k] * b[k] for k in range(3))


def model(meshes, path):
    """A static model's triangles with every node transform applied."""
    nif = Nif(os.path.join(meshes, path + ".nif"))
    parents = nif.parents()
    shapes = []
    for s in nif.shapes():
        i = next(i for i, (kind, _, _) in enumerate(nif.blocks)
                 if kind.endswith("TriShape") and nif.av_object(i)[0] == s["name"])
        chain = []
        while True:
            _, (move, r, scale), _ = nif.av_object(i)
            chain.append((r, move, scale))
            if i not in parents:
                break
            i = parents[i]
        shapes.append(dict(s, verts=[place["to_model"](chain, v) for v in s["verts"]]))
    if "streetsign" in path:                   # the boards only, not the post
        kept = []
        for s in shapes:
            groups = nifpreview["loose_parts"](s)
            wide = lambda g: (max(s["verts"][i][0] for t in g for i in t)
                              - min(s["verts"][i][0] for t in g for i in t))
            widest = max(groups, key=wide)
            kept.append(dict(s, tris=widest))
        shapes = kept
    return shapes


def prism(centre, out, radius, height, sides=6):
    """A bolt head standing out from `centre` along `out`."""
    out = unit(out)
    a = unit(cross(out, (0.0, 0.0, 1.0) if abs(out[2]) < 0.9 else (1.0, 0.0, 0.0)))
    b = cross(out, a)
    verts = [tuple(centre[k] + out[k] * h + radius * (a[k] * math.cos(2 * math.pi * i / sides)
             + b[k] * math.sin(2 * math.pi * i / sides)) for k in range(3))
             for h in (0.0, height) for i in range(sides)]
    tris = []
    for i in range(sides):
        j = (i + 1) % sides
        tris += [(i, j, j + sides), (i, j + sides, i + sides)]
    for first in (0, sides):
        tris += [(first, first + i, first + i + 1) for i in range(1, sides - 1)]
    return {"verts": verts, "tris": tris, "weights": [], "bones": []}


def fit(piece, meshes, surface):
    colour, path, face, up_own, at, facing, up, size, sink, bolts, straps, _ = piece
    shapes = model(meshes, path)
    used = [s["verts"][i] for s in shapes for t in s["tris"] for i in t]
    low = [min(v[k] for v in used) for k in range(3)]
    high = [max(v[k] for v in used) for k in range(3)]
    middle = [(a + b) / 2 for a, b in zip(low, high)]
    if face is None:                           # a disc: it faces along its thinnest side
        thin = min(range(3), key=lambda k: high[k] - low[k])
        face = tuple(1.0 if k == thin else 0.0 for k in range(3))
        up_own = (0, 1, 0) if thin == 2 else (0, 0, 1)
    scale = size / max(high[k] - low[k] for k in range(3))
    across_own = cross(up_own, face)
    n = unit(facing)
    u = unit(tuple(up[k] - n[k] * dot(up, n) for k in range(3)))
    r = cross(u, n)

    def local(v):
        d = [v[k] - middle[k] for k in range(3)]
        return tuple(scale * dot(d, axis) for axis in (across_own, u_axis, face))
    u_axis = up_own
    points = [local(v) for v in used]
    half_w, half_h = max(abs(p[0]) for p in points), max(abs(p[1]) for p in points)
    back = min(p[2] for p in points)
    # Slide the piece out until its back rests on the suit under it.
    start = at
    under = []
    if abs(at[0]) > 8.0:                       # a leg piece: only that leg counts
        surface = [p for p in surface if p[0] * at[0] > 0]
    wide = 1.0 if colour == STREET else 0.6    # a long flat board must clear all of what it spans
    for p in surface:
        d = tuple(p[k] - start[k] for k in range(3))
        if abs(dot(d, r)) < half_w * wide and abs(dot(d, u)) < half_h * wide and dot(d, n) > 0:
            under.append(dot(d, n))
    reach = (sorted(under)[int((len(under) - 1) * (1.0 if colour in (SIGN, STREET) else 0.97))]
             if under else 0.0) - back - sink
    centre = tuple(start[k] + n[k] * reach for k in range(3))

    def world(p):
        return tuple(centre[k] + r[k] * p[0] + u[k] * p[1] + n[k] * p[2] for k in range(3))

    cells = {}
    if colour in (SIGN, STREET):               # how far the suit reaches under each small square
        for p in surface:
            d = tuple(p[k] - centre[k] for k in range(3))
            if dot(d, n) > -14.0:
                key = (int(dot(d, r) // 2.0), int(dot(d, u) // 2.0))
                cells[key] = max(cells.get(key, -99.0), dot(d, n))

    def height(x, y):                          # the chest's outline there, smoothed, never inside it
        i, j = x / 2.0 - 0.5, y / 2.0 - 0.5
        i0, j0 = math.floor(i), math.floor(j)

        def corner(a, b):
            near = [cells[(a + c, b + e)] for c in (-1, 0, 1) for e in (-1, 0, 1) if (a + c, b + e) in cells]
            return max(near) if near else -6.0
        s, t = i - i0, j - j0
        return ((corner(i0, j0) * (1 - s) + corner(i0 + 1, j0) * s) * (1 - t)
                + (corner(i0, j0 + 1) * (1 - s) + corner(i0 + 1, j0 + 1) * s) * t)

    def bend(p):
        if colour in (SIGN, STREET):           # sheet metal beaten to the shape under it
            return (p[0], p[1], p[2] - back + max(-6.0, height(p[0], p[1])) + 0.5)
        return p

    def pieces(shape):                         # a sheet needs many small triangles to bend
        verts, tris = [local(v) for v in shape["verts"]], list(shape["tris"])
        if colour in (SIGN, STREET):
            for _ in range(4):
                mids, split = {}, []

                def mid(a, b):
                    key = (min(a, b), max(a, b))
                    if key not in mids:
                        mids[key] = len(verts)
                        verts.append(tuple((verts[a][k] + verts[b][k]) / 2 for k in range(3)))
                    return mids[key]
                for a, b, c in tris:
                    ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
                    split += [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]
                tris = split
        return {"verts": [world(bend(v)) for v in verts], "tris": tris, "weights": [], "bones": []}
    out = [(colour, pieces(s)) for s in shapes]

    def front(x, y):                           # the piece's outer face near (x, y)
        near = [q[2] for q in points if abs(q[0] - x) < half_w * 0.3 and abs(q[1] - y) < half_h * 0.3]
        return max(near) if near else max(q[2] for q in points)
    for fx, fy in bolts:
        x, y = fx * half_w, fy * half_h
        spot = world(bend((x, y, front(x, y) - 0.2)))
        out.append((BOLT, prism(spot, n, 1.1, 1.0)))
    for fy in straps:
        y, half = fy * half_h, 1.1
        steps = []
        for i in range(9):
            x = (i / 4 - 1) * (half_w + 1.5)
            inside = abs(x) < half_w
            z = (front(x, y) + 0.5) if inside else back
            steps.append((x, z))
        for (x0, z0), (x1, z1) in zip(steps, steps[1:]):
            ring = lambda x, z: [(x, y - half, z - 0.5), (x, y + half, z - 0.5),
                                 (x, y + half, z + 0.4), (x, y - half, z + 0.4)]
            verts = [world(p) for p in ring(x0, z0) + ring(x1, z1)]
            tris = []
            for i in range(4):
                j = (i + 1) % 4
                tris += [(i, j, j + 4), (i, j + 4, i + 4)]
            out.append((BAND, {"verts": verts, "tris": tris, "weights": [], "bones": []}))
        for x, z in (steps[0], steps[-1]):
            out.append((BOLT, prism(world((x, y, z + 0.3)), n, 1.0, 0.9)))
    return out


def loop(points):
    """A closed taut line round (x, y) points, anticlockwise."""
    over = rack["ram"]["over"]
    top = over(points)
    under = [(x, -y) for x, y in over([(x, -y) for x, y in points])]
    return under + top[::-1][1:-1]


def along(path, step):
    """Evenly spaced (point, direction) pairs round a closed path of 3D points."""
    out, carry = [], 0.0
    for a, b in zip(path, path[1:] + path[:1]):
        length = math.dist(a, b)
        if length < 1e-6:
            continue
        d = tuple((b[k] - a[k]) / length for k in range(3))
        while carry < length:
            out.append((tuple(a[k] + d[k] * carry for k in range(3)), d))
            carry += step
        carry -= length
    return out


def link(centre, d, flat):
    """One oval chain link lying along d, flat or edge on."""
    side = unit(cross(d, (0.0, 0.0, 1.0)))
    other = cross(side, d)
    wide = side if flat else other
    points = [tuple(centre[k] + d[k] * 1.5 * math.cos(2 * math.pi * i / 10)
                    + wide[k] * 0.9 * math.sin(2 * math.pi * i / 10) for k in range(3)) for i in range(10)]
    return [segment(a, b, 0.3) for a, b in zip(points, points[1:] + points[:1])]


def segment(a, b, radius):
    """A square wire from a to b."""
    d = unit(tuple(b[k] - a[k] for k in range(3)))
    s = unit(cross(d, (0.0, 0.0, 1.0) if abs(d[2]) < 0.9 else (1.0, 0.0, 0.0)))
    t = cross(d, s)
    verts = [tuple(p[k] + radius * (s[k] * x + t[k] * y) for k in range(3))
             for p in (a, b) for x, y in ((1, 0), (0, 1), (-1, 0), (0, -1))]
    tris = []
    for i in range(4):
        j = (i + 1) % 4
        tris += [(i, j, j + 4), (i, j + 4, i + 4)]
    return {"verts": verts, "tris": tris, "weights": [], "bones": []}


def wrap(piece, parts, surface):
    """Chain or fencing round the leg and over the piece."""
    at, facing, kind = piece[4], unit(piece[5]), piece[11]
    solid = [p for p in surface if p[0] * at[0] > 0]
    for _, q in parts:
        for t in q["tris"]:
            a, b, c = (q["verts"][i] for i in t)
            solid += [tuple(a[k] + (b[k] - a[k]) * i / 4 + (c[k] - a[k]) * j / 4 for k in range(3))
                      for i in range(5) for j in range(5 - i)]

    def girth(z, grow):
        flat = [(p[0], p[1]) for p in solid if abs(p[2] - z) < 1.6]
        line = loop(flat)
        cx, cy = sum(x for x, _ in line) / len(line), sum(y for _, y in line) / len(line)
        return [(x + (x - cx) / math.hypot(x - cx, y - cy) * grow,
                 y + (y - cy) / math.hypot(x - cx, y - cy) * grow) for x, y in line]
    out = []
    if kind == "chain":
        front = math.atan2(facing[1], facing[0])
        for height, lean in ((at[2] + 1.0, 4.5), (at[2] - 1.0, -4.5)):    # two turns, crossed over the front
            line = girth(height, 0.7)
            cx, cy = sum(x for x, _ in line) / len(line), sum(y for _, y in line) / len(line)
            path = [(x, y, height + lean * math.sin(math.atan2(y - cy, x - cx) - front)) for x, y in line]
            for n, (point, d) in enumerate(along(path, 2.3)):
                out += [(CHAIN, q) for q in link(point, d, n % 2 == 0)]
    else:
        low, high = at[2] - 8.0, at[2] + 9.0
        rows = 9
        rings = []
        for i in range(rows):
            z = low + (high - low) * i / (rows - 1)
            rings.append(along([(x, y, z) for x, y in girth(z, 0.6)], 2.2))
        count = 40
        grid = [[ring[int(k * len(ring) / count) % len(ring)][0] for k in range(count)] for ring in rings]
        for i in range(rows - 1):              # slanting strands both ways: a wire cage
            for k in range(count):
                for step in (1, -1):
                    a, b = grid[i][k], grid[i + 1][(k + step) % count]
                    torn = high - 6.0 * abs(math.sin(k * 1.7) * math.cos(k * 0.45))   # ragged top edge
                    if (k + i) % 2 == 0 and math.dist(a, b) < 9.0 and max(a[2], b[2]) <= torn + 0.8:
                        out.append((CHAIN, segment(a, b, 0.22)))
        for ring in (grid[0],):                # a heavier wire binds the lower edge
            out += [(BAND, segment(a, b, 0.45)) for a, b in zip(ring, ring[1:] + ring[:1])
                    if math.dist(a, b) > 0.05]
    return out


def flamingo(meshes, surface):
    """A lawn flamingo slung across the upper back on a slant, head up past the wearer's right
    shoulder, lashed on with chain. Nothing comes down over the fusion core."""
    shape = model(meshes, "setdressing/flamingo/lawnflamingo02static")[0]
    groups = nifpreview["loose_parts"](shape)
    body = [t for g in groups if len(g) > 20 for t in g]          # the bird, without its stake
    used = [shape["verts"][i] for t in body for i in t]
    middle = [(min(v[k] for v in used) + max(v[k] for v in used)) / 2 for k in range(3)]
    top = [v for v in used if v[2] > max(q[2] for q in used) - 4.0]
    head = 1.0 if sum(v[1] for v in top) / len(top) > middle[1] else -1.0
    c, n = math.cos(math.radians(SLANT)), math.sin(math.radians(SLANT))

    def flat(v):                    # the bird's side view in the suit's X (toward the head) and Z
        ahead, high = head * (v[1] - middle[1]) * BIRD, (v[2] - middle[2]) * BIRD
        return (ahead * c - high * n, -head * (v[0] - middle[0]) * BIRD, ahead * n + high * c)
    laid = [flat(v) for v in used]
    # Raised until everything near the middle of the back is above the core.
    lift = max(CORE_TOP - z for x, _, z in laid if abs(x + BIRD_X) < CORE_HALF)
    under = [p[1] for p in surface if p[1] < -15.0
             and any(abs(p[0] - x - BIRD_X) < 2.0 and abs(p[2] - z - lift) < 2.0 for x, _, z in laid[::6])]
    # Rest the bird on the middle of what lies under it, not on whatever sticks out furthest.
    under.sort()
    depth = (under[len(under) // 2] if under else -31.0) - max(y for _, y, _ in laid) + 0.6

    def world(v):
        x, y, z = flat(v)
        return (x + BIRD_X, y + depth, z + lift)
    out = [(BIRD_COLOUR, moved(shape, body, world))]
    points = [world(v) for v in used]
    print("flamingo: x %.0f..%.0f z %.0f..%.0f; lowest near the core %.0f" % (
        min(p[0] for p in points), max(p[0] for p in points), min(p[2] for p in points),
        max(p[2] for p in points), min(p[2] for p in points if abs(p[0]) < CORE_HALF)))
    for start, end in CHAINS:       # each run lies over whatever is outermost along its way
        count = int(math.dist(start, end) / 2.3)
        run = []
        for i in range(count + 1):
            x, z = (start[k] + (end[k] - start[k]) * i / count for k in (0, 1))
            near = [p[1] for p in points + surface
                    if p[1] < -12.0 and abs(p[0] - x) < 2.0 and abs(p[2] - z) < 2.0]
            run.append((x, (min(near) if near else -28.0) - 0.4, z))
        # No single link stands out on its own: each follows its neighbours.
        ys = [sorted(q[1] for q in run[max(0, i - 2):i + 3]) for i in range(len(run))]
        run = [(x, v[len(v) // 2], z) for (x, _, z), v in zip(run, ys)]
        for i, (a, b) in enumerate(zip(run, run[1:])):
            d = unit(tuple(b[k] - a[k] for k in range(3)))
            mid = tuple((a[k] + b[k]) / 2 for k in range(3))
            out += [(CHAIN, q) for q in link(mid, d, i % 2 == 0)]
    return out


def build(meshes, bones):
    """The suit's shapes and the harness's parts."""
    pa = os.path.join(meshes, "actors/powerarmor/characterassets")
    suit, surface = [], []
    for name in ("frame.nif",) + tuple("mods/pa_raider_%s.nif" % n for n in
                                       ("body", "helmet", "larm", "rarm", "lleg", "rleg")):
        for q in place["posed"](os.path.join(pa, name), bones):
            suit.append((SUIT, (q, q["tris"])))
            if "arm" in name:
                continue
            for t in q["tris"]:
                if any(place["dominant"](q, i).startswith(("LArm", "RArm", "L_", "R_")) for i in t):
                    continue
                a, b, c = (q["verts"][i] for i in t)
                surface += [tuple(a[k] + (b[k] - a[k]) * i / 3 + (c[k] - a[k]) * j / 3 for k in range(3))
                            for i in range(4) for j in range(4 - i)]
    junk = []
    for piece in PIECES:
        parts = fit(piece, meshes, surface)
        junk += parts
        if piece[11]:
            junk += wrap(piece, [p for p in parts if p[0] == piece[0]], surface)
    junk += flamingo(meshes, surface)
    return suit, junk


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("meshes")
    ap.add_argument("outdir")
    args = ap.parse_args()
    meshes = args.meshes
    if os.path.isdir(os.path.join(meshes, "meshes")):
        meshes = os.path.join(meshes, "meshes")
    pa = os.path.join(meshes, "actors/powerarmor/characterassets")
    bones = place["skeleton"](os.path.join(pa, "skeleton.nif"))
    suit, junk = build(meshes, bones)
    os.makedirs(args.outdir, exist_ok=True)
    render(suit + [(c, (q, q["tris"])) for c, q in junk], 600, os.path.join(args.outdir, "harness_suit.png"))
    print("drawn")


if __name__ == "__main__":
    main()

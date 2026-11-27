#!/usr/bin/env python3
"""Mock up the Raider weapons: the brick-and-rebar ram (left) and the ritual claw (right).

  python3 -I placeram.py MESHES OUTDIR [--suit]

MESHES holds these, extracted with baunpack from "Fallout4 - Meshes.ba2" (paths start meshes/ or
at the folders below):
  actors/powerarmor/characterassets/{skeleton.nif, frame.nif, mods/pa_raider_*.nif}
  weapons/machete/sacrificalblade.nif
  weapons/powerfist/{rebarfist.nif, powerfist.nif}

The brick sits just past the arm armor, with the Puncturing Power Fist's rebar, cut short and
bent, reaching out in front; a second set of the bars runs straight back up the forearm, held by part of
a Power Fist cuff on a foot that fills down into the arm, and one buckled band over them, bolted
to the arm at both ends. Writes wrist_v2_arm.png (left arm) and claw_v2_arm.png (right arm, the claw dressed with wire
fencing, bolted bands and bolts), both close up, back of the hand up.
--suit also draws the whole Raider suit wearing it and the claw (slow). Previews only: no game model is written. The pictures are
derived from game files: keep them out of every repo.
"""
import argparse
import math
import os
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))
claws = runpy.run_path(os.path.join(HERE, "placeclaw.py"))
place, nifpreview = claws["place"], claws["nifpreview"]
Nif, render = claws["Nif"], claws["render"]
moved, box_tris, top_of = claws["moved"], claws["box_tris"], claws["top_of"]
wire, BLADE_PART = claws["wire"], claws["BLADE"]
BLADE_STAGGER = 2.2                   # how much further one claw blade reaches than the other

# Preview colours (nifpreview part numbers): red, blue, yellow, brown, green, grey.
BRICK, STRAP, CHAIN, BAR, CUFF, SUIT = 1, 2, 7, 9, 3, 10
BRICK_SCALE = 1.25
BRICK_AT = 31.2                       # the brick's middle: its back face just past the arm armor (27)
BRICK_BACK, BRICK_UP = -2.9, 3.4      # the vanilla brick's rear face and half height
BAR_END = 8.0                         # where the straightened bars stop, along the forearm
# The forward bars, one side, middle, other side: length past the brick, then how far the tip is
# pushed across, lifted, and how far the bar swings on the way.
SPIKES = ((6.5, -1.8, 0.9, 0.9), (9.0, 1.1, -1.0, -1.0), (4.8, 1.5, 1.6, -0.7))
CHAIN_OUT = 0.25                      # how far a chain link's middle stands off the brick's end faces
MIDDLE = 1.0                          # across the knuckles: the hand sits toward the thumb
CUFF_AT, STRAP_AT = 12.0, 21.0
STRAP_DROP = 7.0                      # how far below the bars the strap's bolted ends sit
LEAN = 0.22                           # how far the bars and brick drop per unit toward the fingers
ROLL = -13.0                          # degrees round the left arm to the knuckle line; the right is +13
# The Power Fist's big bolted ring: its span along its own X, axis, and inner radius.
CUFF_X, CUFF_AXIS = (20.3, 24.8), (-1.75, -1.85)
CUFF_SIZE, CUFF_MIDDLE = 1.25, 5.8    # its scale, and the radius, before scaling, that meets the bars
CUFF_FLAT = 0.65                      # the ring's height against its width
FOOT_TOP, FOOT_BASE = 1.8, 4.5        # half the foot's length along the arm, at the ring and at the arm


def arm(meshes, bones, side):
    """One Raider arm and the frame under it, in forearm bone coordinates, and points over it."""
    pa = os.path.join(meshes, "actors/powerarmor/characterassets")
    bone = side + "Arm_ForeArm1"
    own = tuple(side + "Arm_" + n for n in ("ForeArm", "Hand", "Finger"))
    local, points = [], []
    for model in ("frame.nif", "mods/pa_raider_%sarm.nif" % side.lower()):
        for s in place["posed"](os.path.join(pa, model), bones):
            tris = [t for t in s["tris"] if all(place["dominant"](s, i).startswith(own) for i in t)]
            if not tris:
                continue
            local.append(moved(s, tris, lambda p: place["to_bone"](bones[bone], p)))
            for t in local[-1]["tris"]:
                a, b, c = (local[-1]["verts"][i] for i in t)
                points += [tuple(a[n] + (b[n] - a[n]) * j / 4 + (c[n] - a[n]) * k / 4 for n in range(3))
                           for j in range(5) for k in range(5 - j)]
    return local, points


def over(points):
    """The upper convex hull of (y, z) points, left to right: the line a tight strap takes."""
    hull = []
    for p in sorted(set(points)):
        while len(hull) > 1 and ((hull[-1][0] - hull[-2][0]) * (p[1] - hull[-2][1])
                                 - (hull[-1][1] - hull[-2][1]) * (p[0] - hull[-2][0])) >= 0:
            hull.pop()
        hull.append(p)
    return hull


def hexbolt(x, at, out, radius, height):
    """A hex head centred at x along the arm and (y, z) = at, standing out along (y, z) = out."""
    ny, nz = out
    verts = []
    for h in (0.0, height):
        for k in range(6):
            across, along = radius * math.sin(k * math.pi / 3), radius * math.cos(k * math.pi / 3)
            verts.append((x + along, at[0] - nz * across + ny * h, at[1] + ny * across + nz * h))
    tris = []
    for k in range(6):
        m = (k + 1) % 6
        tris += [(k, m, m + 6), (k, m + 6, k + 6)]
    for first in (0, 6):
        tris += [(first, first + k, first + k + 1) for k in range(1, 5)]
    return {"verts": verts, "tris": tris, "weights": [], "bones": []}


def belt(surface, top_points, x, bar_z, drop, buckle=True):
    """A bent band over the bars, reaching the same depth on both sides of the arm and bolted
    there, with a buckle on top."""
    slab = [(y, z) for a, y, z in surface if abs(a - x) < 1.5]
    foot = bar_z - drop
    level = [y for y, z in slab if abs(z - foot) < 1.5]
    feet = [(min(level) - 0.3, foot), (max(level) + 0.3, foot)]
    line = over(feet + [q for q in slab + top_points
                        if q[1] >= foot and feet[0][0] <= q[0] <= feet[1][0]])
    solids = []
    for (y0, z0), (y1, z1) in zip(line, line[1:]):
        length = math.hypot(y1 - y0, z1 - z0)
        ny, nz = -(z1 - z0) / length, (y1 - y0) / length          # outward from the arm
        ring = [(y0 - ny * 0.4, z0 - nz * 0.4), (y1 - ny * 0.4, z1 - nz * 0.4),
                (y1 + ny * 0.5, z1 + nz * 0.5), (y0 + ny * 0.5, z0 + nz * 0.5)]
        solids.append(box_tris([(a, ring) for a in (x - 1.1, x + 1.1)]))
    # At each end, a squared-off plate and a hex bolt through it, facing out from the arm.
    for end, back in ((line[0], line[1]), (line[-1], line[-2])):
        length = math.hypot(back[0] - end[0], back[1] - end[1])
        ay, az = (back[0] - end[0]) / length, (back[1] - end[1]) / length     # up the band
        ny, nz = (-az, ay) if end is line[0] else (az, -ay)                    # outward
        at = lambda a, h: (end[0] + ay * a + ny * h, end[1] + az * a + nz * h)
        plate = [at(-0.8, -0.4), at(2.4, -0.4), at(2.4, 0.7), at(-0.8, 0.7)]
        solids.append(box_tris([(x + a, plate) for a in (-1.6, 1.6)]))
        solids.append(hexbolt(x, at(0.8, 0.5), (ny, nz), 1.1, 1.1))
    if not buckle:
        return solids
    # The buckle sits on the longest straight run near the top.
    (y0, z0), (y1, z1) = max([r for r in zip(line, line[1:]) if min(r[0][1], r[1][1]) > bar_z - 2.0] or list(zip(line, line[1:])), key=lambda r: math.hypot(r[1][0] - r[0][0], r[1][1] - r[0][1]))
    length = math.hypot(y1 - y0, z1 - z0)
    ay, az = (y1 - y0) / length, (z1 - z0) / length
    cy, cz = (y0 + y1) / 2, (z0 + z1) / 2

    def bar(a0, a1, x0, x1):  # a piece of the buckle: along the strap a0..a1, along the arm x0..x1
        ring = [(cy + ay * a - az * h, cz + az * a + ay * h) for a, h in ((a0, 0.3), (a1, 0.3), (a1, 1.1), (a0, 1.1))]
        return box_tris([(x + a, ring) for a in (x0, x1)])
    solids += [bar(-1.5, -1.0, -1.6, 1.6), bar(1.0, 1.5, -1.6, 1.6), bar(-1.0, 1.0, -1.6, -1.1),
               bar(-1.0, 1.0, 1.1, 1.6), bar(-1.2, 1.2, -0.2, 0.2)]
    return solids


def fence(points, x0, x1, drop, top_z):
    """Chain-link wire lashed over the housing: two sets of slanting strands that follow the
    surface, with a ragged edge toward the hand and one side hanging lower than the other."""
    def line(x):
        slab = [(y, z) for a, y, z in points if abs(a - x) < 1.2]
        foot = top_z(x) - drop
        level = [y for y, z in slab if abs(z - foot) < 1.5] or [y for y, _ in slab]
        ends = [(min(level), foot), (max(level), foot)]
        return over(ends + [q for q in slab if q[1] >= foot and ends[0][0] <= q[0] <= ends[1][0]])
    cache = {}

    def surface(x, u):
        key = round(x * 2) / 2
        path = cache.setdefault(key, line(key))
        lengths = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:])]
        left = u * sum(lengths)
        for (a, b), n in zip(zip(path, path[1:]), lengths):
            if left <= n or (a, b) == (path[-2], path[-1]):
                t = min(1.0, left / n) if n else 0.0
                ny, nz = -(b[1] - a[1]) / (n or 1), (b[0] - a[0]) / (n or 1)
                return (x, a[0] + (b[0] - a[0]) * t + ny * 0.8, a[1] + (b[1] - a[1]) * t + nz * 0.8)
            left -= n
    wires, pitch, run = [], 2.4, 6.0
    for lean in (1, -1):
        start = x0 - run
        while start < x1 + run:
            strand = []
            for k in range(25):
                u = 0.02 + 0.93 * k / 24
                x = start + lean * run * (u - 0.5)
                edge = x1 + 1.6 * math.sin(u * 11.0) - 3.0 * u       # ragged and slanted
                if x0 <= x <= edge:
                    strand.append(surface(x, u))
                elif len(strand) > 1:
                    break
            wires += [wire([a, b], 0.3) for a, b in zip(strand, strand[1:])]
            start += pitch
    return wires


def dress(claw, points):
    """Raider fittings over the ritual claw's plain housing, in right forearm coordinates."""
    housing = [(c, q) for c, q in claw if c != BLADE_PART]
    blades = [q for c, q in claw if c == BLADE_PART]
    # One blade pushed further out than the other.
    ahead = moved(blades[-1], blades[-1]["tris"], lambda p: (p[0] + BLADE_STAGGER, p[1], p[2] - 0.3))
    parts = housing + [(BLADE_PART, q) for q in blades[:-1]] + [(BLADE_PART, ahead)]
    solid = list(points)
    for _, q in claw:
        for t in q["tris"]:
            a, b, c = (q["verts"][i] for i in t)
            solid += [tuple(a[n] + (b[n] - a[n]) * j / 3 + (c[n] - a[n]) * k / 3 for n in range(3))
                      for j in range(4) for k in range(4 - j)]
    top = lambda x: max([z for a, y, z in solid if abs(a - x) < 1.2 and abs(y) < 6.0] or [0.0])
    parts += [(CHAIN, q) for q in fence(solid, 6.5, 17.5, 10.0, top)]
    # A heavy bolted band at the elbow end, matching the ram's.
    near = [(y, z + 0.5) for a, y, z in solid if abs(a - 8.0) < 1.5]
    parts += [(CUFF, q) for q in belt(solid, near, 8.0, top(8.0), 9.0, buckle=False)]
    # Odd bolts through the housing's flanks.
    for side in (-1, 1):
        for x, size, low in (((10.5, 1.0, 4.9), (15.0, 0.7, 5.6), (21.5, 0.9, 4.6)) if side > 0
                             else ((12.5, 0.8, 5.2), (20.5, 1.15, 5.0))):
            height = top(x) - low
            parts.append((BAR, hexbolt(x, (side * 6.0, height), (side, 0.0), size, 0.9)))
    return parts


def ram(meshes, points):
    """The ram's parts in left forearm coordinates. The left bone's Z points out of the palm, so
    everything is laid out with +Z as the back of the hand and then turned half round the arm."""
    s = BRICK_SCALE
    c, n = math.cos(math.radians(ROLL)), math.sin(math.radians(ROLL))
    axis = 2 * MIDDLE                              # where the forearm bone lies in these coordinates

    def unroll(p):            # the arm seen from the mount's own frame, where the knuckles are level
        y, z = p[1] - axis, p[2]
        return (p[0], axis + y * c + z * n, z * c - y * n)
    back_of_hand = [unroll((x, 2 * MIDDLE - y, -z)) for x, y, z in points]
    top = lambda x: top_of([(a, b - MIDDLE, c) for a, b, c in back_of_hand], x - 1.0, x + 1.0, 8.0)
    rear = BRICK_AT + BRICK_BACK * s
    # The bars fall from the arm's surface under the cuff, and the brick leans with them.
    rise = LEAN
    up = top(CUFF_AT) - rise * (rear - CUFF_AT)

    def turned(p):            # roll the mount round the arm, then into the left bone's coordinates
        y, z = p[1] - axis, p[2]
        return (p[0], 2 * MIDDLE - (axis + y * c - z * n), -(y * n + z * c))
    cos, sin = 1 / math.hypot(1, rise), rise / math.hypot(1, rise)

    def tilted(x, y, z):          # leaned about the brick's back face to lie along the bars
        dx, dz = x - rear, z - up
        return (rear + dx * cos + dz * sin, y, up - dx * sin + dz * cos)
    parts, outer_bars = [], []
    shape = next(q for q in Nif(os.path.join(meshes, "weapons/powerfist/rebarfist.nif")).shapes()
                 if q["name"] == "RebarFist:0")
    groups = nifpreview["loose_parts"](shape)
    spans = []                    # each loose part's extent along X, Y
    for group in groups:
        own = [shape["verts"][i] for t in group for i in t]
        spans.append([(min(v[a] for v in own), max(v[a] for v in own)) for a in (0, 1)])
    block = next(x for x, y in spans if y[1] - y[0] > 12)
    links = [sum(x) / 2 for x, y in spans if y[1] - y[0] <= 12 and x[1] - x[0] <= 5]
    for group in groups:
        own = [shape["verts"][i] for t in group for i in t]
        xs, ys = [v[0] for v in own], [v[1] for v in own]
        brick = max(ys) - min(ys) > 12
        bar = not brick and max(xs) - min(xs) > 5

        def middle(x, own=own):       # the bar's centre line, which carries its kinks
            near = [v for v in own if abs(v[0] - x) < 0.8] or [min(own, key=lambda v: abs(v[0] - x))]
            return [(min(v[a] for v in near) + max(v[a] for v in near)) / 2 for a in (1, 2)]
        root = middle(max(xs)) if bar else None
        if bar:
            outer_bars.append((0.0, MIDDLE + BRICK_SCALE * root[0]))
            bar_ys = [y for _, y in outer_bars]

        shift = 0.0
        if not brick and not bar:
            # A chain link. The vanilla loop also goes round the fist's front plate, which we do
            # not have, so each link is moved along X (not reshaped) to lie tight on the brick.
            here_x = (min(xs) + max(xs)) / 2
            low_x, high_x = block[0] - CHAIN_OUT, block[1] + CHAIN_OUT
            shift = low_x + (here_x - min(links)) / (max(links) - min(links)) * (high_x - low_x) - here_x

        def fn(p, bar=bar, middle=middle, root=root, low=min(xs), shift=shift):
            if not bar:
                return turned(tilted(BRICK_AT + s * (p[0] + shift), MIDDLE + s * p[1], up + s * p[2]))
            here = middle(p[0])
            y, z = MIDDLE + s * (root[0] + p[1] - here[0]), s * (p[2] - here[1])
            if p[0] >= BRICK_BACK:    # the part inside the brick leans with it
                return turned(tilted(BRICK_AT + s * p[0], y, up + z))
            # Every bar reaches the same end, in a straight line.
            x = rear + (p[0] - BRICK_BACK) / (BRICK_BACK - low) * (rear - BAR_END)
            return turned((x, y, up + rise * (rear - x) + z))
        parts.append((BRICK if brick else BAR if bar else CHAIN, moved(shape, group, fn)))
        if bar:     # and the same bar reaching out in front, as on the Puncturing Power Fist
            # Cut short and left crooked, each differently: the vanilla kinks are squeezed into
            # the new length, then the bar is wrenched aside and part way round.
            which = 1 if abs(root[0]) < 2 else (0 if root[0] > 0 else 2)
            length, aside, lift, swirl = SPIKES[which]

            def spike(p, low=min(xs), length=length, aside=aside, lift=lift, swirl=swirl):
                out = max(0.0, block[0] - p[0])               # source distance past the brick
                t = min(1.0, out / (block[0] - low))
                x = p[0] if out == 0 else block[0] - t * length / s
                y = MIDDLE - s * p[1] + aside * t * t + swirl * math.sin(math.pi * t)
                z = up + s * p[2] + lift * t * t + swirl * (1 - math.cos(math.pi * t)) / 2
                return turned(tilted(BRICK_AT - s * x, y, z))
            parts.append((BAR, moved(shape, group, spike)))

    # The cuff: the Power Fist's ring, stretched to go round the arm and the bars on it.
    fist = next(q for q in Nif(os.path.join(meshes, "weapons/powerfist/powerfist.nif")).shapes()
                if q["name"] == "DeathclawGauntlet:1")
    # Only the ring's upper arc, at its own proportions: its ends sink into the arm and the rest
    # rises over the bars like a hoop.
    ring = [t for g in nifpreview["loose_parts"](fist) for t in g
            if all(CUFF_X[0] <= fist["verts"][i][0] <= CUFF_X[1] for q in g for i in q)
            and min(fist["verts"][i][2] for i in t) >= CUFF_AXIS[1] - 0.5]
    # Raised until the outer bars run into the ring rather than over it.
    outer = max(abs(v[1] - MIDDLE) for v in outer_bars)
    mid = CUFF_SIZE * CUFF_MIDDLE
    centre = up + rise * (rear - CUFF_AT) - CUFF_FLAT * math.sqrt(mid * mid - outer * outer)

    def around(p):
        return turned((CUFF_AT + p[0] - sum(CUFF_X) / 2, MIDDLE + CUFF_SIZE * (p[1] - CUFF_AXIS[0]),
                       centre + CUFF_FLAT * CUFF_SIZE * (p[2] - CUFF_AXIS[1])))
    parts.append((CUFF, moved(fist, ring, around)))

    # A foot under the ring, filling down into the arm and spreading along it, so no gap shows.
    sections = []
    for k in range(13):
        y = -mid + 2 * mid * k / 12
        under = [v[2] for v in back_of_hand if abs(v[0] - CUFF_AT) < 2.5 and abs(v[1] - MIDDLE - y) < 1.2]
        crown = centre + CUFF_FLAT * math.sqrt(max(0.0, mid * mid - y * y))
        floor = min(crown - 0.5, (max(under) if under else centre - 3.0) - 1.5)
        sections.append((MIDDLE + y, [(CUFF_AT - FOOT_TOP, crown), (CUFF_AT + FOOT_TOP, crown),
                                      (CUFF_AT + FOOT_BASE, floor), (CUFF_AT - FOOT_BASE, floor)]))
    foot = box_tris(sections)                      # built along y: swap the first two axes
    parts.append((CUFF, moved(foot, foot["tris"], lambda p: turned((p[1], p[0], p[2])))))

    bar_z = up + rise * (rear - STRAP_AT)
    bars = [(y + d, bar_z + h) for y in bar_ys for d, h in ((-1.2, 0.6), (0.0, 1.4), (1.2, 0.6))]
    parts += [(STRAP, moved(q, q["tris"], turned))
              for q in belt(back_of_hand, bars, STRAP_AT, bar_z, STRAP_DROP)]
    print("brick %.1f..%.1f along the forearm before leaning; bars and brick lean %.2f per unit"
          % (rear, BRICK_AT - BRICK_BACK * s, rise))
    return parts


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("meshes")
    ap.add_argument("outdir")
    ap.add_argument("--suit", action="store_true")
    args = ap.parse_args()
    meshes = args.meshes
    if os.path.isdir(os.path.join(meshes, "meshes")):
        meshes = os.path.join(meshes, "meshes")
    pa = os.path.join(meshes, "actors/powerarmor/characterassets")
    bones = place["skeleton"](os.path.join(pa, "skeleton.nif"))
    left, left_points = arm(meshes, bones, "L")
    os.makedirs(args.outdir, exist_ok=True)

    parts = ram(meshes, left_points)
    shown = [(SUIT, q) for q in left] + parts
    # Turned half round so the back of the hand is up in the picture.
    shown = [(c, moved(q, q["tris"], lambda p: (p[0], -p[1], -p[2]))) for c, q in shown]
    render([(c, (q, q["tris"])) for c, q in shown], 600, os.path.join(args.outdir, "wrist_v2_arm.png"))
    print("arm drawn", flush=True)

    right, right_points = arm(meshes, bones, "R")
    # The claw is laid out with the right hand's knuckles level, then rolled round the arm to match.
    c, n = math.cos(math.radians(-ROLL)), math.sin(math.radians(-ROLL))
    level = [(x, y * c + z * n, z * c - y * n) for x, y, z in right_points]
    claw, _ = claws["build"]("ritual", meshes, level)
    bend = claws["pitched"](9.0)
    claw = claw[:1] + [(k, moved(q, q["tris"], bend)) for k, q in claw[1:]]
    claw = [(k, moved(q, q["tris"], lambda p: (p[0], p[1] * c - p[2] * n, p[1] * n + p[2] * c)))
            for k, q in dress(claw, level)]
    render([(SUIT, (q, q["tris"])) for q in right] + [(c, (q, q["tris"])) for c, q in claw], 600,
           os.path.join(args.outdir, "claw_v2_arm.png"))
    print("claw drawn", flush=True)

    if args.suit:
        suit = []
        for model in ("frame.nif",) + tuple("mods/pa_raider_%s.nif" % n for n in
                                             ("body", "helmet", "larm", "rarm", "lleg", "rleg")):
            suit += [(SUIT, (q, q["tris"])) for q in place["posed"](os.path.join(pa, model), bones)]
        # The claw's own colours are the blade (red) and its housing (blue).
        for bone, parts in (("RArm_ForeArm1", claw), ("LArm_ForeArm1", parts)):
            for c, q in parts:
                worn = moved(q, q["tris"], lambda p, bone=bone: place["to_model"](bones[bone], p))
                suit.append((c, (worn, worn["tris"])))
        render(suit, 600, os.path.join(args.outdir, "suit_wrist_v2.png"))
        print("suit drawn")


if __name__ == "__main__":
    main()

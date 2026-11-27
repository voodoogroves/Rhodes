#!/usr/bin/env python3
"""Preview claw layouts on the power armor right forearm. Standard library only.

  python3 -I placeclaw.py MESHES OUTDIR [--claw ritual|shishkebab|officer|assaultron|assaultron_shock|all] [--pitch 9] [--roll N] [--no-suit]

MESHES is a folder holding these, extracted with baunpack from "Fallout4 - Meshes.ba2":
  actors/powerarmor/characterassets/{skeleton.nif, frame.nif, mods/pa_t60_rarm.nif}
  weapons/machete/sacrificalblade.nif
  weapons/chineseofficersword/serratedbladeshock.nif
  weapons/shishkebab/shishkebab.nif
  weapons/laserweapons/{laserreceiver.nif, laserpistolbarrel.nif}
and from "DLCRobot - Main.ba2":
  dlc01/weapons/assaultronblade/{vibroblade.nif, electroblade.nif}

Everything is laid out in right forearm bone coordinates: X toward the hand (elbow 0, hand
joint 27), Y across the knuckles (thumb side positive), Z out of the back of the hand. The
chassis is a placeholder generated here. Writes <claw>_arm.png (close up, in forearm
coordinates) and <claw>_suit.png (slow; --no-suit skips it). --pitch angles everything beyond
the chassis down toward the fist, in degrees. Previews only: no game model is written. The previews are
derived from game files: keep them out of every repo.
"""
import argparse
import math
import os
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))
place = runpy.run_path(os.path.join(HERE, "placeshield.py"))
nifpreview = runpy.run_path(os.path.join(HERE, "nifpreview.py"))
Nif, render = nifpreview["Nif"], nifpreview["render"]

BONE = "RArm_ForeArm1"
ARM = ("RArm_ForeArm", "RArm_Hand", "RArm_Finger")
# Preview colours (nifpreview part numbers).
BLADE, CHASSIS, EXTRA, EXTRA2, SUIT = 1, 2, 4, 3, 10

# source: model, shape, loose part number (None: the whole shape); length along the source Y
# is scaled by `scale`; flip turns the blade's width so a hooked tip curves toward the fist.
CLAWS = {
    "ritual": {"source": ("weapons/machete/sacrificalblade.nif", "SacrificalBlade:0", None),
               "scale": 0.8, "flip": 1, "blades": ((-4.2, 0.0), (4.2, 0.0)), "roll": 45.0,
               "back": 11.0,             # tips end among the fingers
               "saddle": True},          # at roll 45: blades lie on the block's bevels, strapped down
    "assaultron": {"source": ("dlc01/weapons/assaultronblade/vibroblade.nif", "VibroBlade:0", None),
                   "scale": 0.75, "flip": 1, "blades": ((-4.2, 0.0), (0.0, 5.0), (4.2, 0.0))},
    "officer": {"source": ("weapons/chineseofficersword/serratedbladeshock.nif", "SerratedBladeShock:0", None),
                "scale": 0.65, "flip": 1, "blades": ((-3.2, 0.0), (3.2, 0.0)), "roll": 90.0, "back": 12.0},
    "assaultron_shock": {"source": ("dlc01/weapons/assaultronblade/electroblade.nif", "ElectroBlade:0", None),
                         "scale": 0.75, "flip": 1, "blades": ((-4.2, 0.0), (0.0, 0.0), (4.2, 0.0)), "roll": 0.0,
                         "back": 9.7,       # points among the fingers, level with the officer's
                         "cut": 9.0},       # drop anything that would stick out behind the housing
    "officer_laser": {"source": ("weapons/chineseofficersword/serratedbladeshock.nif", "SerratedBladeShock:0", None),
                      "scale": 0.65, "flip": 1, "blades": ((-2.5, 0.0), (2.5, 0.0)), "roll": 90.0, "back": 12.0,
                      "cut": 22.5, "pistols": True},   # preview only: writeclaw.py cannot write it yet
    "shishkebab": {"source": ("weapons/shishkebab/shishkebab.nif", "Shishkebab_02:0", 18),
                   "scale": 0.75, "flip": 1, "blades": ((-3.2, 0.0), (3.2, 0.0))},
}
BLADE_ROOT = 21.0                 # where a blade leaves the chassis, along the forearm
CLEAR = 0.6                       # gap kept between the blades and the hand
CHASSIS_X = (7.0, 23.0)           # the chassis runs between these along the forearm
HALF_WIDTH = (6.2, 5.6)           # half its width at those two ends
SADDLE_WIDTH, SADDLE_BEVEL = 6.0, 4.0   # the strapped block: half width, and its 45 degree faces
STRAPS = (13.0, 19.0)             # where the straps cross it
BATTERIES = (9.4, 13.1, 16.8, 20.5)  # middles of the officer claw's packs, along the forearm
BATTERY_SIZE = 0.82               # the vanilla pack's scale
MUZZLE = 24.5                     # where the laser pistols' barrels end, along the forearm
PISTOL_SIZE = 0.62
# The pistol's parts, and where each sits in the assembled gun (along source X, Y, Z).
PISTOL = (("weapons/laserweapons/laserreceiver.nif", (0.0, 0.0, 0.0)),
          ("weapons/laserweapons/laserpistolbarrel.nif", (0.0, 11.9, 2.8)))


def shape_of(path, name):
    return next(s for s in Nif(path).shapes() if s["name"] == name)


def moved(shape, tris, fn):
    used = sorted({i for t in tris for i in t})
    index = {old: n for n, old in enumerate(used)}
    return {"verts": [fn(shape["verts"][i]) for i in used], "used": used, "fn": fn, "source": shape,
            "tris": [tuple(index[i] for i in t) for t in tris], "weights": [], "bones": []}


def box_tris(sections):
    """A closed solid through cross-sections [(x, [(y, z), ...]), ...] of equal point counts."""
    n = len(sections[0][1])
    verts = [(x, y, z) for x, ring in sections for y, z in ring]
    tris = []
    for s in range(len(sections) - 1):
        for i in range(n):
            a, b = s * n + i, s * n + (i + 1) % n
            tris += [(a, b, b + n), (a, b + n, a + n)]
    for end in (0, len(sections) - 1):
        tris += [(end * n, end * n + i, end * n + i + 1) for i in range(1, n - 1)]
    return {"verts": verts, "tris": tris, "weights": [], "bones": []}


def top_of(points, x0, x1, half):
    """Highest Z among arm points between x0 and x1 within half of the middle."""
    z = [p[2] for p in points if x0 <= p[0] <= x1 and abs(p[1]) <= half]
    return max(z) if z else 0.0


def chassis(surface):
    sections, tops = [], []
    steps = 5
    for k in range(steps):
        x = CHASSIS_X[0] + (CHASSIS_X[1] - CHASSIS_X[0]) * k / (steps - 1)
        w = HALF_WIDTH[0] + (HALF_WIDTH[1] - HALF_WIDTH[0]) * k / (steps - 1)
        z = top_of(surface, x - 2, x + 2, w)
        lid = z + 2.2
        tops.append((x, lid))
        sections.append((x, [(-w, z - 2.5), (-w, lid - 1.2), (-w * 0.65, lid),
                             (w * 0.65, lid), (w, lid - 1.2), (w, z - 2.5)]))
    return box_tris(sections), tops


def wire(points, radius=0.25):
    """A square-section cable through the points."""
    ring = ((-radius, 0), (0, -radius), (radius, 0), (0, radius))
    verts = [(x, y + dy, z + dz) for x, y, z in points for dy, dz in ring]
    tris = []
    for s in range(len(points) - 1):
        for i in range(4):
            a, b = s * 4 + i, s * 4 + (i + 1) % 4
            tris += [(a, b, b + 4), (a, b + 4, a + 4)]
    return {"verts": verts, "tris": tris, "weights": [], "bones": []}


def saddle(surface, thick):
    """A block with a straight sloping top and two 45 degree faces, with straps and bolt heads
    over blades `thick` deep lying on those faces. Returns the block, the rest, and the top's
    height at any x."""
    w, b = SADDLE_WIDTH, SADDLE_BEVEL
    slope = math.tan(math.radians(9.0))              # the default --pitch
    x0, x1 = CHASSIS_X
    end = max(p[2] - slope * (x1 - p[0]) for p in surface if x0 <= p[0] <= x1 and abs(p[1]) <= w) + 2.2

    def lid(x):
        return end + slope * (x1 - x)
    body = box_tris([(x, [(-w, lid(x) - b - 2.5), (-w, lid(x) - b), (b - w, lid(x)),
                          (w - b, lid(x)), (w, lid(x) - b), (w, lid(x) - b - 2.5)]) for x in CHASSIS_X])
    high, n = thick + 0.35, math.sqrt(0.5)
    rest = []
    for middle in STRAPS:
        ends = (middle - 0.7, middle + 0.7)
        corner = w - b + high * (math.sqrt(2) - 1)
        rest.append(box_tris([(x, [(-corner, lid(x) - 0.2), (corner, lid(x) - 0.2),
                                   (corner, lid(x) + high), (-corner, lid(x) + high)]) for x in ends]))
        for side in (-1, 1):
            def face(x, side=side):
                top, low = (w - b, lid(x)), (w, lid(x) - b)
                ring = [(top, -0.2), (low, -0.2), (low, high), (top, high)]
                return [(side * (y + n * out), z + n * out) for (y, z), out in ring]
            rest.append(box_tris([(x, face(x)) for x in ends]))
        for y in (-1.1, 1.1):                        # bolt heads on the strap's top
            ring = lambda x: [(y + 0.45 * math.cos(k * math.pi / 3), x[1] + 0.45 * math.sin(k * math.pi / 3))
                              for k in range(6)]
            z = lid(middle) + high
            hexagon = [(middle + 0.45 * math.cos(k * math.pi / 3), y + 0.45 * math.sin(k * math.pi / 3))
                       for k in range(6)]
            verts = [(x, v, z + up) for up in (-0.1, 0.35) for x, v in hexagon]
            tris = []
            for i in range(6):
                j = (i + 1) % 6
                tris += [(i, j, j + 6), (i, j + 6, i + 6)]
            for base in (0, 6):
                tris += [(base, base + i, base + i + 1) for i in range(1, 5)]
            rest.append({"verts": verts, "tris": tris, "weights": [], "bones": []})
    return body, rest, lid


def build(claw, meshes, surface, roll=None):
    spec = CLAWS[claw]
    turn = math.radians(spec.get("roll", 0.0) if roll is None else roll)
    path, name, part = spec["source"]
    shape = shape_of(os.path.join(meshes, path), name)
    tris = nifpreview["loose_parts"](shape)[part - 1] if part else shape["tris"]
    ys = [shape["verts"][i][1] for t in tris for i in t]
    xs = [shape["verts"][i][0] for t in tris for i in t]
    root, scale, flip = min(ys), spec["scale"], spec["flip"]
    body, tops = chassis(surface)
    half_blade = scale * (max(xs) - min(xs)) / 2
    # Blades sit just above the hand and are never buried below the chassis mouth.
    upright = half_blade * abs(math.cos(turn))       # how far a rolled blade reaches up and down
    height = max(top_of(surface, BLADE_ROOT, 50, 7) + CLEAR + upright, tops[-1][1] - upright - 0.4)
    # Centre the blade's width where it leaves the chassis.
    low = [shape["verts"][i][0] for t in tris for i in t if shape["verts"][i][1] < root + 6]
    mid = (min(low) + max(low)) / 2
    parts = [(CHASSIS, body)]
    strapped = spec.get("saddle") and abs(math.degrees(turn) - 45.0) < 0.01
    if strapped:
        depth = [shape["verts"][i][2] for t in tris for i in t]
        thick = scale * (max(depth) - min(depth))
        body, straps, lid = saddle(surface, thick)
        parts = [(CHASSIS, body)] + [(CHASSIS, q) for q in straps]
        height = lid(BLADE_ROOT) - SADDLE_BEVEL / 2
        slope = math.tan(math.radians(9.0))
    if spec.get("pistols"):
        slope = math.tan(math.radians(9.0))              # the default --pitch
        rise = lambda x: slope * max(0.0, BLADE_ROOT - x)
        height = max(p[2] - rise(p[0]) for p in surface if 7 <= p[0] <= 30 and abs(p[1]) <= 6) + 2.4
        bands = []
        for x in (11.0, 19.5):                           # straps holding the pistols to the arm
            z = height + rise(x)
            ring = [(-6.0, z - 3.6), (-6.0, z - 1.2), (6.0, z - 1.2), (6.0, z - 3.6)]
            bands.append(box_tris([(x - 0.9, ring), (x + 0.9, ring)]))
        parts = [(CHASSIS, bands[0]), (CHASSIS, bands[1])]
    for across, ahead in spec["blades"]:
        def fn(p, across=across, ahead=ahead):
            # source (width, length, thickness) -> forearm (length, thickness, width), then
            # rolled about the blade's length: positive turns the lower edge away from the middle.
            y, z = scale * p[2], flip * scale * (p[0] - mid)
            side = 1 if across > 0 else -1 if across < 0 else 0
            c, s = (math.cos(turn), math.sin(turn)) if side else (1.0, 0.0)
            x = BLADE_ROOT + ahead - spec.get("back", 0.0) + scale * (p[1] - root)
            at, up = across, height
            if strapped:                  # onto the bevel's face, following the block's slope
                out = (thick / 2 + 0.1) * math.sqrt(0.5)
                at = side * (SADDLE_WIDTH - SADDLE_BEVEL / 2 + out)
                up = height + out + slope * max(0.0, BLADE_ROOT - x)
            return (x, at + y * c - side * z * s, up + side * y * s + z * c)
        # Triangles reaching behind the cut are left off; the ragged edge sits inside the housing.
        shown = [t for t in tris if min(fn(shape["verts"][i])[0] for i in t) >= spec.get("cut", -1e9)]
        parts.append((BLADE, moved(shape, shown, fn)))
        if ahead:                     # a collar carries the blade that starts further forward
            ring = [(across - 1.0, height - half_blade * 0.6), (across - 1.0, height + half_blade * 0.6),
                    (across + 1.0, height + half_blade * 0.6), (across + 1.0, height - half_blade * 0.6)]
            parts.append((CHASSIS, box_tris([(CHASSIS_X[1] - 0.5, ring), (BLADE_ROOT + ahead + 1.5, ring)])))

    if spec.get("pistols"):
        for across, _ in spec["blades"]:
            for model, at in PISTOL:
                for piece in Nif(os.path.join(meshes, model)).shapes():
                    def gun(p, across=across, at=at):
                        x = MUZZLE - PISTOL_SIZE * (26.6 - (p[1] + at[1]))
                        return (x, across - PISTOL_SIZE * (p[0] + at[0]),
                                height + rise(x) + PISTOL_SIZE * (p[2] + at[2] - 2.2))
                    parts.append((EXTRA, moved(piece, piece["tris"], gun)))
        coil = shape_of(os.path.join(meshes, path), "SerratedBladeShock:1")
        for across, _ in spec["blades"]:
            side = 1 if across > 0 else -1

            def wrap(p, across=across, side=side):       # the vanilla coil just past the muzzle
                y, z = 1.4 * scale * p[2], 1.4 * scale * p[0]
                c, s = math.cos(turn), math.sin(turn)
                return (MUZZLE + 1.8 + scale * p[1], across + y * c - side * z * s, height + side * y * s + z * c)
            parts.append((EXTRA2, moved(coil, coil["tris"], wrap)))
            top = lambda x, up: height + rise(x) + up
            runs = ([(8.0, across + side * 0.5, top(8.0, 2.2)), (11.0, across + side * 3.6, top(11.0, 4.0)),
                     (19.0, across + side * 4.0, top(19.0, 2.4)), (MUZZLE + 2.0, across + side * 1.4, height + 0.6)],
                    [(13.0, across + side * 1.0, top(13.0, 2.6)), (18.0, across + side * 1.8, top(18.0, 4.8)),
                     (23.0, across + side * 0.6, top(23.0, 3.0)), (MUZZLE + 1.0, across, height + 0.9)])
            for run in runs:
                parts += [(EXTRA2, wire(run[n:n + 2])) for n in range(len(run) - 1)]
        link = [(9.0, -2.5, height + rise(9.0) + 2.4), (10.0, -0.8, height + rise(10.0) + 4.4),
                (13.0, 0.9, height + rise(13.0) + 4.0), (15.0, 2.5, height + rise(15.0) + 2.6)]
        parts += [(EXTRA2, wire(link[n:n + 2])) for n in range(len(link) - 1)]

    if claw == "officer":
        source = os.path.join(meshes, path)
        coil = shape_of(source, "SerratedBladeShock:1")
        for across, _ in spec["blades"]:
            def wrap(p, across=across):       # the vanilla coil, kept on each blade's root
                y, z = 1.4 * scale * p[2], 1.4 * scale * p[0]
                side = 1 if across > 0 else -1
                c, s = math.cos(turn), math.sin(turn)
                return (CHASSIS_X[1] + 4.5 + scale * p[1], across + y * c - side * z * s,
                        height + side * y * s + z * c)
            parts.append((EXTRA2, moved(coil, coil["tris"], wrap)))
        pack = shape_of(source, "SerratedBladeShock:2")
        # The pack's own body only: its two small outlying pieces would float.
        body_tris = [t for t in pack["tris"] if max(pack["verts"][i][1] for i in t) < -1.0]

        def lid(x):                       # the chassis top at x
            for (x0, z0), (x1, z1) in zip(tops, tops[1:]):
                if x <= x1:
                    return z0 + (z1 - z0) * max(0.0, x - x0) / (x1 - x0)
            return tops[-1][1]
        size = BATTERY_SIZE
        for centre in BATTERIES:          # a line of small packs along the chassis top
            def battery(p, centre=centre):
                x = centre + size * (p[1] + 3.37)
                return (x, -size * (p[0] - 0.1), lid(x) + size * (p[2] + 0.2))
            parts.append((EXTRA, moved(pack, body_tris, battery)))
        # Jumpers from one pack to the next, crossing over so they read as wired in a row.
        top = size * 2.3
        for first, second in zip(BATTERIES, BATTERIES[1:]):
            parts.append((EXTRA2, wire([(first + 0.2, 0.8, lid(first + 0.2) + top),
                                        (second - 0.2, -0.8, lid(second - 0.2) + top)])))
        for across, _ in spec["blades"]:
            side = 1 if across > 0 else -1
            run = [(BATTERIES[0], side * 1.4, lid(BATTERIES[0]) + 1.2), (18.0, side * 4.6, lid(18.0) + 0.6),
                   (CHASSIS_X[1], across + side * 1.2, height + 2.2), (CHASSIS_X[1] + 3.5, across, height + 0.8)]
            # One solid per straight run, so each can be given outward faces.
            parts += [(EXTRA2, wire(run[n:n + 2])) for n in range(len(run) - 1)]

    if claw == "shishkebab":
        # Everything on the sword except its grip, trigger lever and blade: tank, valve, pipes.
        solid = shape_of(os.path.join(meshes, path), name)
        loose = nifpreview["loose_parts"](solid)
        kit = [t for n, group in enumerate(loose, 1) if n not in (1, 4, part)
               and max(solid["verts"][i][1] for t in group for i in t) > 2 for t in group]
        floor = min(solid["verts"][i][2] for t in kit for i in t if solid["verts"][i][0] > 2)
        lid = max(z for _, z in tops[:4])

        def hardware(p, grow=0.9):
            return (6.0 + grow * (p[1] - 2.0), grow * (p[0] - 1.0), lid + grow * (p[2] - floor) - 0.8)
        parts.append((EXTRA, moved(solid, kit, hardware)))
    return parts, height


def suit_arm(meshes):
    """The suit's models posed on its skeleton, its right arm in forearm bone coordinates, and
    points spread over that arm."""
    pa = os.path.join(meshes, "actors/powerarmor/characterassets")
    bones = place["skeleton"](os.path.join(pa, "skeleton.nif"))
    suit, local = [], []
    for model in ("frame.nif", "mods/pa_t60_rarm.nif"):
        for s in place["posed"](os.path.join(pa, model), bones):
            suit.append((SUIT, (s, s["tris"])))
            tris = [t for t in s["tris"] if all(place["dominant"](s, i).startswith(ARM) for i in t)]
            if tris:
                local.append(moved(s, tris, lambda p: place["to_bone"](bones[BONE], p)))
    # Points spread over the arm, so the gaps between vertices count too.
    surface = []
    for s in local:
        for t in s["tris"]:
            a, b, c = (s["verts"][i] for i in t)
            surface += [tuple(a[n] + (b[n] - a[n]) * j / 4 + (c[n] - a[n]) * k / 4 for n in range(3))
                        for j in range(5) for k in range(5 - j)]
    return bones, suit, local, surface


def pitched(degrees):
    """Angle everything beyond the chassis mouth down toward the fist."""
    drop = math.tan(math.radians(degrees))
    return lambda p: (p[0], p[1], p[2] - drop * max(0.0, p[0] - BLADE_ROOT))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("meshes")
    ap.add_argument("outdir")
    ap.add_argument("--claw", default="all", choices=list(CLAWS) + ["all"])
    ap.add_argument("--pitch", type=float, default=9.0)
    ap.add_argument("--no-suit", action="store_true")
    ap.add_argument("--roll", type=float, help="roll the blades: 0 edge down, 90 outward, -90 inward")
    args = ap.parse_args()
    bones, suit, local, surface = suit_arm(args.meshes)
    to_model = place["to_model"]

    os.makedirs(args.outdir, exist_ok=True)
    for claw in CLAWS if args.claw == "all" else (args.claw,):
        parts, height = build(claw, args.meshes, surface, args.roll)
        # The first part is the chassis itself, which stays put.
        bend = pitched(args.pitch)
        parts = parts[:1] + [(c, moved(q, q["tris"], bend)) for c, q in parts[1:]]
        close = [(SUIT, (s, s["tris"])) for s in local] + [(c, (s, s["tris"])) for c, s in parts]
        render(close, 600, os.path.join(args.outdir, claw + "_arm.png"))
        if not args.no_suit:
            worn = [(c, moved(s, s["tris"], lambda p: to_model(bones[BONE], p))) for c, s in parts]
            render(suit + [(c, (s, s["tris"])) for c, s in worn], 600,
                   os.path.join(args.outdir, claw + "_suit.png"))
        tip = max(p[0] for c, s in parts if c == BLADE for p in s["verts"])
        print("%s: blade middle height %.1f, longest tip %.1f along the forearm (hand joint 27), %d triangles"
              % (claw, height, tip, sum(len(s["tris"]) for _, s in parts)))


if __name__ == "__main__":
    main()

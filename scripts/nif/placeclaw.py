#!/usr/bin/env python3
"""Preview claw layouts on the power armor right forearm. Standard library only.

  python3 -I placeclaw.py MESHES OUTDIR [--claw ritual|shishkebab|officer|assaultron|all] [--pitch 9] [--no-suit]

MESHES is a folder holding these, extracted with baunpack from "Fallout4 - Meshes.ba2":
  actors/powerarmor/characterassets/{skeleton.nif, frame.nif, mods/pa_t60_rarm.nif}
  weapons/machete/sacrificalblade.nif
  weapons/chineseofficersword/serratedbladeshock.nif
  weapons/shishkebab/shishkebab.nif
and from "DLCRobot - Main.ba2":
  dlc01/weapons/assaultronblade/vibroblade.nif

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
               "scale": 0.8, "flip": 1, "blades": ((-4.2, 0.0), (0.0, 5.0), (4.2, 0.0))},
    "assaultron": {"source": ("dlc01/weapons/assaultronblade/vibroblade.nif", "VibroBlade:0", None),
                   "scale": 0.75, "flip": 1, "blades": ((-4.2, 0.0), (0.0, 5.0), (4.2, 0.0))},
    "officer": {"source": ("weapons/chineseofficersword/serratedbladeshock.nif", "SerratedBladeShock:0", None),
                "scale": 0.65, "flip": 1, "blades": ((-3.2, 0.0), (3.2, 0.0))},
    "shishkebab": {"source": ("weapons/shishkebab/shishkebab.nif", "Shishkebab_02:0", 18),
                   "scale": 0.75, "flip": 1, "blades": ((-3.2, 0.0), (3.2, 0.0))},
}
BLADE_ROOT = 21.0                 # where a blade leaves the chassis, along the forearm
CLEAR = 0.6                       # gap kept between the blades and the hand
CHASSIS_X = (7.0, 23.0)           # the chassis runs between these along the forearm
HALF_WIDTH = (6.2, 5.6)           # half its width at those two ends


def shape_of(path, name):
    return next(s for s in Nif(path).shapes() if s["name"] == name)


def moved(shape, tris, fn):
    used = sorted({i for t in tris for i in t})
    index = {old: n for n, old in enumerate(used)}
    return {"verts": [fn(shape["verts"][i]) for i in used],
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


def build(claw, meshes, surface):
    spec = CLAWS[claw]
    path, name, part = spec["source"]
    shape = shape_of(os.path.join(meshes, path), name)
    tris = nifpreview["loose_parts"](shape)[part - 1] if part else shape["tris"]
    ys = [shape["verts"][i][1] for t in tris for i in t]
    xs = [shape["verts"][i][0] for t in tris for i in t]
    root, scale, flip = min(ys), spec["scale"], spec["flip"]
    body, tops = chassis(surface)
    half_blade = scale * (max(xs) - min(xs)) / 2
    # Blades sit just above the hand and are never buried below the chassis mouth.
    height = max(top_of(surface, BLADE_ROOT, 50, 7) + CLEAR + half_blade, tops[-1][1] - half_blade - 0.4)
    # Centre the blade's width where it leaves the chassis.
    low = [shape["verts"][i][0] for t in tris for i in t if shape["verts"][i][1] < root + 6]
    mid = (min(low) + max(low)) / 2
    parts = [(CHASSIS, body)]
    for across, ahead in spec["blades"]:
        def fn(p, across=across, ahead=ahead):
            # source (width, length, thickness) -> forearm (length, thickness, width)
            return (BLADE_ROOT + ahead + scale * (p[1] - root), across + scale * p[2],
                    height + flip * scale * (p[0] - mid))
        parts.append((BLADE, moved(shape, tris, fn)))
        if ahead:                     # a collar carries the blade that starts further forward
            ring = [(across - 1.0, height - half_blade * 0.6), (across - 1.0, height + half_blade * 0.6),
                    (across + 1.0, height + half_blade * 0.6), (across + 1.0, height - half_blade * 0.6)]
            parts.append((CHASSIS, box_tris([(CHASSIS_X[1] - 0.5, ring), (BLADE_ROOT + ahead + 1.5, ring)])))

    if claw == "officer":
        source = os.path.join(meshes, path)
        coil = shape_of(source, "SerratedBladeShock:1")
        for across, _ in spec["blades"]:
            def wrap(p, across=across):       # the vanilla coil, kept on each blade's root
                return (CHASSIS_X[1] + 4.5 + scale * p[1], across + 1.4 * scale * p[2], height + 1.4 * scale * p[0])
            parts.append((EXTRA2, moved(coil, coil["tris"], wrap)))
        pack = shape_of(source, "SerratedBladeShock:2")
        lid = max(z for _, z in tops[1:4])

        def battery(p, grow=1.8):
            return (14.0 + grow * (p[1] + 1.0), -grow * p[0], lid + grow * (p[2] + 0.2))
        # The pack's own body only: its two small outlying pieces would float.
        body_tris = [t for t in pack["tris"] if max(pack["verts"][i][1] for i in t) < -1.0]
        parts.append((EXTRA, moved(pack, body_tris, battery)))
        for across, _ in spec["blades"]:
            side = 1 if across > 0 else -1
            parts.append((EXTRA2, wire([(10.5, side * 2.5, lid + 2.0), (18.0, side * 4.6, lid + 2.2),
                                        (CHASSIS_X[1], across + side * 1.2, height + 2.2),
                                        (CHASSIS_X[1] + 3.5, across, height + 0.8)])))

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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("meshes")
    ap.add_argument("outdir")
    ap.add_argument("--claw", default="all", choices=list(CLAWS) + ["all"])
    ap.add_argument("--pitch", type=float, default=9.0)
    ap.add_argument("--no-suit", action="store_true")
    args = ap.parse_args()
    pa = os.path.join(args.meshes, "actors/powerarmor/characterassets")
    bones = place["skeleton"](os.path.join(pa, "skeleton.nif"))
    to_bone, to_model, dominant = place["to_bone"], place["to_model"], place["dominant"]

    suit, local = [], []
    for model in ("frame.nif", "mods/pa_t60_rarm.nif"):
        for s in place["posed"](os.path.join(pa, model), bones):
            suit.append((SUIT, (s, s["tris"])))
            tris = [t for t in s["tris"] if all(dominant(s, i).startswith(ARM) for i in t)]
            if tris:
                local.append(moved(s, tris, lambda p: to_bone(bones[BONE], p)))
    # Points spread over the arm, so the gaps between vertices count too.
    surface = []
    for s in local:
        for t in s["tris"]:
            a, b, c = (s["verts"][i] for i in t)
            surface += [tuple(a[n] + (b[n] - a[n]) * j / 4 + (c[n] - a[n]) * k / 4 for n in range(3))
                        for j in range(5) for k in range(5 - j)]

    os.makedirs(args.outdir, exist_ok=True)
    for claw in CLAWS if args.claw == "all" else (args.claw,):
        parts, height = build(claw, args.meshes, surface)
        drop = math.tan(math.radians(args.pitch))
        parts = [(c, s if c == CHASSIS else moved(s, s["tris"], lambda p: (
            p[0], p[1], p[2] - drop * max(0.0, p[0] - BLADE_ROOT)))) for c, s in parts]
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

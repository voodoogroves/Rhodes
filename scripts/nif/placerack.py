#!/usr/bin/env python3
"""Mock up the Raider shotgun rack: four short shotguns facing forward. Standard library only.

  python3 -I placerack.py MESHES OUTDIR [--full]

MESHES holds these, extracted with baunpack (paths start meshes/ or at the folders below):
  from "Fallout4 - Meshes.ba2": actors/powerarmor/characterassets/{skeleton.nif, frame.nif,
      mods/pa_raider_*.nif}, weapons/powerfist/rebarfist.nif,
      weapons/shotgun/{shotgun, shotgunbarrelshort, shotgunstockshort}.nif and
      weapons/combatshotgun/{combatshotgun, combatshotgunbarrelshort, stockshort, drummag}.nif
  from "ccFRSFO4001-HandmadeShotgun - Main.ba2" (Creation Club):
      weapons/handmadeshotgun/handmadeshotgun_{receiver, triplereceiver, barrelshort,
      barreltripleshort, shortstock}.nif

Along the collar, a handmade triple barrel on the wearer's right and a combat shotgun on the
left; at the belt, a handmade double on the right and the base game's sawed-off on the left;
bolted straps along the sides. Writes rack_front.png (torso, helmet and arms) and with --full
rack_suit.png (whole suit, slow). Model coordinates: X to the wearer's right, Y forward, Z up.
Previews only: no game model is written. The pictures are derived from game files: keep them out
of every repo.
"""
import argparse
import math
import os
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))
ram = runpy.run_path(os.path.join(HERE, "placeram.py"))
place, nifpreview, Nif, render = ram["place"], ram["nifpreview"], ram["Nif"], ram["render"]
moved, box_tris, hexbolt = ram["moved"], ram["box_tris"], ram["hexbolt"]

# Preview colours (nifpreview part numbers).
GUN, WOOD, BAND, BAR, BOLT, SUIT = 1, 9, 2, 3, 5, 10
BARREL_AT = (0.0, 10.63, 4.30)        # where the receivers carry the barrels
SAWED_BARREL_AT = (0.0, 10.82, 3.18)  # the same for the base game's double barrel
COMBAT_BARREL_AT, COMBAT_MAG_AT = (0.0, 23.46, 2.78), (-0.05, 17.14, 0.32)
# Each gun: which, breech end (x, y, z), direction it points, roll about the barrels (degrees),
# size, and barrel (and fore-grip) length against the game's short barrels.
GUNS = (
    ("triple", (12.8, -13.0, 138.0), (0.04, 1.0, 0.02), -9.0, 0.95, 1.0),     # along the collar, right
    ("combat", (-12.8, -14.0, 138.0), (-0.05, 1.0, -0.01), 52.0, 0.92, 0.85),  # along the collar, left
    ("double", (14.5, -19.0, 99.0), (0.05, 1.0, -0.05), -66.0, 0.88, 0.55),    # at the belt, right
    ("sawed", (-14.5, -20.0, 101.0), (-0.04, 1.0, 0.04), 62.0, 0.90, 0.55),    # at the belt, left
)
# Side straps: height, from and to along the suit (front is +), half height.
STRAPS = ((99.5, -22.0, 10.0, 1.5), (134.0, -16.0, 14.0, 1.1))
CLAMP = 15.0                          # how far along a gun its clamp sits


def unit(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def shortened(shape, start, factor):
    """The shape with everything past `start` along the barrels pulled in."""
    return dict(shape, verts=[(v[0], v[1] if v[1] <= start else start + (v[1] - start) * factor, v[2])
                              for v in shape["verts"]])


def gun_parts(meshes, kind, length):
    """A short shotgun's shapes in one frame (barrels along +Y): [(colour, shape, offset)].
    Shells belong to the reload animation and a gun at rest does not show them."""
    def load(path):
        return Nif(os.path.join(meshes, "weapons", path + ".nif")).shapes()
    none = (0.0, 0.0, 0.0)
    if kind in ("double", "triple"):
        head = "handmadeshotgun/handmadeshotgun_"
        receiver, barrel = (("receiver", "barrelshort") if kind == "double"
                            else ("triplereceiver", "barreltripleshort"))
        out = [(WOOD, shortened(q, 12.6, length), none) if q["name"].startswith("Handle")
               else (GUN, shortened(q, 16.0, length) if q["name"].startswith("SightBar") else q, none)
               for q in load(head + receiver) if not q["name"].startswith("ShotgunShell")]
        out += [(GUN, shortened(q, 0.0, length), BARREL_AT) for q in load(head + barrel)]
        return out + [(WOOD, q, none) for q in load(head + "shortstock")]
    if kind == "sawed":
        out = [(GUN, q, none) for q in load("shotgun/shotgun")
               if q["name"].startswith(("ShotgunReceiver", "ShotgunBarrelCatch", "ShotgunTrigger", "Safety"))]
        out += [(GUN, shortened(q, 0.0, length), SAWED_BARREL_AT) for q in load("shotgun/shotgunbarrelshort")]
        return out + [(WOOD, q, none) for q in load("shotgun/shotgunstockshort")]
    out = [(GUN, q, none) for q in load("combatshotgun/combatshotgun")]
    out += [(GUN, shortened(q, 0.0, length), COMBAT_BARREL_AT) for q in load("combatshotgun/combatshotgunbarrelshort")]
    out += [(GUN, q, COMBAT_MAG_AT) for q in load("combatshotgun/drummag") if not q["name"].startswith("ShotgunShell")]
    return out + [(WOOD, q, none) for q in load("combatshotgun/stockshort")]


def gun(parts, breech, direction, roll, size):
    f = unit(direction)
    up = unit(tuple((0.0, 0.0, 1.0)[k] - f[k] * f[2] for k in range(3)))
    right = cross(f, up)
    c, s = math.cos(math.radians(roll)), math.sin(math.radians(roll))
    right, up = (tuple(right[k] * c + up[k] * s for k in range(3)),
                 tuple(up[k] * c - right[k] * s for k in range(3)))
    out = []
    for colour, shape, at in parts:
        def fn(p, at=at):
            x, y, z = p[0] + at[0], p[1] + at[1] + 4.0, p[2] + at[2]
            return tuple(breech[k] + size * (right[k] * x + f[k] * y + up[k] * z) for k in range(3))
        out.append((colour, moved(shape, shape["tris"], fn)))
    return out


def clamp(breech, direction, size, parts):
    """A band drawn tight round a gun's barrels, with a bolt on its outer face."""
    f = unit(direction)
    x, y, z = (breech[k] + f[k] * CLAMP * size for k in range(3))
    near = []
    for _, q in parts:
        for t in q["tris"]:
            a, b, c = (q["verts"][i] for i in t)
            near += [v for v in (tuple(a[n] + (b[n] - a[n]) * j / 4 + (c[n] - a[n]) * k / 4 for n in range(3))
                                 for j in range(5) for k in range(5 - j)) if abs(v[1] - y) < 1.4]
    xs, zs = [v[0] for v in near], [v[2] for v in near]
    x, z = (min(xs) + max(xs)) / 2, (min(zs) + max(zs)) / 2
    w, h, side = (max(xs) - min(xs)) / 2 + 0.1, (max(zs) - min(zs)) / 2 + 0.1, 1.0 if breech[0] > 0 else -1.0
    out = []
    ring = ((-w, -h), (w, -h), (w, h), (-w, h), (-w, -h))
    for (x0, z0), (x1, z1) in zip(ring, ring[1:]):
        length = math.hypot(x1 - x0, z1 - z0)
        nx, nz = (z1 - z0) / length * 0.7, -(x1 - x0) / length * 0.7
        shape = [(x + x0, z + z0), (x + x1, z + z1), (x + x1 + nx, z + z1 + nz), (x + x0 + nx, z + z0 + nz)]
        solid = box_tris([(v, shape) for v in (y - 1.4, y + 1.4)])     # built along x: swap to y
        out.append((BAND, moved(solid, solid["tris"], lambda p: (p[1], p[0], p[2]))))
    bolt = hexbolt(y, (x + side * (w + 0.6), z), (side, 0.0), 1.1, 1.0)
    out.append((BOLT, moved(bolt, bolt["tris"], lambda p: (p[1], p[0], p[2]))))
    return out


def side_strap(body, z, back, front, half):
    """A bolted strap along each side of the suit, following its widest line at that height."""
    out, n = [], 9
    for side in (-1, 1):
        points = []
        for i in range(n + 1):
            y = back + (front - back) * i / n
            near = [side * p[0] for p in body if abs(p[2] - z) < 2.0 and abs(p[1] - y) < 2.5]
            points.append((y, max(near) if near else 0.0))
        # Pulled taut: a strap bridges the hollows.
        taut = [max(points[max(0, i - 1)][1], x, points[min(n, i + 1)][1]) for i, (_, x) in enumerate(points)]
        points = [(y, side * (x + 0.5)) for (y, _), x in zip(points, taut)]
        for (y0, x0), (y1, x1) in zip(points, points[1:]):
            sections = [(y, [(x - 0.55, z - half), (x + 0.55, z - half), (x + 0.55, z + half),
                             (x - 0.55, z + half)]) for y, x in ((y0, x0), (y1, x1))]
            solid = box_tris(sections)                      # built along y: swap the first two axes
            out.append((BAND, moved(solid, solid["tris"], lambda p: (p[1], p[0], p[2]))))
        for i in (0, n // 2, n):
            y, x = points[i]
            bolt = hexbolt(y, (x + side * 0.5, z), (side, 0.0), 1.1, 1.0)
            out.append((BOLT, moved(bolt, bolt["tris"], lambda p: (p[1], p[0], p[2]))))
    return out


def rebar(meshes, a, b, which):
    """One of the Power Fist's bars, stretched to run from a to b."""
    shape = next(q for q in Nif(os.path.join(meshes, "weapons/powerfist/rebarfist.nif")).shapes()
                 if q["name"] == "RebarFist:0")
    bars = []
    for group in nifpreview["loose_parts"](shape):
        own = [shape["verts"][i] for t in group for i in t]
        span = [max(v[k] for v in own) - min(v[k] for v in own) for k in (0, 1)]
        if span[0] > 5 and span[1] <= 12:
            bars.append((group, own))
    group, own = bars[which]
    low, high = min(v[0] for v in own), max(v[0] for v in own)
    mid = [sum(v[k] for v in own) / len(own) for k in (1, 2)]
    f = unit(tuple(b[k] - a[k] for k in range(3)))
    side = unit(cross(f, (0.0, 1.0, 0.0)))
    other = cross(f, side)

    def fn(p):
        t = (p[0] - low) / (high - low)
        return tuple(a[k] + (b[k] - a[k]) * t + side[k] * (p[1] - mid[0]) + other[k] * (p[2] - mid[1])
                     for k in range(3))
    return [(BAR, moved(shape, group, fn))]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("meshes")
    ap.add_argument("outdir")
    ap.add_argument("--full", action="store_true")
    args = ap.parse_args()
    meshes = args.meshes
    if os.path.isdir(os.path.join(meshes, "meshes")):
        meshes = os.path.join(meshes, "meshes")
    pa = os.path.join(meshes, "actors/powerarmor/characterassets")
    bones = place["skeleton"](os.path.join(pa, "skeleton.nif"))

    body = []
    for model in ("frame.nif", "mods/pa_raider_body.nif"):
        for q in place["posed"](os.path.join(pa, model), bones):
            for t in q["tris"]:
                if any(place["dominant"](q, i).startswith(("LArm", "RArm", "L_", "R_")) for i in t):
                    continue
                a, b, c = (q["verts"][i] for i in t)
                body += [tuple(a[n] + (b[n] - a[n]) * j / 3 + (c[n] - a[n]) * k / 3 for n in range(3))
                         for j in range(4) for k in range(4 - j)]
    rack = []
    for kind, breech, direction, roll, size, length in GUNS:
        placed = gun(gun_parts(meshes, kind, length), breech, direction, roll, size)
        rack += placed + clamp(breech, direction, size, placed)
    for spec in STRAPS:
        rack += side_strap(body, *spec)
    # Short bars from the suit's sides out to the guns' clamps.
    for n, (_, breech, direction, _, size, _) in enumerate(GUNS):
        f, side = unit(direction), 1.0 if breech[0] > 0 else -1.0
        held = tuple(breech[k] + f[k] * CLAMP * size for k in range(3))
        for lift in (-2.5, 2.5):
            rack += rebar(meshes, (side * 7.0, held[1] - 7.0, held[2] + lift),
                          (held[0] - side * 3.5, held[1], held[2] + lift), n % 3)

    os.makedirs(args.outdir, exist_ok=True)
    sets = [("rack_front.png", ("body", "helmet", "larm", "rarm"))]
    if args.full:
        sets.append(("rack_suit.png", ("body", "helmet", "larm", "rarm", "lleg", "rleg")))
    for name, models in sets:
        suit = []
        for model in ("frame.nif",) + tuple("mods/pa_raider_%s.nif" % n for n in models):
            for q in place["posed"](os.path.join(pa, model), bones):
                tris = q["tris"]
                if name == "rack_front.png":
                    tris = [t for t in tris if min(q["verts"][i][2] for i in t) > 88.0]
                if tris:
                    suit.append((SUIT, (q, tris)))
        render(suit + [(c, (q, q["tris"])) for c, q in rack], 600, os.path.join(args.outdir, name))
        print(name, "drawn", flush=True)


if __name__ == "__main__":
    main()

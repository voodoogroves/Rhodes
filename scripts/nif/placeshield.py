#!/usr/bin/env python3
"""Preview the super mutant right-arm plate on the power armor left forearm. Standard library only.

  python3 -I placeshield.py MESHES OUTDIR [--scale 1.0] [--slide 0] [--out 0|auto] [--tilt 0] [--roll 0] [--bend 0]

MESHES is a folder holding these, extracted from "Fallout4 - Meshes.ba2" with baunpack:
  actors/supermutant/characterassets/{skeleton.nif, smarmor0_arms.nif}
  actors/powerarmor/characterassets/{skeleton.nif, frame.nif, mods/pa_t60_larm.nif}

Both models are posed on their own skeletons. The plate is mirrored to the left and
carried from the super mutant's left forearm bone to the power armor's, keeping its
offset from the middle of the forearm. --slide moves it toward the hand; --out moves it
away from the arm ("auto": just far enough that the arm's lower shell stays under the
plate's outer face, plus 0.3; the arm may sit inside the plate's thickness, unseen).
--tilt leans the plate along the forearm about its own middle (negative brings the elbow
end in); --roll swings it around the arm. --bend flexes the power armor elbow, bringing the
hand forward; plate triangles that then cut into the upper arm, shoulder pad or body are
counted and drawn yellow. Degrees; distances are model units. Writes arm.png (close up) and suit.png.
A preview only: nothing is written as a game model.
"""
import argparse
import math
import os
import runpy

nifpreview = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "nifpreview.py"))
Nif, NODES = nifpreview["Nif"], nifpreview["NODES"]

PLATE = (1, 5, 6)                     # part numbers from `nifpreview.py info --seams`
BONE, HAND = "LArm_ForeArm1", "LArm_Hand"


# A transform is (rotation as 9 numbers by row, translation, scale).
def apply(t, p):
    r, move, s = t
    return tuple(s * sum(r[3 * a + b] * p[b] for b in range(3)) + move[a] for a in range(3))


def unapply(t, p):
    r, move, s = t
    return tuple(sum(r[3 * b + a] * (p[b] - move[b]) for b in range(3)) / s for a in range(3))


def skeleton(path):
    """Bone name -> function from bone coordinates to model coordinates."""
    nif = Nif(path)
    parents = nif.parents()
    bones = {}
    for i, (kind, _, _) in enumerate(nif.blocks):
        if kind not in NODES:
            continue
        chain, node = [], i
        while True:
            name, (move, r, s), _ = nif.av_object(node)
            chain.append((r, move, s))
            if node not in parents:
                break
            node = parents[node]
        bones[nif.av_object(i)[0]] = chain
    return bones


def to_model(chain, p):
    for t in chain:
        p = apply(t, p)
    return p


def to_bone(chain, p):
    for t in reversed(chain):
        p = unapply(t, p)
    return p


def skin_to_bone(nif):
    """For each skinned shape, in file order: the transforms from stored vertices to each bone."""
    out = []
    for kind, offset, _ in nif.blocks:
        if kind != "BSSkin::Instance":
            continue
        nif.p = offset + 4
        data = nif._u("i")
        nif.p = nif.blocks[data][1]
        transforms = []
        for _ in range(nif._u("I")):
            nif._u("4f")                                  # bounding sphere
            r = nif._u("9f")
            move = nif._u("3f")
            transforms.append((r, move, nif._u("f")))
        out.append(transforms)
    return out


def posed(path, bones):
    """The model's shapes with skinned vertices moved onto the skeleton."""
    nif = Nif(path)
    skins = iter(skin_to_bone(nif))
    shapes = []
    for shape in nif.shapes():
        if shape["weights"]:
            transforms = next(skins)
            missing = {n for n in shape["bones"] if n not in bones}
            if missing:
                raise SystemExit("%s: bones not in skeleton: %s" % (path, ", ".join(sorted(missing))))
            verts = []
            for v, weights in zip(shape["verts"], shape["weights"]):
                total = sum(w for _, w in weights)
                points = [(to_model(bones[shape["bones"][b]], apply(transforms[b], v)), w)
                          for b, w in weights]
                verts.append(tuple(sum(p[a] * w for p, w in points) / total for a in range(3)))
            shape = dict(shape, verts=verts)
        shapes.append(shape)
    return shapes


def poke(samples, shield_tris):
    """Compare arm points with the plate, both as (height, u, v) with height pointing away from
    the bone. Returns how many points under or over the plate stick out past its outer face,
    how many are covered at all, the furthest any sticks out, and how many pass the inner side
    only (inside the plate's thickness, not showing in front)."""
    out, covered, worst, back = 0, 0, 0.0, 0
    for h, u, v in samples:
        heights = []
        for (h0, u0, v0), (h1, u1, v1), (h2, u2, v2) in shield_tris:
            area = (u1 - u0) * (v2 - v0) - (u2 - u0) * (v1 - v0)
            if abs(area) < 1e-9:
                continue
            b1 = ((u - u0) * (v2 - v0) - (u2 - u0) * (v - v0)) / area
            b2 = ((u1 - u0) * (v - v0) - (u - u0) * (v1 - v0)) / area
            if b1 >= 0 and b2 >= 0 and b1 + b2 <= 1:
                heights.append(h0 + b1 * (h1 - h0) + b2 * (h2 - h0))
        if heights:
            covered += 1
            depth = h - max(heights)
            if depth > 0:
                out += 1
                worst = max(worst, depth)
            elif h > min(heights):
                back += 1
    return out, covered, worst, back


def bend(bones, degrees):
    """Flex the left elbow about the forearm bone's Z axis, moving the hand forward (+Y)."""
    elbow = to_model(bones[BONE], (0, 0, 0))
    axis = [a - b for a, b in zip(to_model(bones[BONE], (0, 0, 1)), elbow)]
    along = [a - b for a, b in zip(to_model(bones[BONE], (1, 0, 0)), elbow)]
    if axis[2] * along[0] - axis[0] * along[2] < 0:       # Y part of axis x forearm
        axis = [-a for a in axis]
    n = math.sqrt(sum(a * a for a in axis))
    x, y, z = (a / n for a in axis)
    c, s = math.cos(math.radians(degrees)), math.sin(math.radians(degrees))
    k = 1 - c
    r = (c + x * x * k, x * y * k - z * s, x * z * k + y * s,
         y * x * k + z * s, c + y * y * k, y * z * k - x * s,
         z * x * k - y * s, z * y * k + x * s, c + z * z * k)
    turn = (r, tuple(elbow[a] - sum(r[3 * a + b] * elbow[b] for b in range(3)) for a in range(3)), 1.0)
    for name in bones:
        if name.startswith(("LArm_ForeArm", "LArm_Hand", "LArm_Finger")):
            bones[name] = bones[name] + [turn]


def crosses(a, b):
    """True if an edge of either triangle passes through the other."""
    def sub(p, q):
        return (p[0] - q[0], p[1] - q[1], p[2] - q[2])

    def cross(p, q):
        return (p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0])

    def dot(p, q):
        return p[0] * q[0] + p[1] * q[1] + p[2] * q[2]

    for edges, tri in ((a, b), (b, a)):
        e1, e2 = sub(tri[1], tri[0]), sub(tri[2], tri[0])
        for i in range(3):
            start, d = edges[i], sub(edges[(i + 1) % 3], edges[i])
            h = cross(d, e2)
            det = dot(e1, h)
            if abs(det) < 1e-9:
                continue
            s = sub(start, tri[0])
            u = dot(s, h) / det
            q = cross(s, e1)
            v = dot(d, q) / det
            if u >= 0 and v >= 0 and u + v <= 1 and 0 <= dot(e2, q) / det <= 1:
                return True
    return False


def boxed(verts, tris):
    out = []
    for t in tris:
        pts = [verts[i] for i in t]
        out.append((t, pts, [min(c) for c in zip(*pts)], [max(c) for c in zip(*pts)]))
    return out


def dominant(shape, i):
    return shape["bones"][max(shape["weights"][i], key=lambda w: w[1])[0]] if shape["weights"] else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("meshes")
    ap.add_argument("outdir")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--slide", type=float, default=0.0)
    ap.add_argument("--out", default="0")
    ap.add_argument("--tilt", type=float, default=0.0)
    ap.add_argument("--roll", type=float, default=0.0)
    ap.add_argument("--bend", type=float, default=0.0)
    ap.add_argument("--no-render", action="store_true")
    args = ap.parse_args()
    sm = os.path.join(args.meshes, "actors/supermutant/characterassets")
    pa = os.path.join(args.meshes, "actors/powerarmor/characterassets")
    sm_bones = skeleton(os.path.join(sm, "skeleton.nif"))
    pa_bones = skeleton(os.path.join(pa, "skeleton.nif"))

    bend(pa_bones, args.bend)

    arms = Nif(os.path.join(sm, "smarmor0_arms.nif"))
    split = nifpreview["all_parts"](arms, True)
    on_skeleton = {s["name"]: s for s in posed(os.path.join(sm, "smarmor0_arms.nif"), sm_bones)}
    drift = max(math.dist(a, b) for s in arms.shapes() for a, b in zip(s["verts"], on_skeleton[s["name"]]["verts"]))
    shield = on_skeleton[split[0][0]["name"]]
    triangles = [t for n in PLATE for t in split[n - 1][1]]

    lengths = [math.dist(to_model(b[BONE], (0, 0, 0)), to_model(b[HAND], (0, 0, 0)))
               for b in (sm_bones, pa_bones)]
    local = {}
    for i in {i for t in triangles for i in t}:
        x, y, z = shield["verts"][i]
        local[i] = to_bone(sm_bones[BONE], (-x, y, z))     # mirror right to left
    centre = [(min(p[a] for p in local.values()) + max(p[a] for p in local.values())) / 2 for a in range(3)]
    for i, p in local.items():
        p = [centre[a] + args.scale * (p[a] - centre[a]) for a in range(3)]
        p[0] += (lengths[1] - lengths[0]) / 2 + args.slide  # X runs along the forearm
        local[i] = p

    arm = [(2, (s, s["tris"])) for s in posed(os.path.join(pa, "mods/pa_t60_larm.nif"), pa_bones)]
    # "Outward" is from the forearm bone's axis to the middle of the plate.
    middle = [sum(p[a] for p in local.values()) / len(local) for a in (1, 2)]
    ny, nz = (c / math.hypot(*middle) for c in middle)

    def flat(p):
        return (p[1] * ny + p[2] * nz, p[0], p[2] * ny - p[1] * nz)

    # Points spread over the arm's forearm shell, outer side only.
    samples, upper, steps = [], [], 4                      # upper: shoulder pad and upper arm
    for _, (s, tris) in arm:
        for t in tris:
            into = samples if all(dominant(s, i).startswith("LArm_ForeArm") for i in t) else upper
            a, b, c = (flat(to_bone(pa_bones[BONE], s["verts"][i])) for i in t)
            for j in range(steps + 1):
                for k in range(steps + 1 - j):
                    q = tuple(a[n] + (b[n] - a[n]) * j / steps + (c[n] - a[n]) * k / steps for n in range(3))
                    if q[0] > 0:
                        into.append(q)

    placed = {i: flat(p) for i, p in local.items()}
    mid_h, mid_u = (sum(p[a] for p in placed.values()) / len(placed) for a in (0, 1))
    ct, st = math.cos(math.radians(args.tilt)), math.sin(math.radians(args.tilt))
    cr, sr = math.cos(math.radians(args.roll)), math.sin(math.radians(args.roll))
    for i, (h, u, v) in placed.items():
        dh, du = h - mid_h, u - mid_u
        h, u = mid_h + dh * ct + du * st, mid_u - dh * st + du * ct
        placed[i] = (h * cr - v * sr, u, h * sr + v * cr)

    def plate_at(push):
        return [tuple((h + push, u, v) for h, u, v in (placed[i] for i in t)) for t in triangles]

    if args.out == "auto":
        push = poke(samples, plate_at(0))[2] + 0.3
    else:
        push = float(args.out)
    out, covered, worst, back = poke(samples, plate_at(push))
    verts = list(shield["verts"])
    for i, (h, u, v) in placed.items():
        h += push
        verts[i] = to_model(pa_bones[BONE], (u, h * ny - v * nz, h * nz + v * ny))
    shield = dict(shield, verts=verts)
    along = [p[1] for p in placed.values()]
    print("slide %g, tilt %g, roll %g, out %.1f: plate runs %.1f..%.1f along the forearm (elbow 0, hand %.1f)"
          % (args.slide, args.tilt, args.roll, push, min(along), max(along), lengths[1]))
    for name, o, c, w, b in (("forearm shell", out, covered, worst, back),
                             ("shoulder pad / upper arm", *poke(upper, plate_at(push)))):
        print("%s: of %d points under the plate, %d through the front (worst %.1f), %d into the back only"
              % (name, c, o, w, b))
    frame, frame_arm = [], []
    for s in posed(os.path.join(pa, "frame.nif"), pa_bones):
        frame.append((10, (s, s["tris"])))
        lower = [t for t in s["tris"] if all(
            dominant(s, i).startswith(("LArm_", "L_")) and not dominant(s, i).startswith("LArm_Collar")
            for i in t)]
        if lower:
            frame_arm.append((10, (s, lower)))

    # Plate triangles cutting into anything that does not move with the forearm.
    fixed = {}
    for group, parts in (("arm piece", arm), ("frame", frame)):
        for _, (s, tris) in parts:
            for t in tris:
                if not any(dominant(s, i).startswith(("LArm_ForeArm", "LArm_Hand", "LArm_Finger")) for i in t):
                    fixed.setdefault(group, []).extend(boxed(s["verts"], [t]))
    hit = set()
    counts = {}
    for group, others in fixed.items():
        for t, pts, low, high in boxed(shield["verts"], triangles):
            if any(all(low[a] <= h[a] and high[a] >= l[a] for a in range(3)) and crosses(pts, q)
                   for _, q, l, h in others):
                hit.add(t)
                counts[group] = counts.get(group, 0) + 1
    print("bend %g: plate triangles cutting in, of %d: shoulder pad / upper arm %d, frame %d"
          % (args.bend, len(triangles), counts.get("arm piece", 0), counts.get("frame", 0)))

    if args.no_render:
        return
    os.makedirs(args.outdir, exist_ok=True)
    plate = [(1, (shield, [t for t in triangles if t not in hit]))]
    if hit:
        plate.append((7, (shield, sorted(hit))))
    nifpreview["render"](frame_arm + arm + plate, 600, os.path.join(args.outdir, "arm.png"))
    nifpreview["render"](frame + arm + plate, 600, os.path.join(args.outdir, "suit.png"))
    print("super mutant skinning check: largest vertex drift %.3f" % drift)
    print("forearm bone length: super mutant %.1f, power armor %.1f; scale %g" % (*lengths, args.scale))
    for name, group in (("shield", plate), ("T-60 arm", arm)):
        pts = [s["verts"][i] for _, (s, tris) in group for t in tris for i in t]
        print(name, "  ".join("%s %.1f..%.1f" % (n, min(p[a] for p in pts), max(p[a] for p in pts))
                              for a, n in enumerate("XYZ")))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Write a claw layout from placeclaw.py as a worn power armor model. Standard library only.

  python3 -I writeclaw.py MESHES OUT.nif [--claw ritual|assaultron|assaultron_shock|officer] [--pitch 9] [--roll N]

MESHES is the folder placeclaw.py needs. The model has two skinned shapes, both weighted
wholly to the right forearm bone and stored in its coordinates: one shape for each source
weapon shape used (blades, coils, battery), each with that shape's own texture, and one for
the generated housing and cables, with the T-60 right arm's metal. The shishkebab claw is not
handled yet. The output is derived from game files: keep it out of every repo.
"""
import argparse
import math
import os
import runpy
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
claws = runpy.run_path(os.path.join(HERE, "placeclaw.py"))
shield = runpy.run_path(os.path.join(HERE, "writeshield.py"))
nifpreview = runpy.run_path(os.path.join(HERE, "nifpreview.py"))
Nif, NODES = nifpreview["Nif"], nifpreview["NODES"]
header_parts, ints = shield["header_parts"], shield["ints"]
NODE_HEAD, BONE = 72, "RArm_ForeArm1"
SKINNED_LAYOUT, STATIC_LAYOUT = 0x0005B00050430208, 0x0001B00000430205
SKINNED_FLAG = 0x2                      # in the lighting shader's first flag word
ROOT_MATERIAL = 60                      # offset of the shader's second string reference
HOUSING_TEXELS = 0.004                  # texture distance per model unit on the housing


def sub(a, b):
    return tuple(a[k] - b[k] for k in range(3))


def dot(a, b):
    return sum(a[k] * b[k] for k in range(3))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def unit(a):
    n = math.sqrt(dot(a, a))
    return tuple(c / n for c in a) if n > 1e-9 else (1.0, 0.0, 0.0)


def block_of(nif, i):
    _, offset, size = nif.blocks[i]
    return bytearray(nif.d[offset:offset + size])


def shape_data(nif, name):
    """A named shape's block index, layout, vertex bytes and shader block index."""
    for i, (kind, _, _) in enumerate(nif.blocks):
        if kind.endswith("TriShape") and nif.av_object(i)[0] == name:
            _, local, p = nif.av_object(i)
            skin, shader = struct.unpack_from("<2i", nif.d, p + 16)
            desc = struct.unpack_from("<Q", nif.d, p + 28)[0]
            count = struct.unpack_from("<H", nif.d, p + 40)[0]
            stride = (desc & 0xF) * 4
            return {"local": local, "desc": desc, "shader": shader,
                    "vertices": [nif.d[p + 46 + v * stride:p + 46 + (v + 1) * stride] for v in range(count)]}
    raise SystemExit("no shape named " + name)


def carried(part, data, bend):
    """Source blade vertices through the placement: (position, uv bytes, normal, tangent,
    bitangent). Directions follow the placement's local slope."""
    rotation = data["local"][1]
    if rotation != (1, 0, 0, 0, 1, 0, 0, 0, 1):
        raise SystemExit("the source shape is rotated; not handled")
    place = lambda p: bend(part["fn"](p))
    out = []
    for new, old in enumerate(part["used"]):
        raw = data["vertices"][old]
        at = part["source"]["verts"][old]
        step = 0.01
        columns = [tuple(c / (2 * step) for c in sub(
            place(tuple(at[k] + (step if k == a else 0) for k in range(3))),
            place(tuple(at[k] - (step if k == a else 0) for k in range(3))))) for a in range(3)]
        along = lambda v: tuple(sum(columns[a][k] * v[a] for a in range(3)) for k in range(3))
        # Normals turn with the cofactors of the slope, so they stay square to the surface.
        across = [cross(columns[1], columns[2]), cross(columns[2], columns[0]), cross(columns[0], columns[1])]
        side = 1 if dot(columns[0], across[0]) > 0 else -1
        turn = lambda v: tuple(side * sum(across[a][k] * v[a] for a in range(3)) for k in range(3))
        value = lambda b: tuple(x / 127.5 - 1 for x in b)
        bitangent = (struct.unpack_from("<e", raw, 6)[0], raw[15] / 127.5 - 1, raw[19] / 127.5 - 1)
        out.append((place(at), raw[8:12], unit(turn(value(raw[12:15]))),
                    unit(along(value(raw[16:19]))), unit(along(bitangent))))
    return out


def flat_faced(part, bend, anchor):
    """The generated housing: one flat face per triangle, facing away from the solid's middle,
    textured by a flat projection around one spot on the suit's arm."""
    points = [bend(p) for p in part["verts"]] if bend else part["verts"]
    middle = tuple(sum(p[k] for p in points) / len(points) for k in range(3))
    vertices, tris = [], []
    for t in part["tris"]:
        a, b, c = (points[i] for i in t)
        normal = cross(sub(b, a), sub(c, a))
        if dot(normal, normal) < 1e-8:
            continue
        centre = tuple((a[k] + b[k] + c[k]) / 3 for k in range(3))
        if dot(normal, sub(centre, middle)) < 0:
            b, c = c, b
            normal = tuple(-x for x in normal)
        normal = unit(normal)
        axis = max(range(3), key=lambda k: abs(normal[k]))
        i, j = [k for k in range(3) if k != axis]
        tangent = unit(tuple((1.0 if k == i else 0.0) - normal[k] * normal[i] for k in range(3)))
        bitangent = cross(normal, tangent)
        if bitangent[j] < 0:
            bitangent = tuple(-x for x in bitangent)
        for p in (a, b, c):
            uv = struct.pack("<2e", anchor[0] + HOUSING_TEXELS * (p[i] - 14), anchor[1] + HOUSING_TEXELS * p[j])
            vertices.append((p, uv, normal, tangent, bitangent))
        tris.append(tuple(range(len(vertices) - 3, len(vertices))))
    return vertices, tris


def joined(groups):
    vertices, tris = [], []
    for v, t in groups:
        base = len(vertices)
        vertices += v
        tris += [tuple(base + i for i in tri) for tri in t]
    return vertices, tris


def sphere(points):
    centre = [(min(p[k] for p in points) + max(p[k] for p in points)) / 2 for k in range(3)]
    return (*centre, max(math.dist(p, centre) for p in points))


def shape_block(name, flags, vertices, tris, skin, shader, count=3):
    def packed(v):
        return bytes(max(0, min(255, round((x + 1) * 127.5))) for x in v)

    body = bytearray()
    for point, uv, normal, tangent, bit in vertices:
        body += (struct.pack("<4e", *point, bit[0]) + uv
                 + packed(normal) + packed(bit[1:2]) + packed(tangent) + packed(bit[2:3])
                 + struct.pack("<4e4B", 1, 0, 0, 0, 0, 0, 0, 0))
    faces = b"".join(struct.pack("<3H", *t) for t in tris)
    n = len(tris)
    segments = struct.pack("<3I", n, count, count)        # all in the last: 3 as the T-60 right arm
    for s in range(count):
        segments += struct.pack("<IIiI", 0, n if s == count - 1 else 0, -1, 0)
    head = struct.pack("<iIiI13fi", name, 0, -1, flags, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, -1)
    return (head + struct.pack("<4f3iQIHI", *sphere([v[0] for v in vertices]), skin, shader, -1,
                               SKINNED_LAYOUT, n, len(vertices), len(body) + len(faces))
            + body + faces + segments)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("meshes")
    ap.add_argument("out")
    ap.add_argument("--claw", default="ritual", choices=("ritual", "assaultron", "assaultron_shock", "officer"))
    ap.add_argument("--pitch", type=float, default=9.0)
    ap.add_argument("--roll", type=float, help="as in placeclaw.py")
    ap.add_argument("--back", type=float, help="override how far the blades sit back in the chassis")
    ap.add_argument("--only", choices=("source", "metal"),
                    help="for fault finding: write only the shapes cut from the weapon, or only the generated metal")
    ap.add_argument("--paint", choices=("source", "metal"), default="source",
                    help="for fault finding: metal gives the weapon shapes the housing's material")
    ap.add_argument("--like-shield", action="store_true",
                    help="for fault finding: five segments, and the root settings and file header of "
                         "the super mutant arm the shield is cut from")
    args = ap.parse_args()

    _, _, local, surface = claws["suit_arm"](args.meshes)
    if args.back is not None:
        claws["CLAWS"][args.claw]["back"] = args.back
    parts, _ = claws["build"](args.claw, args.meshes, surface, args.roll)
    bend = claws["pitched"](args.pitch)
    path, name, _ = claws["CLAWS"][args.claw]["source"]
    source = Nif(os.path.join(args.meshes, path))
    donor = Nif(os.path.join(args.meshes, "actors/powerarmor/characterassets/mods/pa_t60_rarm.nif"))
    donor_name = next(donor.av_object(i)[0] for i, b in enumerate(donor.blocks) if b[0].endswith("TriShape"))
    donor_data = shape_data(donor, donor_name)
    if donor_data["desc"] != SKINNED_LAYOUT:
        raise SystemExit("unexpected arm vertex layout %x" % donor_data["desc"])

    # Texture spot for the housing: the arm vertex nearest the top middle of the forearm.
    arm = next(s for s in local if len(s["source"]["verts"]) == len(donor_data["vertices"]))
    best = min(range(len(arm["verts"])), key=lambda i: math.dist(arm["verts"][i], (14.0, 0.0, 11.0)))
    anchor = struct.unpack_from("<2e", donor_data["vertices"][arm["used"][best]], 8)

    # One group of parts for each source shape, then the generated metal.
    moved_parts = {}
    for _, p in parts:
        if "source" in p:
            moved_parts.setdefault(p["source"]["name"], []).append(p)
    shapes_out = []
    for shape_name, group in moved_parts.items():
        data = shape_data(source, shape_name)
        if data["desc"] != STATIC_LAYOUT:
            raise SystemExit("%s: unexpected vertex layout %x" % (shape_name, data["desc"]))
        vertices, tris = joined([(carried(p, data, bend), p["tris"]) for p in group])
        agree = sum(dot(cross(sub(vertices[t[1]][0], vertices[t[0]][0]), sub(vertices[t[2]][0], vertices[t[0]][0])),
                        tuple(sum(vertices[i][2][k] for i in t) for k in range(3))) > 0 for t in tris)
        print("%s: triangles facing with their normals: %d of %d" % (shape_name, agree, len(tris)))
        if agree < 0.9 * len(tris):
            raise SystemExit("%s: winding disagrees with the normals" % shape_name)
        paint = (donor, donor_data) if args.paint == "metal" else (source, data)
        shapes_out.append(("PAXClaw%d" % len(shapes_out), (vertices, tris), *paint))
    metal = joined([flat_faced(p, bend if n else None, anchor)
                    for n, (_, p) in enumerate(parts) if "source" not in p])
    shapes_out.append(("PAXClawMetal", metal, donor, donor_data))
    if args.only:
        shapes_out = [s for s in shapes_out if (s[0] == "PAXClawMetal") == (args.only == "metal")]

    node = next(i for i, b in enumerate(donor.blocks) if b[0] in NODES and donor.av_object(i)[0] == BONE)
    end = donor.av_object(node)[2]
    bone_transform = donor.d[end - 56:end - 4]
    flags = struct.unpack_from("<I", block_of(donor, node), 12)[0]
    shape_flags = struct.unpack_from("<I", block_of(donor, next(
        i for i, b in enumerate(donor.blocks) if b[0].endswith("TriShape"))), 12)[0]

    root_flags, header_from, segment_count = flags, donor, 3
    if args.like_shield:
        header_from = Nif(os.path.join(args.meshes, "actors/supermutant/characterassets/smarmor0_arms.nif"))
        root_flags, segment_count = struct.unpack_from("<I", block_of(header_from, 0), 12)[0], 5
        print("shield packaging: root flags %x, %d segments" % (root_flags, segment_count))

    strings = ["PAXClaw.nif", BONE]

    def string(s):
        if s not in strings:
            strings.append(s)
        return strings.index(s)

    def node_block(label, transform, children, flags=flags):
        return (struct.pack("<iIiI", string(label), 0, -1, flags) + transform + struct.pack("<i", -1)
                + struct.pack("<I", len(children)) + ints(*children))

    identity = struct.pack("<13f", 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1)
    # Blocks: root, bone, then per shape: shape, skin, bone data, shader, textures.
    firsts = [2 + 5 * n for n in range(len(shapes_out))]
    expected = []                          # each shader's (material, root material)
    names = ["NiNode", "NiNode"]
    blocks = [node_block("PAXClaw.nif", identity, (1, *firsts), root_flags), node_block(BONE, bone_transform, ())]
    for first, (label, (vertices, tris), nif, data) in zip(firsts, shapes_out):
        shader = block_of(nif, data["shader"])
        textures = struct.unpack_from("<i", shader, 40)[0]
        if nif.blocks[textures][0] != "BSShaderTextureSet":
            raise SystemExit("texture set reference not where expected")
        material = nif.string(struct.unpack_from("<i", shader, 4)[0])
        template = struct.unpack_from("<i", shader, ROOT_MATERIAL)[0]
        template = nif.string(template) if template >= 0 else None
        struct.pack_into("<i", shader, 4, string(material))
        # Every string reference must point into the new table: the game crashes otherwise.
        struct.pack_into("<i", shader, ROOT_MATERIAL, -1 if template is None else string(template))
        expected.append((material, template))
        struct.pack_into("<I", shader, 16, struct.unpack_from("<I", shader, 16)[0] | SKINNED_FLAG)
        struct.pack_into("<i", shader, 40, first + 4)
        centre = sphere([v[0] for v in vertices])
        blocks += [shape_block(string(label), shape_flags, vertices, tris, first + 1, first + 3,
                               segment_count),
                   ints(0, first + 2) + struct.pack("<I", 1) + ints(1) + struct.pack("<I", 0),
                   struct.pack("<I17f", 1, *centre, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1),
                   shader, block_of(nif, textures)]
        names += ["BSSubIndexTriShape", "BSSkin::Instance", "BSSkin::BoneData",
                  "BSLightingShaderProperty", "BSShaderTextureSet"]
        print("%s: %d vertices, %d triangles, %s" % (label, len(vertices), len(tris), material or "(textures in the model)"))

    (before, after), _ = header_parts(header_from.d)
    types = list(dict.fromkeys(names))
    out = bytearray(before + struct.pack("<I", len(blocks)) + after)
    out += struct.pack("<H", len(types))
    for t in types:
        out += struct.pack("<I", len(t)) + t.encode()
    out += struct.pack("<%dH" % len(names), *(types.index(t) for t in names))
    out += struct.pack("<%dI" % len(blocks), *(len(b) for b in blocks))
    out += struct.pack("<II", len(strings), max(len(s) for s in strings))
    for s in strings:
        out += struct.pack("<I", len(s)) + s.encode("latin1")
    out += struct.pack("<I", 0)                           # no groups
    for b in blocks:
        out += b
    out += ints(1, 0)                                     # footer: one root, block 0
    with open(args.out, "xb") as f:
        f.write(out)
    check = Nif(args.out)
    shapes = list(check.shapes())
    if [len(s["tris"]) for s in shapes] != [len(g[1]) for _, g, _, _ in shapes_out] or any(
            s["bones"] != [BONE] for s in shapes):
        raise SystemExit("FAIL: the written model does not read back as expected")
    found = []
    for i, (kind, offset, _) in enumerate(check.blocks):
        if kind == "BSLightingShaderProperty":
            refs = [struct.unpack_from("<i", check.d, offset + at)[0] for at in (4, ROOT_MATERIAL)]
            if any(not -1 <= r < len(check.strings) for r in refs):
                raise SystemExit("FAIL: shader %d has a string reference outside the table: %s" % (i, refs))
            found.append(tuple(check.strings[r] if r >= 0 else None for r in refs))
    if found != expected:
        raise SystemExit("FAIL: shader material names read back wrong: %s" % found)
    points = [v for s in shapes for v in s["verts"]]
    print("wrote %s; reads back; bounds %s to %s" % (args.out, [round(min(p[k] for p in points), 1) for k in range(3)],
                                                      [round(max(p[k] for p in points), 1) for k in range(3)]))


if __name__ == "__main__":
    main()

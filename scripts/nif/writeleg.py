#!/usr/bin/env python3
"""Write the Scrappy left leg: the base game's Raider left leg with junk merged in. Standard library.

  python3 -I writeleg.py MESHES OUT.nif

MESHES holds what placeharness.py asks for, extracted from "Fallout4 - Meshes.ba2". Step 1: the
street sign on the thigh. The vanilla leg's blocks are kept byte for byte and new blocks are added
after them: for each piece of junk a skinned shape wholly weighted to one leg bone (stored in that
bone's coordinates, identity skin transform), its skin, bone data, shader, textures and, where the
source has one, alpha settings. Step 2 adds the teddy bear on the calf. The output is derived from game files: keep it out of every repo.
"""
import argparse
import math
import os
import runpy
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
claw = runpy.run_path(os.path.join(HERE, "writeclaw.py"))
harness = runpy.run_path(os.path.join(HERE, "placeharness.py"))
shield = runpy.run_path(os.path.join(HERE, "writeshield.py"))
Nif, NODES, ints = claw["Nif"], claw["NODES"], claw["ints"]
carried, shape_data, sphere, block_of = (claw[n] for n in ("carried", "shape_data", "sphere", "block_of"))
header_parts, place = shield["header_parts"], harness["place"]
SKINNED, STATIC, SKINNED_FLAG, ROOT_MATERIAL, NODE_HEAD = (
    claw["SKINNED_LAYOUT"], claw["STATIC_LAYOUT"], claw["SKINNED_FLAG"], claw["ROOT_MATERIAL"], claw["NODE_HEAD"])
LEG = "actors/powerarmor/characterassets/mods/pa_raider_lleg.nif"
SPLITS = {"STREET": 3}                 # times each triangle is cut in four, so a flat board can bend
# The junk: the harness piece's colour name, and the leg bone it rides on.
JUNK = (("STREET", "LLeg_Thigh"), ("BEAR", "LLeg_Calf"))


def split(positions, raw, tris, times):
    """Cut every triangle in four, blending texture coordinates and directions at the new points."""
    positions, raw, tris = list(positions), list(raw), list(tris)
    for _ in range(times):
        mids, cut = {}, []

        def mid(a, b):
            key = (min(a, b), max(a, b))
            if key not in mids:
                mids[key] = len(positions)
                positions.append(tuple((positions[a][k] + positions[b][k]) / 2 for k in range(3)))
                va, vb = raw[a], raw[b]
                half = lambda at: struct.pack("<e", (struct.unpack_from("<e", va, at)[0]
                                                     + struct.unpack_from("<e", vb, at)[0]) / 2)
                bytes_ = lambda i, n: bytes((va[k] + vb[k] + 1) // 2 for k in range(i, i + n))
                # position (unused here), bitangent x, u, v, normal + bitangent y, tangent + bitangent z
                raw.append(va[:6] + half(6) + half(8) + half(10) + bytes_(12, 4) + bytes_(16, 4))
            return mids[key]
        for a, b, c in tris:
            ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
            cut += [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]
        tris = cut
    return positions, raw, tris


def shape_block(name, flags, vertices, tris, skin, shader, alpha):
    """A skinned BSTriShape, the kind the vanilla leg uses."""
    def packed(v):
        return bytes(max(0, min(255, round((x + 1) * 127.5))) for x in v)
    body = bytearray()
    for point, uv, normal, tangent, bit in vertices:
        body += (struct.pack("<4e", *point, bit[0]) + uv
                 + packed(normal) + packed(bit[1:2]) + packed(tangent) + packed(bit[2:3])
                 + struct.pack("<4e4B", 1, 0, 0, 0, 0, 0, 0, 0))
    faces = b"".join(struct.pack("<3H", *t) for t in tris)
    head = struct.pack("<iIiI13fi", name, 0, -1, flags, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, -1)
    return (head + struct.pack("<4f3iQIHI", *sphere([v[0] for v in vertices]), skin, shader, alpha,
                               SKINNED, len(tris), len(vertices), len(body) + len(faces))
            + body + faces)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("meshes")
    ap.add_argument("out")
    args = ap.parse_args()
    meshes = args.meshes
    if os.path.isdir(os.path.join(meshes, "meshes")):
        meshes = os.path.join(meshes, "meshes")
    pa = os.path.join(meshes, "actors/powerarmor/characterassets")
    bones = place["skeleton"](os.path.join(pa, "skeleton.nif"))
    # The same surface the mockup rests the junk on.
    surface = []
    for name in ("frame.nif",) + tuple("mods/pa_raider_%s.nif" % n for n in ("body", "helmet", "lleg", "rleg")):
        for q in place["posed"](os.path.join(pa, name), bones):
            for t in q["tris"]:
                if any(place["dominant"](q, i).startswith(("LArm", "RArm", "L_", "R_")) for i in t):
                    continue
                a, b, c = (q["verts"][i] for i in t)
                surface += [tuple(a[k] + (b[k] - a[k]) * i / 3 + (c[k] - a[k]) * j / 3 for k in range(3))
                            for i in range(4) for j in range(4 - i)]

    leg = Nif(os.path.join(meshes, LEG))
    blocks = [bytes(block_of(leg, i)) for i in range(len(leg.blocks))]
    names = [b[0] for b in leg.blocks]
    strings = list(leg.strings)
    kept = len(blocks)

    def string(s):
        if s not in strings:
            strings.append(s)
        return strings.index(s)
    vanilla_shape = next(i for i, n in enumerate(names) if n.endswith("TriShape"))
    shape_flags = struct.unpack_from("<I", blocks[vanilla_shape], 12)[0]
    added, expected = [], []

    for colour, bone in JUNK:
        piece = next(p for p in harness["PIECES"] if p[0] == harness[colour])
        mapping = []
        harness["fit"](piece, meshes, surface, mapping)
        source = Nif(os.path.join(meshes, piece[1] + ".nif"))
        node = next(i for i, n in enumerate(names) if n in NODES and leg.av_object(i)[0] == bone)
        # The same shapes and triangles the mockup keeps (for the street sign, one board).
        for kept_shape in harness["model"](meshes, piece[1]):
            data = shape_data(source, kept_shape["name"])
            if data["desc"] != STATIC:
                raise SystemExit("%s: unexpected vertex layout %x" % (kept_shape["name"], data["desc"]))
            used = sorted({i for t in kept_shape["tris"] for i in t})
            index = {old: n for n, old in enumerate(used)}
            # Positions with the source's node transforms applied, as the mockup placed them. Its
            # normals are used as stored, so the nodes may move and scale it but not turn it.
            node_at = next(i for i, b in enumerate(source.blocks)
                           if b[0].endswith("TriShape") and source.av_object(i)[0] == kept_shape["name"])
            parents = source.parents()
            while True:
                if any(abs(a - b) > 1e-4 for a, b in zip(source.av_object(node_at)[1][1], (1, 0, 0, 0, 1, 0, 0, 0, 1))):
                    raise SystemExit("%s: a source node is rotated; not handled" % kept_shape["name"])
                if node_at not in parents:
                    break
                node_at = parents[node_at]
            positions, raw, tris = split([kept_shape["verts"][i] for i in used], [data["vertices"][i] for i in used],
                                         [tuple(index[i] for i in t) for t in kept_shape["tris"]],
                                         SPLITS.get(colour, 0))
            data["local"] = (data["local"][0], (1, 0, 0, 0, 1, 0, 0, 0, 1))
            part = {"used": list(range(len(positions))), "source": {"verts": positions},
                    "fn": lambda v, f=mapping[0], b=bone: place["to_bone"](bones[b], f(v))}
            vertices = carried(part, {"local": data["local"], "vertices": raw}, lambda p: p)
            facing = sum(claw["dot"](claw["cross"](claw["sub"](vertices[b][0], vertices[a][0]),
                                                   claw["sub"](vertices[c][0], vertices[a][0])),
                                     tuple(sum(vertices[i][2][k] for i in (a, b, c)) for k in range(3))) > 0
                         for a, b, c in tris)
            print("%s: triangles facing with their normals: %d of %d" % (colour, facing, len(tris)))
            if facing < 0.9 * len(tris):
                raise SystemExit("winding disagrees with the normals")
            if len(vertices) > 65535:
                raise SystemExit("too many vertices")

            first = len(blocks)
            _, _, p = source.av_object(next(i for i, b in enumerate(source.blocks)
                                            if b[0].endswith("TriShape") and source.av_object(i)[0] == kept_shape["name"]))
            alpha_at = struct.unpack_from("<i", source.d, p + 24)[0]
            shader = block_of(source, data["shader"])
            textures = struct.unpack_from("<i", shader, 40)[0]
            if source.blocks[textures][0] != "BSShaderTextureSet" or struct.unpack_from("<Ii", shader, 8) != (0, -1):
                raise SystemExit("unexpected shader layout")
            # A shader starts with its type; the material name is at 4, the root material at 60.
            # Every string reference must point into the new table: the game crashes otherwise.
            refs = []
            for at in (4, ROOT_MATERIAL):
                old = struct.unpack_from("<i", shader, at)[0]
                text = source.string(old) if old >= 0 else None
                struct.pack_into("<i", shader, at, -1 if text is None else string(text))
                refs.append(text)
            expected.append(tuple(refs))
            struct.pack_into("<I", shader, 16, struct.unpack_from("<I", shader, 16)[0] | SKINNED_FLAG)
            struct.pack_into("<i", shader, 40, first + 4)
            centre = sphere([v[0] for v in vertices])
            new = [("BSTriShape", shape_block(string("PAXScrappy%d:0" % len(added)), shape_flags, vertices, tris,
                                              first + 1, first + 3, first + 5 if alpha_at >= 0 else -1)),
                   ("BSSkin::Instance", ints(0, first + 2) + struct.pack("<I", 1) + ints(node) + struct.pack("<I", 0)),
                   ("BSSkin::BoneData", struct.pack("<I17f", 1, *centre, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1)),
                   ("BSLightingShaderProperty", bytes(shader)),
                   ("BSShaderTextureSet", bytes(block_of(source, textures)))]
            if alpha_at >= 0:
                alpha = block_of(source, alpha_at)
                if source.blocks[alpha_at][0] != "NiAlphaProperty" or struct.unpack_from("<iIi", alpha) != (-1, 0, -1):
                    raise SystemExit("unexpected alpha settings")
                new.append(("NiAlphaProperty", bytes(alpha)))
            for kind, body in new:
                names.append(kind)
                blocks.append(body)
            added.append((first, bone, len(vertices), len(tris)))
            print("%s on %s: %d vertices, %d triangles, %s" % (colour, bone, len(vertices), len(tris), refs[0]))

    root = blocks[0]
    # Name, extra data list, controller, flags, transform, collision, then the children.
    at = NODE_HEAD + 4 * struct.unpack_from("<I", root, 4)[0]
    count = struct.unpack_from("<I", root, at)[0]
    if len(root) != at + 4 + 4 * count:
        raise SystemExit("the root node is not laid out as expected")
    children = struct.unpack_from("<%di" % count, root, at + 4) + tuple(a[0] for a in added)
    blocks[0] = root[:at] + struct.pack("<I", len(children)) + ints(*children)

    (before, after), _ = header_parts(leg.d)
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
    # The footer is the vanilla one.
    end = leg.blocks[-1][1] + leg.blocks[-1][2]
    out += leg.d[end:]
    with open(args.out, "xb") as f:
        f.write(out)

    # Read it back: the vanilla blocks untouched, every reference inside its table.
    check = Nif(args.out)
    for i in range(1, kept):
        if bytes(block_of(check, i)) != bytes(block_of(leg, i)):
            raise SystemExit("FAIL: vanilla block %d changed" % i)
    if check.strings[:len(leg.strings)] != leg.strings:
        raise SystemExit("FAIL: vanilla strings moved")
    found = []
    for i, (kind, offset, _) in enumerate(check.blocks):
        if kind == "BSLightingShaderProperty" and i >= kept:
            refs = [struct.unpack_from("<i", check.d, offset + at)[0] for at in (4, ROOT_MATERIAL)]
            if any(not -1 <= r < len(check.strings) for r in refs):
                raise SystemExit("FAIL: shader %d has a string reference outside the table" % i)
            found.append(tuple(check.strings[r] if r >= 0 else None for r in refs))
    if found != expected:
        raise SystemExit("FAIL: shader names read back wrong: %s" % found)
    shapes = place["posed"](args.out, bones)
    if len(shapes) != 1 + len(added):
        raise SystemExit("FAIL: expected %d shapes" % (1 + len(added)))
    for shape, (_, bone, nv, nt) in zip(shapes[1:], added):
        if shape["bones"] != [bone] or len(shape["tris"]) != nt or len(shape["verts"]) != nv:
            raise SystemExit("FAIL: a junk shape does not read back")
        print("on the skeleton: %s to %s" % ([round(min(v[k] for v in shape["verts"]), 1) for k in range(3)],
                                             [round(max(v[k] for v in shape["verts"]), 1) for k in range(3)]))
    print("wrote %s, %d bytes; reads back" % (args.out, len(out)))


if __name__ == "__main__":
    main()

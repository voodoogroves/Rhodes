"""Write the placed shield as a skinned model, made by cutting down the super mutant arm model.

Used by `placeshield.py --write`. The result keeps only the plate's triangles, adds a second set facing the other way (the game
draws one side of a face, and the plate is open where the glove was), stores them in
the power armor forearm bone's coordinates and weights every vertex wholly to that bone.
It is derived from game files: keep it out of every repo.
"""
import math
import struct

BONE = b"LArm_ForeArm1"
BEHIND = 0.05                       # how far the back faces sit behind the front ones
KEEP = ("NiNode", "BSSubIndexTriShape", "BSSkin::Instance", "BSSkin::BoneData",
        "BSLightingShaderProperty", "BSShaderTextureSet")
NODE_HEAD = 72                      # NiNode bytes before its child count


def ints(*values):
    return struct.pack("<%di" % len(values), *values)


def header_parts(d):
    """The file's header, split so the block and string tables can be written again."""
    def short(p):
        return p + 1 + d[p]

    p = d.index(b"\n") + 1
    p += 9                                               # version, endian, user version
    count_at = p
    p += 4
    bs = struct.unpack_from("<I", d, p)[0]
    p = short(p + 4)
    if bs > 130:
        p += 4
    p = short(short(p))
    if 103 <= bs < 170:
        p = short(p)
    start = d[:count_at], d[count_at + 4:p]
    ntypes = struct.unpack_from("<H", d, p)[0]
    p += 2
    types = []
    for _ in range(ntypes):
        n = struct.unpack_from("<I", d, p)[0]
        types.append(d[p + 4:p + 4 + n].decode("latin1"))
        p += 4 + n
    return start, types


def write(nif, shape_block, triangles, place, direction, bone_transform, path, extra=((), ())):
    """nif: nifpreview.Nif of the source. place(i) -> new position of vertex i;
    direction(i, d) -> unit direction d of vertex i after placing; bone_transform: the 52
    bytes (translation, rotation, scale) of the bone's node in a power armor model;
    extra: further (vertices, triangles) already in bone coordinates, as mounts.build makes."""
    d = nif.d
    kinds = [b[0] for b in nif.blocks]
    if any(k not in KEEP for k in kinds) or kinds.count("BSSubIndexTriShape") != 1:
        raise SystemExit("unexpected blocks in the source model")

    def block(i):
        _, offset, size = nif.blocks[i]
        return bytearray(d[offset:offset + size])

    shape = block(shape_block)
    skin_at = kinds.index("BSSkin::Instance")
    data_at = kinds.index("BSSkin::BoneData")
    shader_at = kinds.index("BSLightingShaderProperty")
    texture_at = kinds.index("BSShaderTextureSet")
    desc = struct.unpack_from("<Q", shape, NODE_HEAD + 28)[0]
    if desc != 0x0005B00050430208:
        raise SystemExit("unexpected vertex layout %x" % desc)
    nverts = struct.unpack_from("<H", shape, NODE_HEAD + 40)[0]
    first = NODE_HEAD + 46
    used = sorted({i for t in triangles for i in t})
    new_index = {old: n for n, old in enumerate(used)}
    stride = 32

    def unit(b):
        return tuple(x / 127.5 - 1 for x in b)

    def packed(v):
        return bytes(max(0, min(255, round((x + 1) * 127.5))) for x in v)

    def turned(i, v):
        length = math.sqrt(sum(x * x for x in v))
        return tuple(x * length for x in direction(i, tuple(x / length for x in v))) if length else v

    vertices, points, normals, backs = bytearray(), [], {}, []
    for i in used:
        raw = shape[first + i * stride:first + (i + 1) * stride]
        bx = struct.unpack_from("<e", raw, 6)[0]
        normal, by = unit(raw[12:15]), raw[15] / 127.5 - 1
        tangent, bz = unit(raw[16:19]), raw[19] / 127.5 - 1
        point = place(i)
        normal, tangent, bit = turned(i, normal), turned(i, tangent), turned(i, (bx, by, bz))
        points.append(point)
        normals[i] = normal
        vertices += (struct.pack("<4e", *point, bit[0]) + raw[8:12]
                     + packed(normal) + packed(bit[1:2]) + packed(tangent) + packed(bit[2:3])
                     + struct.pack("<4e4B", 1, 0, 0, 0, 0, 0, 0, 0))
        behind = tuple(point[k] - BEHIND * normal[k] for k in range(3))
        backs.append((behind, raw[8:12], tuple(-c for c in normal), tangent, bit))

    for point, uv, normal, tangent, bit in backs:
        points.append(point)
        vertices += (struct.pack("<4e", *point, bit[0]) + uv
                     + packed(normal) + packed(bit[1:2]) + packed(tangent) + packed(bit[2:3])
                     + struct.pack("<4e4B", 1, 0, 0, 0, 0, 0, 0, 0))

    # Mirroring turns faces inside out: wind each triangle to agree with its vertex normals.
    agree = []
    for t in triangles:
        a, b, c = (points[new_index[i]] for i in t)
        u, v = [b[k] - a[k] for k in range(3)], [c[k] - a[k] for k in range(3)]
        face = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
        agree.append(sum(face[k] * sum(normals[i][k] for i in t) for k in range(3)) > 0)
    flip = sum(agree) < len(agree) / 2
    print("triangles facing with their normals: %d of %d; winding %s"
          % (sum(agree), len(agree), "reversed" if flip else "kept"))
    faces = bytearray()
    for a, b, c in triangles:
        if flip:
            b, c = c, b
        faces += struct.pack("<3H", new_index[a], new_index[b], new_index[c])
        faces += struct.pack("<3H", *(len(used) + new_index[i] for i in (a, c, b)))

    for point, uv, normal, tangent, bit in extra[0]:
        points.append(point)
        vertices += (struct.pack("<4e2e", *point, bit[0], *uv)
                     + packed(normal) + packed(bit[1:2]) + packed(tangent) + packed(bit[2:3])
                     + struct.pack("<4e4B", 1, 0, 0, 0, 0, 0, 0, 0))
    for t in extra[1]:
        faces += struct.pack("<3H", *(2 * len(used) + i for i in t))

    n = 2 * len(triangles) + len(extra[1])
    total = 2 * len(used) + len(extra[0])
    segments = struct.pack("<3I", n, 5, 5)
    for s in range(5):                                    # all in the fifth, as vanilla arms do
        segments += struct.pack("<IIiI", 0, n if s == 4 else 0, -1, 0)
    shape = (shape[:NODE_HEAD + 40] + struct.pack("<HI", total, len(vertices) + len(faces))
             + vertices + faces + segments)
    struct.pack_into("<I", shape, NODE_HEAD + 36, n)

    root = block(0)
    bone = block(1)
    # New block order: root, bone, shape, skin, bone data, shader, textures.
    struct.pack_into("<3i", shape, NODE_HEAD + 16, 3, 5, -1)
    root = root[:NODE_HEAD] + struct.pack("<I", 2) + ints(1, 2)
    bone[NODE_HEAD - 56:NODE_HEAD - 4] = bone_transform
    skin = ints(0, 4) + struct.pack("<I", 1) + ints(1) + struct.pack("<I", 0)
    centre = [(min(p[k] for p in points) + max(p[k] for p in points)) / 2 for k in range(3)]
    radius = max(math.dist(p, centre) for p in points)
    identity = (1, 0, 0, 0, 1, 0, 0, 0, 1)
    bone_data = struct.pack("<I17f", 1, *centre, radius, *identity, 0, 0, 0, 1)
    shader = block(shader_at)
    if struct.unpack_from("<i", shader, 40)[0] != texture_at:
        raise SystemExit("texture set reference not where expected")
    struct.pack_into("<i", shader, 40, 6)
    blocks = [root, bone, shape, skin, bone_data, shader, block(texture_at)]
    names = ["NiNode", "NiNode", "BSSubIndexTriShape", "BSSkin::Instance", "BSSkin::BoneData",
             "BSLightingShaderProperty", "BSShaderTextureSet"]

    strings = [s.encode("latin1") for s in nif.strings]
    name_of = lambda b: struct.unpack_from("<i", b, 0)[0]
    strings[name_of(root)] = b"PAXShield.nif"
    strings[name_of(bone)] = BONE
    strings[name_of(shape)] = b"PAXShield"

    (before, after), _ = header_parts(d)
    types = list(dict.fromkeys(names))
    out = bytearray(before + struct.pack("<I", len(blocks)) + after)
    out += struct.pack("<H", len(types))
    for t in types:
        out += struct.pack("<I", len(t)) + t.encode()
    out += struct.pack("<%dH" % len(names), *(types.index(t) for t in names))
    out += struct.pack("<%dI" % len(blocks), *(len(b) for b in blocks))
    out += struct.pack("<II", len(strings), max(len(s) for s in strings))
    for s in strings:
        out += struct.pack("<I", len(s)) + s
    out += struct.pack("<I", 0)                           # no groups
    for b in blocks:
        out += b
    out += ints(1, 0)                                     # footer: one root, block 0
    with open(path, "wb") as f:
        f.write(out)
    print("wrote %s: %d vertices, %d triangles" % (path, total, n))

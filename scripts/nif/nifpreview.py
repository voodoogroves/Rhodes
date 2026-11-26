#!/usr/bin/env python3
"""Read Fallout 4 NIF models and draw flat-shaded preview PNGs. Standard library only.

  python3 -I nifpreview.py info   model.nif            shapes, loose parts, bones, connect points
  python3 -I nifpreview.py render model.nif out.png    six views; each loose part gets a colour
      --seams            also split parts at texture seams (separates joined pieces)
      --parts 1,3        draw only these parts (numbers from info)
      --size 600         pixels per view

Reads BSTriShape and BSSubIndexTriShape (stream version 130). Skinned meshes are drawn
as stored (bind pose); bones are reported, not applied. Reads only; never writes a model.
Extracted models and previews are game-derived: keep them out of every repo.
"""
import argparse
import math
import struct
import sys
import zlib

SHAPES = ("BSTriShape", "BSSubIndexTriShape")
NODES = ("NiNode", "BSFadeNode")
COLOURS = [("red", (220, 70, 60)), ("blue", (70, 120, 220)), ("green", (80, 170, 80)),
           ("orange", (235, 150, 40)), ("purple", (150, 90, 200)), ("teal", (40, 170, 175)),
           ("yellow", (215, 200, 50)), ("pink", (230, 110, 170)), ("brown", (140, 100, 60)),
           ("grey", (140, 140, 140))]


class Nif:
    def __init__(self, path):
        with open(path, "rb") as f:
            self.d = f.read()
        self.p = self.d.index(b"\n") + 1
        self._u("I"), self._u("B"), self._u("I")          # version, endian, user version
        count = self._u("I")
        self.bs = self._u("I")
        self._short()
        if self.bs > 130:
            self._u("I")
        self._short(), self._short()
        if 103 <= self.bs < 170:
            self._short()
        types = [self._sized() for _ in range(self._u("H"))]
        index = [self._u("H") & 0x7FFF for _ in range(count)]
        sizes = [self._u("I") for _ in range(count)]
        strings = self._u("I")
        self._u("I")
        self.strings = [self._sized() for _ in range(strings)]
        for _ in range(self._u("I")):
            self._u("I")
        self.blocks = []
        for i in range(count):
            self.blocks.append((types[index[i]], self.p, sizes[i]))
            self.p += sizes[i]
        if self.p > len(self.d):
            raise ValueError("truncated file")

    def _u(self, fmt):
        v = struct.unpack_from("<" + fmt, self.d, self.p)
        self.p += struct.calcsize("<" + fmt)
        return v[0] if len(v) == 1 else v

    def _short(self):
        n = self._u("B")
        self.p += n

    def _sized(self):
        n = self._u("I")
        s = self.d[self.p:self.p + n]
        self.p += n
        return s.decode("latin1")

    def string(self, i):
        return self.strings[i] if 0 <= i < len(self.strings) else ""

    def av_object(self, block):
        """Name, local transform (translation, rotation rows, scale), offset after the header."""
        self.p = self.blocks[block][1]
        name = self.string(self._u("i"))
        for _ in range(self._u("I")):
            self._u("i")
        self._u("i"), self._u("I")                        # controller, flags
        t = self._u("3f")
        r = self._u("9f")
        s = self._u("f")
        self._u("i")                                      # collision
        return name, (t, r, s), self.p

    def parents(self):
        out = {}
        for i, (kind, _, _) in enumerate(self.blocks):
            if kind in NODES:
                self.av_object(i)
                for _ in range(self._u("I")):
                    child = self._u("i")
                    if child >= 0:
                        out[child] = i
        return out

    def shapes(self):
        parents = self.parents()
        for i, (kind, _, _) in enumerate(self.blocks):
            if kind not in SHAPES:
                continue
            name, local, _ = self.av_object(i)
            self._u("4f")                                 # bounding sphere
            skin = self._u("i")
            self._u("i"), self._u("i")                    # shader, alpha
            desc = self._u("Q")
            ntris = self._u("I")
            nverts = self._u("H")
            if not self._u("I"):
                continue
            stride = (desc & 0xF) * 4
            flags = desc >> 44
            skin_at = ((desc >> 28) & 0xF) * 4
            start = self.p
            verts, weights = [], []
            for v in range(nverts):
                o = start + v * stride
                verts.append(struct.unpack_from("<3f" if flags & 0x400 else "<3e", self.d, o))
                if flags & 0x40:
                    w = struct.unpack_from("<4e", self.d, o + skin_at)
                    b = struct.unpack_from("<4B", self.d, o + skin_at + 8)
                    weights.append([(bone, x) for bone, x in zip(b, w) if x > 0])
            at = start + nverts * stride
            tris = [struct.unpack_from("<3H", self.d, at + t * 6) for t in range(ntris)]
            chain, node = [local], i
            while node in parents:
                node = parents[node]
                chain.append(self.av_object(node)[1])
            for t, r, s in chain:
                verts = [tuple(s * (r[3 * a] * x + r[3 * a + 1] * y + r[3 * a + 2] * z) + t[a]
                               for a in range(3)) for x, y, z in verts]
            yield {"name": name, "verts": verts, "tris": tris, "weights": weights,
                   "bones": self.bones(skin) if skin >= 0 else []}

    def bones(self, block):
        if self.blocks[block][0] != "BSSkin::Instance":
            return []
        self.p = self.blocks[block][1] + 8                # skeleton root, bone data
        refs = [self._u("i") for _ in range(self._u("I"))]
        return [self.av_object(r)[0] if r >= 0 else "?" for r in refs]

    def connect_points(self):
        for kind, offset, _ in self.blocks:
            if not kind.startswith("BSConnectPoint::"):
                continue
            self.p = offset + 4                           # name
            if kind.endswith("Parents"):
                for _ in range(self._u("I")):
                    parent, name = self._sized(), self._sized()
                    v = self._u("8f")
                    yield "point %s on '%s' at (%.2f, %.2f, %.2f)" % (name, parent, v[4], v[5], v[6])
            else:
                self._u("B")
                names = [self._sized() for _ in range(self._u("I"))]
                yield "attaches to " + ", ".join(names)


def loose_parts(shape, seams=False):
    """Split a shape into triangle groups that share no vertex position, largest first.
    With seams, groups need only share no vertex, which also cuts along texture seams."""
    ids = {}
    welded = [i if seams else ids.setdefault(tuple(round(c, 2) for c in v), len(ids))
              for i, v in enumerate(shape["verts"])]
    root = list(range(len(shape["verts"])))

    def find(a):
        while root[a] != a:
            root[a] = root[root[a]]
            a = root[a]
        return a

    for a, b, c in shape["tris"]:
        for other in (b, c):
            root[find(welded[other])] = find(welded[a])
    groups = {}
    for tri in shape["tris"]:
        groups.setdefault(find(welded[tri[0]]), []).append(tri)
    return sorted(groups.values(), key=len, reverse=True)


def all_parts(nif, seams=False):
    parts = [(shape, tris) for shape in nif.shapes() for tris in loose_parts(shape, seams)]
    return sorted(parts, key=lambda p: len(p[1]), reverse=True)


def describe(shape, tris):
    used = {i for t in tris for i in t}
    pts = [shape["verts"][i] for i in used]
    span = "  ".join("%s %.1f..%.1f" % (n, min(p[a] for p in pts), max(p[a] for p in pts))
                     for a, n in enumerate("XYZ"))
    total = {}
    for i in used:
        for bone, w in (shape["weights"][i] if shape["weights"] else []):
            total[bone] = total.get(bone, 0) + w
    top = sorted(total.items(), key=lambda b: -b[1])[:3]
    bones = ", ".join("%s %d%%" % (shape["bones"][b] if b < len(shape["bones"]) else b,
                                   round(100 * w / len(used))) for b, w in top)
    return "%4d tris  %s%s" % (len(tris), span, "\n         bones: " + bones if bones else "")


def view_basis(forward, up):
    def norm(v):
        n = math.sqrt(sum(c * c for c in v))
        return tuple(c / n for c in v)

    def cross(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

    f = norm(forward)
    r = norm(cross(f, up))
    return r, cross(r, f), f


# Fallout 4: +X is the model's right, +Y forward, +Z up. (title, camera direction, screen up)
VIEWS = [("front", (0, -1, 0), (0, 0, 1)), ("model's left side", (1, 0, 0), (0, 0, 1)),
         ("top", (0, 0, -1), (0, 1, 0)),
         ("back", (0, 1, 0), (0, 0, 1)), ("model's right side", (-1, 0, 0), (0, 0, 1)),
         ("front right, above", (-1, -1, -0.6), (0, 0, 1))]


def render(parts, size, path):
    big = size * 2                                        # draw at double size, then average
    width, height = big * 3, big * 2                      # three views across, two down
    pixels = bytearray([245]) * (width * height * 3)
    depth = [math.inf] * (width * height)
    used = [shape["verts"][i] for _, (shape, tris) in parts for t in tris for i in t]
    centre = tuple((min(p[a] for p in used) + max(p[a] for p in used)) / 2 for a in range(3))
    radius = max(math.dist(p, centre) for p in used) or 1
    scale = big * 0.47 / radius
    for v, (_, forward, up) in enumerate(VIEWS):
        basis = view_basis(forward, up)
        ox, oy = (v % 3) * big, (v // 3) * big
        for number, (shape, tris) in parts:
            colour = COLOURS[(number - 1) % len(COLOURS)][1]
            for tri in tris:
                pts = []
                for i in tri:
                    q = [shape["verts"][i][a] - centre[a] for a in range(3)]
                    x, y, z = (sum(q[a] * axis[a] for a in range(3)) for axis in basis)
                    pts.append((ox + big / 2 + x * scale, oy + big / 2 - y * scale, z))
                (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = pts
                area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
                if abs(area) < 1e-9:
                    continue
                u = [pts[1][a] - pts[0][a] for a in range(3)]
                w = [pts[2][a] - pts[0][a] for a in range(3)]
                nx, ny = u[1] * w[2] / scale - u[2] * w[1] / scale, u[2] * w[0] / scale - u[0] * w[2] / scale
                nz = (u[0] * w[1] - u[1] * w[0]) / (scale * scale)
                light = 0.3 + 0.7 * abs(nz) / (math.sqrt(nx * nx + ny * ny + nz * nz) or 1)
                shade = bytes(int(c * light) for c in colour)
                for py in range(max(oy, int(min(y0, y1, y2))), min(oy + big, int(max(y0, y1, y2)) + 1)):
                    for px in range(max(ox, int(min(x0, x1, x2))), min(ox + big, int(max(x0, x1, x2)) + 1)):
                        cx, cy = px + 0.5, py + 0.5
                        b1 = ((cx - x0) * (y2 - y0) - (x2 - x0) * (cy - y0)) / area
                        b2 = ((x1 - x0) * (cy - y0) - (cx - x0) * (y1 - y0)) / area
                        if b1 < 0 or b2 < 0 or b1 + b2 > 1:
                            continue
                        z = z0 + b1 * (z1 - z0) + b2 * (z2 - z0)
                        k = py * width + px
                        if z < depth[k]:
                            depth[k] = z
                            pixels[3 * k:3 * k + 3] = shade
    rows = bytearray()
    for y in range(size * 2):
        rows.append(0)
        for x in range(size * 3):
            if (x and x % size == 0) or y == size:
                rows += b"\x80\x80\x80"
                continue
            k = [3 * ((2 * y + dy) * width + 2 * x + dx) for dy in (0, 1) for dx in (0, 1)]
            rows += bytes(sum(pixels[i + c] for i in k) // 4 for c in range(3))

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size * 3, size * 2, 8, 2, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(bytes(rows), 9)) + chunk(b"IEND", b""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=("info", "render"))
    ap.add_argument("model")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--parts")
    ap.add_argument("--seams", action="store_true")
    ap.add_argument("--size", type=int, default=600)
    args = ap.parse_args()
    nif = Nif(args.model)
    parts = list(enumerate(all_parts(nif, args.seams), 1))
    if args.parts:
        wanted = {int(n) for n in args.parts.split(",")}
        parts = [p for p in parts if p[0] in wanted]
    if args.command == "info":
        for number, (shape, tris) in parts:
            print("part %d (%s) of %s\n    %s" % (number, COLOURS[(number - 1) % len(COLOURS)][0],
                                                  shape["name"], describe(shape, tris)))
        for line in nif.connect_points():
            print(line)
        return
    if not args.out or not parts:
        sys.exit("render needs an output file and at least one part")
    render(parts, args.size, args.out)
    print(args.out, "| views, left to right then down:", "; ".join(v[0] for v in VIEWS))


if __name__ == "__main__":
    main()

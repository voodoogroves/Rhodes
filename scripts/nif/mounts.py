"""Solid mounting blocks that join the placed shield to the forearm, in forearm bone coordinates.

Each block runs along the forearm (X) and spans an angle around it. At every grid point a ray
from the bone's axis finds the arm's surface and the plate: the block starts just under the
arm's surface and stops just short of the plate. It borrows the plate's texture from where the
ray meets it, so it uses the plate's own metal.
"""
import math

SINK, GAP = 0.8, 0.15            # how far the block reaches into the arm; how short of the plate
STATIONS = ((3.0, 9.0), (16.0, 23.0))        # along the forearm: elbow 0, hand joint 27
HALF_ANGLE = 28.0                # degrees either side of the blocks' middle
SWING = -20.0                    # the middle, in degrees from the plate's middle: where arm and plate are closest
ALONG, AROUND = 8, 14            # grid cells


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def unit(a):
    n = math.sqrt(dot(a, a))
    return tuple(c / n for c in a) if n > 1e-9 else (1.0, 0.0, 0.0)


def hits(origin, d, triangles):
    """(distance, triangle number, b1, b2) for every triangle the ray passes through."""
    out = []
    for n, (a, b, c) in enumerate(triangles):
        e1, e2 = sub(b, a), sub(c, a)
        h = cross(d, e2)
        det = dot(e1, h)
        if abs(det) < 1e-9:
            continue
        s = sub(origin, a)
        b1 = dot(s, h) / det
        q = cross(s, e1)
        b2 = dot(d, q) / det
        t = dot(e2, q) / det
        if b1 >= -1e-6 and b2 >= -1e-6 and b1 + b2 <= 1 + 1e-6 and t > 0:
            out.append((t, n, b1, b2))
    return out


def build(arm, plate, plate_uvs, toward):
    """arm, plate: triangles as three points; plate_uvs: matching triples of (u, v);
    toward: unit direction (y, z) from the bone's axis to the plate.
    Returns vertices (position, uv, normal, tangent, bitangent) and triangles."""
    base = math.atan2(toward[1], toward[0]) + math.radians(SWING)
    density = []
    for tri, uv in zip(plate, plate_uvs):
        length = math.dist(tri[0], tri[1])
        if length > 1:
            density.append(math.dist(uv[0], uv[1]) / length)
    density = sorted(density)[len(density) // 2]
    vertices, triangles = [], []
    for x0, x1 in STATIONS:
        grid = []
        for i in range(ALONG + 1):
            x = x0 + (x1 - x0) * i / ALONG
            row = []
            for j in range(AROUND + 1):
                angle = base + math.radians(HALF_ANGLE) * (2 * j / AROUND - 1)
                d = (0.0, math.cos(angle), math.sin(angle))
                origin = (x, 0.0, 0.0)
                on_arm, on_plate = hits(origin, d, arm), hits(origin, d, plate)
                if not on_arm or not on_plate:
                    raise SystemExit("mount at %.1f along, angle %d misses the %s"
                                     % (x, j, "arm" if not on_arm else "plate"))
                surface = max(h[0] for h in on_arm)
                near = min(on_plate)
                # Sample around the ray too, so a flat block face cannot cut through a ridge.
                reach = near[0]
                for dx, da in ((-0.6, 0), (0.6, 0), (0, -0.04), (0, 0.04)):
                    more = hits((x + dx, 0.0, 0.0), (0.0, math.cos(angle + da), math.sin(angle + da)), plate)
                    if more:
                        reach = min(reach, min(more)[0])
                top = reach - GAP
                bottom = min(surface - SINK, top - 0.3)
                _, n, b1, b2 = near
                uv = tuple(plate_uvs[n][0][k] * (1 - b1 - b2) + plate_uvs[n][1][k] * b1
                           + plate_uvs[n][2][k] * b2 for k in range(2))
                low = tuple(origin[k] + d[k] * bottom for k in range(3))
                high = tuple(origin[k] + d[k] * top for k in range(3))
                row.append((low, high, uv))
            grid.append(row)

        points = [p for row in grid for cell in row for p in cell[:2]]
        middle = tuple(sum(p[k] for p in points) / len(points) for k in range(3))

        def quad(corners):
            """corners: four (point, uv) in order round the face."""
            for tri in ((0, 1, 2), (0, 2, 3)):
                (p0, t0), (p1, t1), (p2, t2) = (corners[k] for k in tri)
                e1, e2 = sub(p1, p0), sub(p2, p0)
                normal = cross(e1, e2)
                if dot(normal, normal) < 1e-8:
                    continue
                centre = tuple((p0[k] + p1[k] + p2[k]) / 3 for k in range(3))
                order = [(p0, t0), (p1, t1), (p2, t2)]
                if dot(normal, sub(centre, middle)) < 0:
                    order[1], order[2] = order[2], order[1]
                    normal = tuple(-c for c in normal)
                normal = unit(normal)
                du1, dv1, du2, dv2 = t1[0] - t0[0], t1[1] - t0[1], t2[0] - t0[0], t2[1] - t0[1]
                det = du1 * dv2 - du2 * dv1
                along = ([(e1[k] * dv2 - e2[k] * dv1) / det for k in range(3)] if abs(det) > 1e-12
                         else e1)
                tangent = unit(tuple(along[k] - normal[k] * dot(along, normal) for k in range(3)))
                bitangent = cross(normal, tangent)
                for p, uv in order:
                    vertices.append((p, uv, normal, tangent, bitangent))
                triangles.append(tuple(range(len(vertices) - 3, len(vertices))))

        for i in range(ALONG):
            for j in range(AROUND):
                for layer in (0, 1):
                    quad([(grid[a][b][layer], grid[a][b][2])
                          for a, b in ((i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1))])
        edges = ([((0, j), (0, j + 1)) for j in range(AROUND)]
                 + [((ALONG, j), (ALONG, j + 1)) for j in range(AROUND)]
                 + [((i, 0), (i + 1, 0)) for i in range(ALONG)]
                 + [((i, AROUND), (i + 1, AROUND)) for i in range(ALONG)])
        for first, second in edges:
            a, b = grid[first[0]][first[1]], grid[second[0]][second[1]]
            drop_a, drop_b = math.dist(a[0], a[1]) * density, math.dist(b[0], b[1]) * density
            quad([(a[1], a[2]), (b[1], b[2]), (b[0], (b[2][0], b[2][1] + drop_b)),
                  (a[0], (a[2][0], a[2][1] + drop_a))])
    return vertices, triangles

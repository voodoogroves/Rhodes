#!/usr/bin/env python3
"""Add shape to a fitted female outfit: seat, the crease under it, the back, the chest.

  python3 sculpt.py IN.nif OUT.nif [--back 1.0] [--front 1.0]

The cheeks are one broad swelling; each other feature is a soft hollow at a fixed place in
vanilla female outfit coordinates (+y is forward, heights run downward from the neck),
mirrored left and right. --back and --front scale them; 0 turns that side off. Points are
moved by position, so seams, trim and layers travel together. Stored normals follow the new
surface. Run it after fitbody.py hug, on a model fine enough to hold the detail
(subdivide.py).
The result is derived from the source model: keep it out of every repo.
"""
import argparse
import math

from fitbody import apply
from nifpreview import Nif

# side (-1 back, 1 front), |x|, height, width, tall, amount (+ stands out, - sinks in)
FEATURES = (
    (-1, 0.0, -52.6, 1.1, 4.2, -1.15),   # line between the cheeks
    (-1, 3.6, -57.8, 2.6, 1.3, -0.55),   # crease underneath
    (-1, 0.0, -36.0, 1.0, 7.0, -0.30),   # line up the spine
    (1, 0.0, -22.5, 1.1, 3.0, -0.55),    # between the chest
    (1, 4.0, -27.8, 2.4, 1.2, -0.45),    # under the chest
)
# Cheeks: a broad swelling that reaches further up than down and meets the cloth around it
# without an edge. |x|, height, half width, reach up, reach down, amount.
CHEEK = (3.9, -51.8, 5.4, 9.0, 6.6, 1.35)


def cheek(p):
    """How much further back p should sit."""
    x, z, width, up, down, amount = CHEEK
    r = ((abs(p[0]) - x) / width) ** 2 + ((p[2] - z) / (up if p[2] > z else down)) ** 2
    if r >= 1:
        return 0.0
    facing = max(0.0, min(1.0, (-p[1] - 2) / 4))
    return amount * facing * (1 - r) ** 1.6


def sculpt(source, target, back, front):
    def move(p):
        y = -back * cheek(p)
        for side, x, z, width, tall, amount in FEATURES:
            facing = max(0.0, min(1.0, (side * p[1] - 2) / 3))      # leave the far side alone
            if not facing:
                continue
            spread = ((abs(p[0]) - x) / width) ** 2 + ((p[2] - z) / tall) ** 2
            if spread < 9:
                y += side * amount * facing * math.exp(-spread) * (back if side < 0 else front)
        return (0.0, y, 0.0)

    apply(Nif(source), source, target, move, turn=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("source")
    ap.add_argument("target")
    ap.add_argument("--back", type=float, default=1.0)
    ap.add_argument("--front", type=float, default=1.0)
    a = ap.parse_args()
    if a.source == a.target:
        raise SystemExit("give a different output file")
    sculpt(a.source, a.target, a.back, a.front)


if __name__ == "__main__":
    main()

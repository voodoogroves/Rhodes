#!/usr/bin/env python3
"""Draw the whole Raider set on one suit: claw, brick ram, shotgun rack and scrap harness.

  python3 -I placeset.py MESHES OUTDIR

MESHES holds everything placeram.py, placerack.py and placeharness.py ask for. Writes
raider_set.png (six views, slow). Previews only: no game model is written. The picture is derived
from game files: keep it out of every repo.
"""
import argparse
import os
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))
arms, rack, harness = (runpy.run_path(os.path.join(HERE, "place%s.py" % n)) for n in ("ram", "rack", "harness"))
place, render, moved = arms["place"], arms["render"], arms["moved"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("meshes")
    ap.add_argument("outdir")
    args = ap.parse_args()
    meshes = args.meshes
    if os.path.isdir(os.path.join(meshes, "meshes")):
        meshes = os.path.join(meshes, "meshes")
    bones = place["skeleton"](os.path.join(meshes, "actors/powerarmor/characterassets/skeleton.nif"))
    suit, junk = harness["build"](meshes, bones)
    parts = junk + rack["build"](meshes, bones)
    left = arms["ram"](meshes, arms["arm"](meshes, bones, "L")[1])
    right = arms["worn_claw"](meshes, arms["arm"](meshes, bones, "R")[1])
    for bone, own in (("LArm_ForeArm1", left), ("RArm_ForeArm1", right)):
        parts += [(c, moved(q, q["tris"], lambda p, bone=bone: place["to_model"](bones[bone], p)))
                  for c, q in own]
    os.makedirs(args.outdir, exist_ok=True)
    render(suit + [(c, (q, q["tris"])) for c, q in parts],
           700, os.path.join(args.outdir, "raider_set.png"))
    print("drawn")


if __name__ == "__main__":
    main()

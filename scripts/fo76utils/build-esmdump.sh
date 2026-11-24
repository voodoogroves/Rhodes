#!/usr/bin/env bash
# Build esmdump (record lister for .esm/.esp files) from fo76utils and install it to ~/.local/bin.
# No scons needed. Tested 2026-11-24 on the Deck with g++ (C++20) against upstream commit
# c52da18 (MIT license); takes about 12 seconds. Flags mirror the upstream SConstruct.
#
# Usage: build-esmdump.sh        (clones to ~/Repos/upstream/fo76utils if missing)
set -euo pipefail

SRC="${FO76UTILS_SRC:-$HOME/Repos/upstream/fo76utils}"
DEST="${BAUNPACK_DEST:-$HOME/.local/bin}"

if [ ! -d "$SRC/.git" ]; then
    git clone --depth 1 https://github.com/fo76utils/fo76utils.git "$SRC"
fi

L="$SRC/libfo76utils/src"
mkdir -p "$DEST"
g++ -std=c++20 -O2 -march=sandybridge -ffast-math -I"$SRC/src" -I"$L" -o "$DEST/esmdump" \
    "$SRC/src/esmdump.cpp" "$SRC/src/esmdbase.cpp" \
    "$L/common.cpp" "$L/filebuf.cpp" "$L/zlib.cpp" "$L/ba2file.cpp" "$L/esmfile.cpp" "$L/stringdb.cpp" \
    -lm -lpthread

echo "built $DEST/esmdump"

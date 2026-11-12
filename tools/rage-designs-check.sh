#!/bin/sh
# tools/rage-designs-check.sh [DB] - on the Tegra (an ARM host), designs/' forth-arm checked against what it measured
# (Iteration 646). Run from the laptop through tools/rage-check.sh, which copies HEAD there and builds the stages:
#   RAGECHECK_CMD='sh tools/rage-designs-check.sh' sh tools/rage-check.sh
# A copy of designs/, then lab/evolve/export-arm.py on it natively: each GCC design without the JIT built by the host's
# cc as the lab's build() builds it - the bytes the Tegra measured (GCC 16) - and its Makefile's `make forth-arm` (CCARM
# cc) must give them byte for byte and run ': SQ DUP * ; 7 SQ .' to 49. The clang designs are cross-built on x86-64 (the
# Tegra has no clang) and checked there. Every design of designs/ is passed: export-arm.py takes this host's by each
# design's exported Makefile, its --list printed first (Iteration 652). DB: the records, default designs/*/record.json -
# what designs/ holds (652: the default was results/relf-designs-636.md, without 649's smallest).
set -u
T=$(mktemp -d) && cp -r designs "$T/designs" || exit 1
N=$(for r in designs/*/record.json; do printf '%s=%s,' "$(basename "$(dirname "$r")")" \
    "$(python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["id"])' "$r")"; done | sed 's/,$//')
DB=${1:-$T/records.md}
[ $# -ge 1 ] || for r in designs/*/record.json; do
    python3 -c 'import json, sys; print(json.dumps(json.load(open(sys.argv[1]))))' "$r"; done > "$DB"
python3 lab/evolve/export-arm.py "$T/designs" "$DB" "$N" --list && python3 lab/evolve/export-arm.py "$T/designs" "$DB" "$N"; rc=$?
rm -rf "$T"; exit $rc

#!/bin/sh
# jit-check.sh - how this machine's compiler shaped SPN's stencils, read by
# engine/jit.c's scanner (JIT.md). A stencil without the expected holes is
# never used by the JIT: this shows which, before anything relies on it.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT=${TMPDIR:-/tmp}/jit-check.$$
trap 'rm -f "$OUT"' EXIT
cc ${CFLAGS:--O2} -DJIT_SCAN_MAIN -I"$ROOT/engine" -o "$OUT" "$ROOT/engine/jit.c" "$ROOT/engine/spn-stencils.c" "$ROOT/engine/spn-markers.c"
"$OUT"

#!/bin/bash
# find-depth.sh - how many dictionary entries does each system visit?
#
# The corpus and parse benchmarks both say SOD32 is much faster than
# anything in this repository, and loop-bench.sh says the VMs are not the
# reason. This script finds the reason.
#
# METHOD, and it is symmetric on purpose: add one counter to the outer
# loop of SEARCH-WORDLIST in each system's own kernel source, rebuild
# each system with its own cross-compiler, run the identical workload,
# print the counter. Nothing is modelled and nothing is shared except
# the workload.
#
# Everything happens in a scratch directory. An earlier version of this
# copied the Forth sources out of build/work, which holds SYMLINKS back
# into forth/, and so instrumented the tracked kernel instead of a copy.
set -e
cd "$(dirname "$0")/.."
ROOT=$PWD
O=${1:-/tmp/find-depth}
rm -rf "$O"; mkdir -p "$O/relf" "$O/sod32"

WORK=${2:-$ROOT/build}
[ -x "$WORK/s0-cell-64" ] || { echo "run tools/build-stages.sh first"; exit 1; }

# The workload: 4000 lines of interpreted arithmetic, half of whose
# tokens are numbers. A number is the worst case for a dictionary
# search, because it is not found, so the whole chain is walked before
# the system gives up and converts it.
# parse.fth ends with its own BYE, which would exit before the counter
# is ever printed; drop that last line and supply our own tail.
sed '$d' "$ROOT/bench/parse.fth" > "$O/work.fth"
printf 'FINDITER @ . CR\nBYE\n' >> "$O/work.fth"

# ---- RelF ------------------------------------------------------------
for f in "$ROOT"/forth/*.4; do cp -L "$f" "$O/relf/"; done
cp -L "$ROOT/forth/kernel-seed.img" "$O/relf/kernel.img"
cp "$WORK/s0-cell-64" "$O/relf/relf"
python3 - "$O/relf/kernel.4" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
s = s.replace("VARIABLE NAMEBUF ( --- a-addr)",
              "VARIABLE FINDITER ( --- a-addr)\nVARIABLE NAMEBUF ( --- a-addr)", 1)
s = s.replace("   NAMEBUF @ OVER @ -1 224 XOR AND = ",
              "   1 FINDITER +!\n   NAMEBUF @ OVER @ -1 224 XOR AND = ", 1)
open(p, 'w').write(s)
PY
( cd "$O/relf" && printf 'S" extend.4" INCLUDED\nS" cross.4" INCLUDED\n' \
    | ./relf kernel.img >/dev/null 2>&1 )
RELF=$( cd "$O/relf" && ./relf kernel.img < "$O/work.fth" 2>&1 \
        | tr -d '\r' | grep -oE '[0-9]{3,}' | tail -1 )

# ---- SOD32 -----------------------------------------------------------
cp "$ROOT"/vendor/sod32/* "$O/sod32/"
( cd "$O/sod32" && make >/dev/null 2>&1 )
python3 - "$O/sod32/kernel.4th" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
s = s.replace("VARIABLE NAMEBUF ( --- a-addr)",
              "VARIABLE FINDITER ( --- a-addr)\nVARIABLE NAMEBUF ( --- a-addr)", 1)
s = s.replace("   NAMEBUF @ OVER @ $1FFFFFFF AND = ",
              "   1 FINDITER +!\n   NAMEBUF @ OVER @ $1FFFFFFF AND = ", 1)
open(p, 'w').write(s)
PY
( cd "$O/sod32" && printf 'S" cross.4th" INCLUDED \n' | ./sod32 forth.img >/dev/null 2>&1
  printf 'S" extend.4th" INCLUDED \n' | ./sod32 kernel.img >/dev/null 2>&1 )
SOD=$( cd "$O/sod32" && ./sod32 forth.img < "$O/work.fth" 2>&1 \
       | tr -d '\r' | grep -oE '[0-9]{3,}' | tail -1 )

echo
printf '%-10s %16s\n' system "entries visited"
printf '%-10s %16s\n' sod32 "$SOD"
printf '%-10s %16s\n' relf "$RELF"
python3 -c "print('\nratio %.1fx' % ($RELF / $SOD))"

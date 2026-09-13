#!/bin/bash
# build-stages.sh [OUTDIR] - build every stage in stages/STAGES.md, at
# both cell widths, from a clean checkout.
#
# Output goes to OUTDIR (default build/). Nothing is written back into
# the tracked tree, so a build can always be thrown away and redone.
#
# The Forth sources INCLUDE each other by bare filename, so everything
# runs in a flat work directory ($O/work) built by symlink. That keeps
# the repository organised without making the runtime care.
set -e
cd "$(dirname "$0")/.."
ROOT=$PWD
O=${1:-$ROOT/build}
mkdir -p "$O"; O=$(cd "$O" && pwd)
W=$O/work
mkdir -p "$W"

# The fold set: primitives that get a folded `prim;EXIT` opcode. It must
# match forth/cv8.4's FOLD-OPS, which is what the image's own compiler
# uses to fold at run time. Checked, not assumed.
HOT='+,=,!,@,LSHIFT,RSHIFT,C@,C!,AND,OR,XOR,LIT,<,U<,OVER,DROP,DUP,SWAP,ROT,>R,R>,R@,NEGATE'
CV8_LIST=$(sed -n "/^CREATE FOLD-OPS/,/^ALIGN/p" forth/cv8.4 |
           grep -o "' [^ ]* >OP" | sed "s/^' //; s/ >OP$//" | paste -sd,)
[ "$CV8_LIST" = "$HOT" ] || {
    echo "fold set mismatch between build-stages.sh and forth/cv8.4:"
    echo "  here:      $HOT"
    echo "  cv8.4:     $CV8_LIST"; exit 1; }

SPECS=loc,var,tiny,small,imm

# ---- flat work directory ---------------------------------------------
ln -sf "$ROOT"/forth/*.4        "$W"/ 2>/dev/null || true
ln -sf "$ROOT"/tools/*.4        "$W"/ 2>/dev/null || true
ln -sf "$ROOT"/tests/core/*.fr  "$W"/ 2>/dev/null || true
ln -sf "$ROOT"/tests/core/*.fth "$W"/ 2>/dev/null || true
cp -f "$ROOT/forth/kernel-seed.img"   "$W/kernel.img"
cp -f "$ROOT/forth/kernel32-seed.img" "$W/kernel32.img"

# ---- stage -1: SOD32, the ancestor ------------------------------------
# Built out-of-tree so vendor/sod32 stays exactly as upstream shipped it.
# The Makefile's own chain is kept: kernel.img + extend.4th -> forth.img,
# and forth.img is what the size table and the tests use, because that is
# what the Makefile calls the finished system.
SOD=$O/sod32
rm -rf "$SOD"; mkdir -p "$SOD"
cp vendor/sod32/* "$SOD"/
( cd "$SOD" && make sod32 >/dev/null 2>&1 ) || { echo "sod32 build failed"; exit 1; }
( cd "$SOD" && printf 'S" extend.4th" INCLUDED \n' | ./sod32 kernel.img >/dev/null 2>&1 )
[ -s "$SOD/forth.img" ] || { echo "sod32 forth.img not produced"; exit 1; }
echo "built  sod32 (forth.img $(stat -c%s "$SOD/forth.img") bytes)"

# ---- stage 0: the cell engine ----------------------------------------
# This is also the bootstrap host: every other stage's image is derived
# from a dictionary dump taken by running this one.
cc -O2 -Wall -o "$O/s0-cell-64" engine/relf.c
cc -m32 -O2 -Wall -o "$O/s0-cell-32" engine/relf.c
echo "built  s0-cell-64 s0-cell-32"

# ---- dictionary dumps -------------------------------------------------
# Three flavours, because the translator needs to know exactly which
# words are in the image it is laying out:
#   d*   full shell image      - what tests/shell and the size table use
#   k*   bare kernel           - boots into the Forth interpreter
#   *self  same, plus cv8.4    - the self-hosting compiler overlay
dump() { # dump OUTFILE ENGINE IMAGE BOOTSCRIPT
    ( cd "$W" && printf "$4" | "$1" "$2" ) | tr -d '\r' > "$O/$3"
}
SHELL_BOOT='S" pool.4" INCLUDED\nS" locals.4" INCLUDED\nS" save-system.4" INCLUDED\nS" shell.4" INCLUDED\nS" dict-dump-addr.4" INCLUDED\nBYE\n'
SELF_BOOT='S" cv8.4" INCLUDED\nS" pool.4" INCLUDED\nS" locals.4" INCLUDED\nS" save-system.4" INCLUDED\nS" shell.4" INCLUDED\nS" cv8-save.4" INCLUDED\nS" dict-dump-addr.4" INCLUDED\nBYE\n'
KERN_BOOT='S" dict-dump-addr.4" INCLUDED\nBYE\n'
KSELF_BOOT='S" cv8.4" INCLUDED\nS" dict-dump-addr.4" INCLUDED\nBYE\n'
KCPT_BOOT='S" cpt16.4" INCLUDED\nS" dict-dump-addr.4" INCLUDED\nBYE\n'
KS16_BOOT='S" sod16.4" INCLUDED\nS" dict-dump-addr.4" INCLUDED\nBYE\n'

dump "$O/s0-cell-64" kernel.img   d64.txt      "$SHELL_BOOT"
dump "$O/s0-cell-32" kernel32.img d32.txt      "$SHELL_BOOT"
dump "$O/s0-cell-64" kernel.img   d64-self.txt "$SELF_BOOT"
dump "$O/s0-cell-32" kernel32.img d32-self.txt "$SELF_BOOT"
dump "$O/s0-cell-64" kernel.img   k64.txt      "$KERN_BOOT"
dump "$O/s0-cell-32" kernel32.img k32.txt      "$KERN_BOOT"
dump "$O/s0-cell-64" kernel.img   k64-self.txt "$KSELF_BOOT"
dump "$O/s0-cell-32" kernel32.img k32-self.txt "$KSELF_BOOT"
dump "$O/s0-cell-64" kernel.img   k64-cpt.txt  "$KCPT_BOOT"
dump "$O/s0-cell-32" kernel32.img k32-cpt.txt  "$KCPT_BOOT"
dump "$O/s0-cell-64" kernel.img   k64-s16.txt  "$KS16_BOOT"
dump "$O/s0-cell-32" kernel32.img k32-s16.txt  "$KS16_BOOT"
echo "built  dictionary dumps"

# ---- engines ----------------------------------------------------------
# vm-lab.c is one source with the whole ladder behind -D flags. That is
# deliberate and is part of the article's argument: the difference
# between these VMs is small enough to live in one file.
#   ENC=1 SOD16 (word table)   ENC=2 CPT16 (computed target)   ENC=3 CV8
#   REG=1 VM registers in locals        FOLD=1 folded prim+EXIT
#   SCALE=S call scale shift            SKIPPAD=1 loader drops NOOPs
#   SPEC=1 specialised opcodes          SHAREDCALL=1 shared call path
cp engine/vm-lab.c "$O/"
python3 tools/gen-tos.py "$O/vm-lab.c" > "$O/vm-lab-tos.c"

cc      -O2 -Wall -o "$O/p8-pack8-64" engine/pack8.c
cc -m32 -O2 -Wall -o "$O/p8-pack8-32" engine/pack8.c
cc      -O2 -DENC=1 -DREG=1 -DSKIPPAD=1 -DSCALE=1 -o "$O/s1-sod16-64" "$O/vm-lab.c"
cc -m32 -O2 -DENC=1 -DREG=1 -DSKIPPAD=1 -DSCALE=1 -o "$O/s1-sod16-32" "$O/vm-lab.c"
cc      -O2 -DENC=2 -DREG=1 -DSCALE=1 -o "$O/s2-cpt16-64" "$O/vm-lab.c"
cc -m32 -O2 -DENC=2 -DREG=1 -DSCALE=1 -o "$O/s2-cpt16-32" "$O/vm-lab.c"

python3 tools/gen-fold.py "$O/vm-lab.c" "$HOT" > /dev/null
cc      -O2 -DENC=2 -DREG=1 -DFOLD=1 -DSCALE=3 -o "$O/s3-cpt16f-64" "$O/vm-lab.c"
cc -m32 -O2 -DENC=2 -DREG=1 -DFOLD=1 -DSCALE=2 -o "$O/s3-cpt16f-32" "$O/vm-lab.c"

python3 tools/gen-fold.py "$O/vm-lab.c" "$HOT" v8 > /dev/null
cc      -O2 -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=3 -DVARCALL=0 -DVARSLOT=0 -o "$O/s4-cv8-64" "$O/vm-lab.c"
cc -m32 -O2 -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=2 -DVARCALL=0 -DVARSLOT=0 -o "$O/s4-cv8-32" "$O/vm-lab.c"

python3 tools/gen-fold.py "$O/vm-lab-tos.c" "$HOT" v8 > /dev/null
cc      -O2 -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=3 -DSPEC=1 -DSHAREDCALL=1 \
        -o "$O/s5-cv8spec-64" "$O/vm-lab-tos.c"
cc -m32 -O2 -fno-pie -no-pie -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=2 -DSPEC=1 -DSHAREDCALL=1 \
        -o "$O/s5-cv8spec-32" "$O/vm-lab-tos.c"
echo "built  stage engines"

# ---- images -----------------------------------------------------------
img() { # img NAME CELL DUMP OPTIONS...
    local n=$1 c=$2 d=$3; shift 3
    # run from the flat work dir: sod16.py reads kernel.4 from the CWD
    ( cd "$W" && python3 "$ROOT/tools/layout.py" "$O/$d" "$c" "$@" \
        --emit-image "$O/$n.img" ) > "$O/$n.log" 2>&1 \
        || { echo "layout failed: $n"; tail -5 "$O/$n.log"; exit 1; }
}
CPTF="--dataprims --fold --fold-set $HOT"

# shell images - what the size table and the shell suites use
img s1-sod16-64   8 d64.txt --skip-pad
img s1-sod16-32   4 d32.txt --skip-pad
img s2-cpt16-64   8 d64.txt --cpt 1 --skip-pad
img s2-cpt16-32   4 d32.txt --cpt 1 --skip-pad
img s3-cpt16f-64  8 d64.txt --cpt 3 $CPTF
img s3-cpt16f-32  4 d32.txt --cpt 2 $CPTF
img s4-cv8-64     8 d64.txt --v8 --cpt 3 $CPTF --no-varcall --no-varslot
img s4-cv8-32     4 d32.txt --v8 --cpt 2 $CPTF --no-varcall --no-varslot
img s5-cv8spec-64 8 d64-self.txt --v8 --cpt 3 $CPTF --spec $SPECS --cv8-compiler
img s5-cv8spec-32 4 d32-self.txt --v8 --cpt 2 $CPTF --spec $SPECS --cv8-compiler

# ---- kernel-only images ----------------------------------------------
# These boot into the Forth INTERPRETER, which is what the CORE suite
# and the kernel-compile benchmark need. TWO are built per stage, and
# the distinction matters for every number in the article:
#
#   -k*   RUN-ONLY. Translated from the plain kernel dump, no compiler
#         overlay. The word set is identical at every stage, so the size
#         difference between two rows is the ENCODING and nothing else.
#         It cannot compile, so it cannot run the corpus.
#   -s*   SELF-HOSTING. Carries the stage's own emitter overlay, so it
#         compiles its own encoding. This is the image that gets tested
#         and benchmarked, and the one that answers "how small is a
#         Forth that can still rebuild itself".
#
# s0-cell needs no overlay - its compiler already emits cells - so its
# two images are the same file, and the gap between the columns at every
# other row is exactly what that stage pays to carry its own compiler.
cp "$W/kernel.img"   "$O/s0-cell-k64.img"
cp "$W/kernel32.img" "$O/s0-cell-k32.img"
img s1-sod16-k64   8 k64.txt --skip-pad
img s1-sod16-k32   4 k32.txt --skip-pad
img s2-cpt16-k64   8 k64.txt --cpt 1 --skip-pad
img s2-cpt16-k32   4 k32.txt --cpt 1 --skip-pad
img s3-cpt16f-k64  8 k64.txt --cpt 3 $CPTF
img s3-cpt16f-k32  4 k32.txt --cpt 2 $CPTF
img s4-cv8-k64     8 k64.txt --v8 --cpt 3 $CPTF --no-varcall --no-varslot
img s4-cv8-k32     4 k32.txt --v8 --cpt 2 $CPTF --no-varcall --no-varslot
img s5-cv8spec-k64 8 k64.txt --v8 --cpt 3 $CPTF --spec $SPECS
img s5-cv8spec-k32 4 k32.txt --v8 --cpt 2 $CPTF --spec $SPECS

# Run from the flat work dir, like the translator: sod16.py reads
# kernel.4 from the CWD.
( cd "$W" && python3 "$ROOT/tools/pack8.py" "$O/k64.txt" 8 kernel.img \
    "$O/p8-pack8-k64.img" ) > "$O/p8-pack8-k64.log"
( cd "$W" && python3 "$ROOT/tools/pack8.py" "$O/k32.txt" 4 kernel32.img \
    "$O/p8-pack8-k32.img" ) > "$O/p8-pack8-k32.log"
cp "$O/p8-pack8-k64.img" "$O/p8-pack8-s64.img"
cp "$O/p8-pack8-k32.img" "$O/p8-pack8-s32.img"

cp "$O/s0-cell-k64.img" "$O/s0-cell-s64.img"
cp "$O/s0-cell-k32.img" "$O/s0-cell-s32.img"
img s1-sod16-s64   8 k64-s16.txt --skip-pad --compiler-overlay 16
img s1-sod16-s32   4 k32-s16.txt --skip-pad --compiler-overlay 16
img s2-cpt16-s64   8 k64-cpt.txt --cpt 1 --skip-pad --compiler-overlay 16
img s2-cpt16-s32   4 k32-cpt.txt --cpt 1 --skip-pad --compiler-overlay 16
img s3-cpt16f-s64  8 k64-cpt.txt --cpt 3 $CPTF --compiler-overlay 16
img s3-cpt16f-s32  4 k32-cpt.txt --cpt 2 $CPTF --compiler-overlay 16
# s4 uses cv8.4 too. Its engine is built with VARCALL=0, so it reads
# every call as the fixed 2-byte form; cv8.4 emits the 3-byte form only
# past 16384 scaled units, which a kernel image never reaches. The build
# checks this rather than trusting it - see the far-call assertion in
# the log.
img s4-cv8-s64     8 k64-self.txt --v8 --cpt 3 $CPTF --no-varcall --no-varslot --cv8-compiler
img s4-cv8-s32     4 k32-self.txt --v8 --cpt 2 $CPTF --no-varcall --no-varslot --cv8-compiler
img s5-cv8spec-s64 8 k64-self.txt --v8 --cpt 3 $CPTF --spec $SPECS --cv8-compiler
img s5-cv8spec-s32 4 k32-self.txt --v8 --cpt 2 $CPTF --spec $SPECS --cv8-compiler
echo "built  stage images"

# ---- stage 0 shell image ---------------------------------------------
# The cell stage needs a saved shell image too, or the size table would
# be comparing a translated shell image against a bare kernel. SAVE-SYSTEM
# writes the running system out; SET-BOOT makes it boot into MAIN.
cellshell() { # cellshell ENGINE SEEDIMG OUTNAME
    ( cd "$W" && printf 'S" pool.4" INCLUDED\nS" locals.4" INCLUDED\nS" save-system.4" INCLUDED\nS" shell.4" INCLUDED\n'"'"' MAIN SET-BOOT\nS" %s" SAVE-SYSTEM\nBYE\n' "$3" \
        | "$1" "$2" >/dev/null 2>&1 )
    [ -s "$W/$3" ] || { echo "failed to save $3"; exit 1; }
    cp "$W/$3" "$O/$3"
}
cellshell "$O/s0-cell-64" kernel.img   s0-cell-64.img
cellshell "$O/s0-cell-32" kernel32.img s0-cell-32.img
# and the kernel-only cell images, for the compile benchmark
echo "built  stage 0 images"

# ---- size table -------------------------------------------------------
# The unit of comparison is the FORTH IMAGE - the smallest image that
# boots into the interpreter and can recompile the system - not the shell
# image. That follows SOD32's own Makefile, where `forth.img` (kernel +
# extend) is the finished artefact. A shell image would measure shell.4,
# which is application code and has nothing to do with the encoding.
{
  echo "stage,runonly_64,runonly_32,selfhost_64,selfhost_32"
  printf 'sod32,NA,NA,NA,%s\n' "$(stat -c%s "$SOD/forth.img")"
  for st in s0-cell p8-pack8 s1-sod16 s2-cpt16 s3-cpt16f s4-cv8 s5-cv8spec; do
      sz() { [ -r "$1" ] && stat -c%s "$1" || echo NA; }
      printf '%s,%s,%s,%s,%s\n' "$st" \
          "$(sz "$O/$st-k64.img")" "$(sz "$O/$st-k32.img")" \
          "$(sz "$O/$st-s64.img")" "$(sz "$O/$st-s32.img")"
  done
} > "$O/sizes.csv"
# The shell images are still built and still measured, but in a separate
# file, so the two questions never get mixed up in one table.
{
  echo "stage,shell_bytes_64,shell_bytes_32"
  for s in s0-cell s1-sod16 s2-cpt16 s3-cpt16f s4-cv8 s5-cv8spec; do
      printf '%s,%s,%s\n' "$s" "$(stat -c%s "$O/$s-64.img")" "$(stat -c%s "$O/$s-32.img")"
  done
} > "$O/sizes-shell.csv"
awk -F, '{printf "%-12s %10s %10s %10s %10s\n", $1,$2,$3,$4,$5}' "$O/sizes.csv"
echo
echo "build complete: $O"

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

# Every engine this script runs is a measured subject, so it runs in a
# predictable environment rather than in whatever the caller happens to
# have exported.
#
# LD_PRELOAD is the one that actually bites. A desktop session that
# preloads a library into everything will have it loaded into every
# engine here too, which is unwanted work inside the thing being timed;
# and when the engine is a 32-bit binary and the library is 64-bit,
# ld.so cannot load it and writes a line of complaint per process. That
# was reported from a real machine: six copies of "object
# 'libgtk3-nocsd.so.0' from LD_PRELOAD cannot be preloaded" during the
# dictionary dumps. Harmless there, because a dump captures stdout and
# ld.so writes to stderr - but not something to leave in a benchmark.
unset LD_PRELOAD

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

# ---- preflight --------------------------------------------------------
# Check the toolchain before building anything, because the failure
# otherwise surfaces as a missing header three files deep and looks like
# a bug in this repository rather than a missing package.
command -v cc >/dev/null      || { echo "no C compiler on PATH"; exit 1; }
command -v python3 >/dev/null || { echo "python3 is required"; exit 1; }

# Every stage is built at both cell widths. Which compiler produces
# which width is NOT a constant, and assuming it was is how this script
# failed on a 32-bit ARM box: relf.c picks its cell width from the
# host's own UINTPTR_MAX, so on armv7l the NATIVE compiler gives 4-byte
# cells and `-m32` means nothing. The script built a 4-byte engine,
# called it the 8-byte one, and handed it the 8-byte seed image, which
# refused to load.
#
# So ask the compiler what it actually produces, rather than telling it.
_t=$(mktemp -d) || { echo "cannot create a temporary directory"; exit 1; }
trap 'rm -rf "$_t"' EXIT INT TERM
printf '#include <stdio.h>\nint main(void){printf("%%d\\n",(int)sizeof(void*));return 0;}\n' \
    > "$_t/w.c"
cc -o "$_t/w" "$_t/w.c" >/dev/null 2>&1 || { echo "the C compiler cannot build a program"; exit 1; }
NATIVE=$("$_t/w") || { echo "cannot run a freshly built program"; exit 1; }

BUILD64=0; BUILD32=0
CC64=""; CC32=""
case "$NATIVE" in
  8)  BUILD64=1; CC64="cc"
      # 4-byte cells need a compiler that can target a 32-bit ABI AND a
      # 32-bit libc to link against. On a 64-bit distribution that is a
      # separate package and is usually absent.
      printf 'int main(void){return 0;}\n' > "$_t/t.c"
      if cc -m32 -o "$_t/t" "$_t/t.c" >/dev/null 2>&1; then
          BUILD32=1; CC32="cc -m32"
      fi ;;
  4)  # A 32-bit host. Native IS the 4-byte build; there is no practical
      # way to get 8-byte cells here, and nothing needs one.
      BUILD32=1; CC32="cc" ;;
  *)  echo "unsupported pointer width: $NATIVE bytes"; exit 1 ;;
esac

_w=""
[ "$BUILD64" = 1 ] && _w="8-byte"
[ "$BUILD32" = 1 ] && _w="${_w:+$_w and }4-byte"
echo "host pointer width $NATIVE bytes; building $_w cells"
if [ "$BUILD64" = 1 ] && [ "$BUILD32" = 0 ]; then
    cat >&2 <<'WARN'
-------------------------------------------------------------------
 4-byte cells DISABLED: this compiler cannot link a 32-bit binary.
 Building 8-byte cells only; every 4-byte figure will be reported
 as "not built" rather than silently omitted.

   Debian / Ubuntu   sudo apt install gcc-multilib
   Fedora / RHEL     sudo dnf install glibc-devel.i686 libgcc.i686
   Arch              sudo pacman -S lib32-glibc lib32-gcc-libs
   openSUSE          sudo zypper install glibc-devel-32bit
-------------------------------------------------------------------
WARN
fi
if [ "$BUILD32" = 1 ] && [ "$BUILD64" = 0 ]; then
    cat >&2 <<'WARN'
-------------------------------------------------------------------
 8-byte cells DISABLED: this is a 32-bit host, so the native build
 IS the 4-byte one. Every 8-byte figure will be reported as "not
 built". Nothing is wrong; the 8-byte column simply does not exist
 on this machine.
-------------------------------------------------------------------
WARN
fi

# A compile at a given cell width, or nothing at all. Both return
# success either way so `set -e` does not abort a single-width build.
# LAYOUTS: how many differently-laid-out builds of each engine to make.
#
# WHY. The numbers these engines produce carry a per-BUILD bias, not just
# run-to-run noise. Three consecutive runs of the same binaries agree to
# about 1%, but rebuild the tree and a stage can move by five or ten -
# tools/layout-noise.sh measures 2.5% to 17% between five builds that
# differ only in flags that move code around. Taking the minimum over
# repetitions does nothing about that: the bias is fixed for a given
# binary, so more repetitions measure it more precisely.
#
# The fix is to make it a distribution instead of a constant: build each
# engine several ways, time all of them, and report the median. This is
# the same reasoning as Mytkowicz et al., "Producing Wrong Data Without
# Doing Anything Obviously Wrong!" (ASPLOS 2009), and Stabilizer.
#
# LAYOUTS=1 (the default) keeps the old single-build behaviour, which is
# what the correctness gates and a quick check want.
LAYOUTS=${LAYOUTS:-1}
LAYOUT_FLAGS_0=""
LAYOUT_FLAGS_1="-falign-functions=32 -falign-loops=32"
LAYOUT_FLAGS_2="-falign-functions=64 -falign-jumps=32"
LAYOUT_FLAGS_3="-fno-align-jumps -falign-labels=16"
LAYOUT_FLAGS_4="-falign-functions=16 -falign-loops=64"
LV=0                  # which variant is being built right now
LVSUF=""              # "" for variant 0, "-v1".. for the rest

cc64() { [ "$BUILD64" = 1 ] || return 0; $CC64 $LF "$@"; }
cc32() { [ "$BUILD32" = 1 ] || return 0; $CC32 $LF "$@"; }

# ---- flat work directory ---------------------------------------------
ln -sf "$ROOT"/forth/*.4        "$W"/ 2>/dev/null || true
ln -sf "$ROOT"/tools/*.4        "$W"/ 2>/dev/null || true
ln -sf "$ROOT"/tests/core/*.fr  "$W"/ 2>/dev/null || true
ln -sf "$ROOT"/tests/core/*.fth "$W"/ 2>/dev/null || true
cp -f "$ROOT/forth/kernel-seed.img"   "$W/kernel.img"
cp -f "$ROOT/forth/kernel32-seed.img" "$W/kernel32.img"

# ---- clear what a previous run built ---------------------------------
# This script is not idempotent across a change of configuration, and
# pretending otherwise cost a debugging session. A build on a machine
# where the 8-byte column exists leaves engines and images behind; run
# it again somewhere the 8-byte column does NOT exist - or after
# installing multilib, or after a git pull that changes what is built -
# and those files are still sitting in the output directory. The script
# then skips building them, finds them anyway, and runs them. On a
# 32-bit ARM host that produced six copies of "cannot execute binary
# file: Exec format error" from a binary this run never created.
#
# Only what this script generates is removed. build/results/ and
# build/work/ are left alone: the first is measurement output that takes
# minutes to reproduce, the second is rebuilt below in place.
rm -f "$O"/s[0-9]-* "$O"/p[48]-* "$O"/*.img "$O"/*.txt "$O"/*.log \
      "$O"/sizes*.csv "$O"/vm-lab*.c "$O"/pack4-alphabet.h \
      "$O"/vm-fold-*.h 2>/dev/null || true

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
# The baseline needs layout variants as much as any other stage - every
# ratio in the tables is divided by it, so a single biased build would
# tilt the whole column.
for LV in $(seq 0 $((LAYOUTS - 1))); do
  eval "LF=\$LAYOUT_FLAGS_$LV"
  [ "$LV" = 0 ] && LVSUF="" || LVSUF="-v$LV"
  cc64 -O2 -Wall -o "$O/s0-cell-64$LVSUF" engine/relf.c
  cc32 -O2 -Wall -o "$O/s0-cell-32$LVSUF" engine/relf.c
done
LF=""; LVSUF=""
_b=""
[ "$BUILD64" = 1 ] && _b="s0-cell-64"
[ "$BUILD32" = 1 ] && _b="${_b:+$_b }s0-cell-32"
echo "built  $_b"

# ---- dictionary dumps -------------------------------------------------
# Three flavours, because the translator needs to know exactly which
# words are in the image it is laying out:
#   d*   full shell image      - what tests/shell and the size table use
#   k*   bare kernel           - boots into the Forth interpreter
#   *self  same, plus cv8.4    - the self-hosting compiler overlay
runnable() { # runnable ENGINE - exists, and this host can execute it
    [ -x "$1" ] || return 1
    "$1" /dev/null >/dev/null 2>&1
    [ $? -ne 126 ] || return 1
    return 0
}

dump() { # dump ENGINE IMAGE OUTFILE BOOTSCRIPT
    # Silently skipped when the engine was not built - that is how a
    # cell width that does not exist on this host disappears cleanly.
    runnable "$1" || return 0
    ( cd "$W" && printf "$4" | "$1" "$2" ) | tr -d '\r' > "$O/$3"
}
SHELL_BOOT='S" pool.4" INCLUDED\nS" locals.4" INCLUDED\nS" save-system.4" INCLUDED\nS" shell.4" INCLUDED\nS" dict-dump-addr.4" INCLUDED\nBYE\n'
SELF_BOOT='S" cv8.4" INCLUDED\nS" pool.4" INCLUDED\nS" locals.4" INCLUDED\nS" save-system.4" INCLUDED\nS" shell.4" INCLUDED\nS" cv8-save.4" INCLUDED\nS" dict-dump-addr.4" INCLUDED\nBYE\n'
KERN_BOOT='S" dict-dump-addr.4" INCLUDED\nBYE\n'
KSELF_BOOT='S" cv8.4" INCLUDED\nS" dict-dump-addr.4" INCLUDED\nBYE\n'
KCPT_BOOT='S" cpt16.4" INCLUDED\nS" dict-dump-addr.4" INCLUDED\nBYE\n'
KS16_BOOT='S" sod16.4" INCLUDED\nS" dict-dump-addr.4" INCLUDED\nBYE\n'
KCV8B_BOOT='S" cv8.4" INCLUDED\nS" cv8b.4" INCLUDED\nS" dict-dump-addr.4" INCLUDED\nBYE\n'

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
dump "$O/s0-cell-64" kernel.img   k64-b.txt    "$KCV8B_BOOT"
dump "$O/s0-cell-32" kernel32.img k32-b.txt    "$KCV8B_BOOT"
echo "built  dictionary dumps"

# The timing helper. Reports a child's CPU time, which excludes the time
# a process spends descheduled - the dominant noise term on a loaded
# machine. Built with the plain compiler, not cc64/cc32: it is a tool,
# not a measured subject.
cc -O2 -Wall -o "$O/cputime" tools/cputime.c 2>/dev/null || \
    echo "note: cputime helper did not build; harnesses will use wall clock"

# ---- engines ----------------------------------------------------------
for LV in $(seq 0 $((LAYOUTS - 1))); do
  eval "LF=\$LAYOUT_FLAGS_$LV"
  [ "$LV" = 0 ] && LVSUF="" || LVSUF="-v$LV"
  # vm-lab.c is one source with the whole ladder behind -D flags. That is
  # deliberate and is part of the article's argument: the difference
  # between these VMs is small enough to live in one file.
  #   ENC=1 SOD16 (word table)   ENC=2 CPT16 (computed target)   ENC=3 CV8
  #   REG=1 VM registers in locals        FOLD=1 folded prim+EXIT
  #   SCALE=S call scale shift            SKIPPAD=1 loader drops NOOPs
  #   SPEC=1 specialised opcodes          SHAREDCALL=1 shared call path
  cp engine/vm-lab.c "$O/"
  python3 tools/gen-tos.py "$O/vm-lab.c" > "$O/vm-lab-tos.c"

  # PACK4's alphabet is derived from the image, and the engine needs it at
  # compile time, so the packer runs BEFORE the engine is built and emits
  # both the image and pack4-alphabet.h. The 64-bit run writes the header;
  # the 32-bit run reads it back, so one alphabet serves both widths.
  rm -f "$O/pack4-alphabet.h"
  [ "$BUILD64" = 1 ] && ( cd "$W" && python3 "$ROOT/tools/pack4.py" "$O/k64.txt" 8 kernel.img \
      "$O/p4-pack4-k64.img" "$O/pack4-alphabet.h" ) > "$O/p4-pack4-k64.log"
  if [ "$BUILD32" = 1 ]; then
  ( cd "$W" && python3 "$ROOT/tools/pack4.py" "$O/k32.txt" 4 kernel32.img \
      "$O/p4-pack4-k32.img" "$O/pack4-alphabet.h" ) > "$O/p4-pack4-k32.log"
    cp "$O/p4-pack4-k32.img" "$O/p4-pack4-s32.img"
  fi
  [ "$BUILD64" = 1 ] && cp "$O/p4-pack4-k64.img" "$O/p4-pack4-s64.img"
  cc64    -O2 -Wall -I"$O" -o "$O/p4-pack4-64$LVSUF" engine/pack4.c
  cc32 -O2 -Wall -I"$O" -o "$O/p4-pack4-32$LVSUF" engine/pack4.c
  cc64    -O2 -Wall -o "$O/p8-pack8-64$LVSUF" engine/pack8.c
  cc32 -O2 -Wall -o "$O/p8-pack8-32$LVSUF" engine/pack8.c
  cc64    -O2 -DENC=1 -DREG=1 -DSKIPPAD=1 -DSCALE=1 -o "$O/s1-sod16-64$LVSUF" "$O/vm-lab.c"
  cc32 -O2 -DENC=1 -DREG=1 -DSKIPPAD=1 -DSCALE=1 -o "$O/s1-sod16-32$LVSUF" "$O/vm-lab.c"
  cc64    -O2 -DENC=2 -DREG=1 -DSCALE=1 -o "$O/s2-cpt16-64$LVSUF" "$O/vm-lab.c"
  cc32 -O2 -DENC=2 -DREG=1 -DSCALE=1 -o "$O/s2-cpt16-32$LVSUF" "$O/vm-lab.c"

  python3 tools/gen-fold.py "$O/vm-lab.c" "$HOT" > /dev/null
  cc64    -O2 -DENC=2 -DREG=1 -DFOLD=1 -DSCALE=3 -o "$O/s3-cpt16f-64$LVSUF" "$O/vm-lab.c"
  cc32 -O2 -DENC=2 -DREG=1 -DFOLD=1 -DSCALE=2 -o "$O/s3-cpt16f-32$LVSUF" "$O/vm-lab.c"

  python3 tools/gen-fold.py "$O/vm-lab.c" "$HOT" v8 > /dev/null
  cc64    -O2 -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=3 -DVARCALL=0 -DVARSLOT=0 -o "$O/s4-cv8-64$LVSUF" "$O/vm-lab.c"
  cc32 -O2 -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=2 -DVARCALL=0 -DVARSLOT=0 -o "$O/s4-cv8-32$LVSUF" "$O/vm-lab.c"

  python3 tools/gen-fold.py "$O/vm-lab-tos.c" "$HOT" v8 > /dev/null
  cc64    -O2 -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=3 -DSPEC=1 -DSHAREDCALL=1 \
          -o "$O/s5-cv8spec-64$LVSUF" "$O/vm-lab-tos.c"
  cc32 -O2 -fno-pie -no-pie -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=2 -DSPEC=1 -DSHAREDCALL=1 \
          -o "$O/s5-cv8spec-32$LVSUF" "$O/vm-lab-tos.c"
  # s6: s5 with byte-aligned call targets (SCALE=0). The engine never reads
  # a dictionary link, so the byte-granular header is invisible to it; the
  # scale is the only difference in the binary.
  cc64    -O2 -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=0 -DSPEC=1 -DSHAREDCALL=1 -DDOESFAR=1 \
          -o "$O/s6-cv8b-64$LVSUF" "$O/vm-lab-tos.c"
  cc32 -O2 -fno-pie -no-pie -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=0 -DSPEC=1 -DSHAREDCALL=1 -DDOESFAR=1 \
          -o "$O/s6-cv8b-32$LVSUF" "$O/vm-lab-tos.c"

done
LF=""; LVSUF=""
echo "built  stage engines ($LAYOUTS layout(s) each)"

# ---- images -----------------------------------------------------------
echo "translating images (pure Python; minutes on a slow machine) ..."
img() { # img NAME CELL DUMP OPTIONS...
    local n=$1 c=$2 d=$3; shift 3
    [ "$c" = 4 ] && [ "$BUILD32" = 0 ] && return 0
    [ "$c" = 8 ] && [ "$BUILD64" = 0 ] && return 0
    [ -r "$O/$d" ] || return 0
    # One line per image. layout.py is pure Python and translates every
    # word body in the dictionary; on a fast x86 box the whole set takes
    # a few seconds, on an ARMv7 board it is minutes. Without this the
    # script sits silent for long enough to look hung, and gets killed.
    printf '  %-18s ' "$n"
    # run from the flat work dir: sod16.py reads kernel.4 from the CWD
    ( cd "$W" && python3 "$ROOT/tools/layout.py" "$O/$d" "$c" "$@" \
        --emit-image "$O/$n.img" ) > "$O/$n.log" 2>&1 \
        || { echo "FAILED"; tail -5 "$O/$n.log"; exit 1; }
    printf '%s bytes\n' "$(stat -c%s "$O/$n.img")"
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
[ "$BUILD64" = 1 ] && cp "$W/kernel.img"   "$O/s0-cell-k64.img"
[ "$BUILD32" = 1 ] && cp "$W/kernel32.img" "$O/s0-cell-k32.img"
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
# s6 run-only: the same word set laid out with byte headers, for the size
# column ONLY. It does not boot: the kernel's own SEARCH-WORDLIST assumes
# a cell link and an aligned name, and only the cv8b.4 overlay replaces
# it. The self-hosting image below is the one that runs.
img s6-cv8b-k64    8 k64.txt --v8 --cpt 0 --bytehdr $CPTF --spec $SPECS
img s6-cv8b-k32    4 k32.txt --v8 --cpt 0 --bytehdr $CPTF --spec $SPECS

# Run from the flat work dir, like the translator: sod16.py reads
# kernel.4 from the CWD.
[ "$BUILD64" = 1 ] && ( cd "$W" && python3 "$ROOT/tools/pack8.py" "$O/k64.txt" 8 kernel.img \
    "$O/p8-pack8-k64.img" ) > "$O/p8-pack8-k64.log"
if [ "$BUILD32" = 1 ]; then
( cd "$W" && python3 "$ROOT/tools/pack8.py" "$O/k32.txt" 4 kernel32.img \
    "$O/p8-pack8-k32.img" ) > "$O/p8-pack8-k32.log"
fi
[ "$BUILD64" = 1 ] && cp "$O/p8-pack8-k64.img" "$O/p8-pack8-s64.img"
[ "$BUILD32" = 1 ] && cp "$O/p8-pack8-k32.img" "$O/p8-pack8-s32.img"

[ "$BUILD64" = 1 ] && cp "$O/s0-cell-k64.img" "$O/s0-cell-s64.img"
[ "$BUILD32" = 1 ] && cp "$O/s0-cell-k32.img" "$O/s0-cell-s32.img"
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
img s6-cv8b-s64    8 k64-b.txt --v8 --cpt 0 --bytehdr $CPTF --spec $SPECS --cv8-compiler
img s6-cv8b-s32    4 k32-b.txt --v8 --cpt 0 --bytehdr $CPTF --spec $SPECS --cv8-compiler
echo "built  stage images"

# ---- stage 0 shell image ---------------------------------------------
# The cell stage needs a saved shell image too, or the size table would
# be comparing a translated shell image against a bare kernel. SAVE-SYSTEM
# writes the running system out; SET-BOOT makes it boot into MAIN.
cellshell() { # cellshell ENGINE SEEDIMG OUTNAME
    runnable "$1" || return 0
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
  for st in s0-cell p4-pack4 p8-pack8 s1-sod16 s2-cpt16 s3-cpt16f s4-cv8 s5-cv8spec s6-cv8b; do
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
      printf '%s,%s,%s\n' "$s" "$(stat -c%s "$O/$s-64.img" 2>/dev/null || echo NA)" "$(stat -c%s "$O/$s-32.img" 2>/dev/null || echo NA)"
  done
} > "$O/sizes-shell.csv"
awk -F, '{printf "%-12s %10s %10s %10s %10s\n", $1,$2,$3,$4,$5}' "$O/sizes.csv"
echo
if [ "$BUILD32" = 0 ]; then
    echo "build complete (8-byte cells only): $O"
elif [ "$BUILD64" = 0 ]; then
    echo "build complete (4-byte cells only - 32-bit host): $O"
else
    echo "build complete: $O"
fi

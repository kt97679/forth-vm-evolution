#!/bin/sh
# results/drafts/doesfar-pp-593.sh TREE [OLD [NEW]] - doesfar's retirement checked at the preprocessor (Iteration 593):
# the engines at OLD (default HEAD~1) built with -DDOESFAR=1 and at NEW (default HEAD) without it, preprocessed (gcc -E -P)
# and compared - vm-lab.c at ENC 1, 2 and 3 (tag 2, the JIT), its TOS form (gen-tos.py of each revision) at ENC 3, and
# spn-cv8.c, each at 8- and 4-byte cells: 22 settings, every one the same text, so every engine the same code. As the build user.
set -u; T=${1:?TREE}; OLD=${2:-HEAD~1}; NEW=${3:-HEAD}; P=$(mktemp -d); trap 'rm -rf "$P"' EXIT; cd "$T"
for r in old new; do v=$OLD; [ $r = new ] && v=$NEW
  git show $v:engine/vm-lab.c > $P/$r-vm.c; git show $v:engine/spn-cv8.c > $P/$r-spn.c; git show $v:tools/gen-tos.py > $P/$r-gen-tos.py
  python3 $P/$r-gen-tos.py $P/$r-vm.c > $P/$r-tos.c; done
E3="-DENC=3 -DREG=1 -DFOLD=1 -DSCALE=0 -DSPEC=1"; n=0; bad=0
cmp1() { # SRC FLAGS
  for w in "" "-m32"; do n=$((n+1))
    gcc -E -P -I engine $w $2 -DDOESFAR=1 $P/old-$1.c > $P/a.i 2>/dev/null; gcc -E -P -I engine $w $2 $P/new-$1.c > $P/b.i 2>/dev/null
    if [ ! -s $P/b.i ] || ! cmp -s $P/a.i $P/b.i; then bad=$((bad+1)); echo "DIFFER $1 $w $2"; fi; done; }
for fl in "$E3" "$E3 -DTAG2=1" "$E3 -DTAG2=1 -DX_JIT=1 -DFSYS=2" "$E3 -DCELL32=1"; do cmp1 vm "$fl"; cmp1 tos "$fl"; done
cmp1 vm "-DENC=1 -DREG=1 -DSKIPPAD=1 -DSCALE=1"; cmp1 vm "-DENC=2 -DREG=1 -DSCALE=3"
cmp1 spn "$E3 -DSPN_FUSED_BR=1 -DSPN_IO=1"
echo "doesfar-pp: $n settings preprocessed, $((n-bad)) the same"; [ $bad = 0 ]

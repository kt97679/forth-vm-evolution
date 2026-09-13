#!/bin/bash
# show-word.sh [WORD] [BUILDDIR] - the same Forth word, as bytes, in each
# encoding. This is where the diagram in the article comes from; it is a
# script so the diagram cannot drift from the images.
set -u
cd "$(dirname "$0")/.."
unset LD_PRELOAD
W=${1:-COUNT}
O=${2:-$PWD/build}; O=$(cd "$O" && pwd)
cat > "$O/.showword.fth" <<EOF
: DUMPB ( a n --- ) 0 DO DUP I + C@ . LOOP DROP CR ;
' $W 32 DUMPB
BYE
EOF
echo "word: $W   (4-byte cells)"
for pair in "s0-cell 28" "s1-sod16 14" "s2-cpt16 14" "s5-cv8spec 5"; do
    set -- $pair
    e=$O/$1-32; i=$O/$1-s32.img
    [ -x "$e" ] && [ -r "$i" ] || { printf '  %-12s not built\n' "$1"; continue; }
    printf '  %-12s %2s bytes: ' "$1" "$2"
    ( cd "$O/work" && timeout 10 "$e" "$i" < "$O/.showword.fth" 2>&1 ) \
        | tr -d '\r' | tr '\n' ' ' \
        | sed 's/Welcome to Forth//; s/OK//g' \
        | awk -v n="$2" '{for(i=1;i<=n;i++) printf "%s ", $i; print ""}'
done
echo
echo "A cell-image value is 1 + index*CELL: the low bit marks a primitive"
echo "rather than a call. A token is the index itself. In CV8, 120 is ADDI"
echo "- an add with an immediate operand, into which LIT 1 + collapses -"
echo "and 79 is the folded 'C@ then EXIT'."

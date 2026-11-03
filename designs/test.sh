#!/bin/sh
# designs/test.sh NAME... - each design's engine runs its image: a definition, a call, a number printed (make test).
cd "$(dirname "$0")" || exit 1
fail=0
for d in "$@"; do
    out=$(printf ': SQ DUP * ; 7 SQ . BYE\n' | ./"$d"/forth "$d"/image.img 2>&1)
    case $out in *49*) echo "$d: ok" ;; *) echo "$d: FAILED - $out"; fail=1 ;; esac
done
exit $fail

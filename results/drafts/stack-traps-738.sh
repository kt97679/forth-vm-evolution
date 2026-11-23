#!/bin/sh
# results/drafts/stack-traps-738.sh DIR [qemu-arm] - the stacks' traps on one built design (Iteration 738; the data
# layout's step 2 moved the stacks' chunk). DIR holds engine and image.img (an x86 role: data-layout-734.py's
# build/evolve/dlay-ROLE, run in its work/; an ARM build: with qemu-arm). A line a program: its status and stderr's
# last line. Run it on two trees' builds of the same design and diff the outputs - the guard gene (guard pages, "data
# stack underflow") and the designs without it (the fault trap, the interpreter's bounds) each have their own lines.
#   : DEEP RECURSE ;            return stack overflow (or, where the tail call makes it a jump, the 20 s timeout: 124)
#   : OVF BEGIN 1 0 UNTIL ;     data stack overflow (the JIT's code without the guard: 139 - results/drafts/data-layout2-738.txt)
#   : UND BEGIN DROP 0 UNTIL ;  a runaway underflow: the guard page, or the fault trap
#   : UNR BEGIN R> DROP 0 UNTIL ; the return stack's runaway underflow
#   20000 D2, 25 FIB            deep but bounded work: the overflow trap, then 75025 (run-engine-stacks' fib)
D=$1; Q=${2:-}
W=$D; [ -d "$D/work" ] && W=$D/work
for p in ': DEEP RECURSE ; DEEP' ': OVF BEGIN 1 0 UNTIL ; OVF' ': UND BEGIN DROP 0 UNTIL ; UND' \
         ': UNR BEGIN R> DROP 0 UNTIL ; UNR' ': D2 DUP IF 1- RECURSE THEN ; 20000 D2 . CR' \
         ': FIB DUP 2 < IF EXIT THEN DUP 1- RECURSE SWAP 2 - RECURSE + ; 25 FIB . CR'; do
    o=$(printf '%s\n' "$p" | (cd "$W" && timeout 60 $Q "$D/engine" "$D/image.img") 2>&1); s=$?
    printf '  %-34s status %3s  %s\n' "$p" "$s" "$(printf '%s' "$o" | tr -d '\r' | grep -v '^Welcome' | tail -n 2 | tr '\n' '|' | cut -c1-60)"
done

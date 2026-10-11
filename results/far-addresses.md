# Code far from the image base (Iterations 157-158)

The owner: small benchmarks on a small kernel use short addresses, and long
ones can cost. What this system encodes by distance, what the workloads reach,
and what happens past it.

## The thresholds

tag2 - the whole front: a call holds its target's byte offset from the image
base in 2, 3 or 4 bytes (below 16 KB, 4 MB, 1 GB; vm-lab.c reads one, two or
three more bytes - the same tail). Calls into the kernel stay short: it sits at
the bottom. Branches are relative within a word. cv8 (s4-s6): near 14 scaled
bits, far 21-22 (0xC0 prefix, decoded only by the shared-call engine); header
links 22 bits.

## What the workloads reach

bubble ends at 12.6 KB, ackermann at 9.8 KB (s6), sieve at 18 KB; the kernel
workload passes 16 KB - cross.4 allots its 40,000-byte target image before its
own code, so its calls are three bytes. Nothing reaches 4 MB: no workload and
no test used tag2's four-byte call.

## tests/core/far.fth

Code and data past 64 KB, then 8 MB more: calls, recursion, CREATE DOES> with
a far tail, far data, EXECUTE from a near word into far ones. Line k prints
k*100000 plus its answer (tools/farcheck.py): every answer right, any missing
one refused out loud.

**The front: all 165 of seed 38's designs and both founders right, every answer.**

**The ladder, before:** relf alone right. The rest crashed (s0, pack4, pack8,
s7 - before an answer), hung (s2, s3), hit an unknown opcode (s3, s4-32),
stopped silently (s5-32 at a DOES> word past its near form's reach - the hazard
cv8.4's own comment records), lost far words to a cut header link (s6, s8:
"Undefined word"), or refused cleanly (s1: "DOES> tail beyond 128 KB").

**Fixed - cv8 refuses instead of truncating:** CALL, past the far form's 21
bits, DOES>8 a tail out of its form's reach (refused with the defining word,
before a child exists to be left half made), cv8b's LINK-LEN past 4 MB. Now s1,
s5, s6 and the s8 stages refuse with "out of reach" where they broke.

**Still broken, listed in run-tests.sh (FAR_KNOWN) and shown on every run:**
- s4: its engine (vm-lab.c without shared calls) has no 0xC0 far form - a far
  call there is the FARCALL opcode - but cv8.4's CALL, cannot tell which engine
  it compiles for. Needs a flag the converter sets, as CV8-DOES-FAR? is.
- s0, pack4, pack8, s7: crash before an answer, output lost with the crash.
  pack4, pack8 and spn.c hold 1 MB (an 8 MB gap is past their memory; ALLOT
  checks nothing); s0's cause is not found yet.
- s2, s3: hang past 64 KB; not diagnosed.

## The gate

alive() runs far.fth on every evolved design: right, or refused out loud;
crashing, hanging or computing something else kills it. The hand-made stages
and --validate are exempt - run-tests.sh judges them. Its cost: lost in the
build's noise (the 167-design sweep 133 s, 139-143 s before).

## Speed (a probe, one CPU, five runs each)

fib at 0, 64 KB, 4 MB, 8 MB: interpreted tag2 designs 5-9% slower with long
calls (the smallest 9.0 -> 9.7 ms; a t2wide design 5.5 -> 5.8-6.0 ms); the JIT
founder no change beyond noise. A far benchmark, held out for one laptop run,
would say how much it reorders the front.

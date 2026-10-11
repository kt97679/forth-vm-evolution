# The cheaper rtloop: rtloop=2 (Iteration 190)

forth/cv8-fuse-loop.4's eight internal words (X10-OP, W@, CHAIN16?,
RESOLVE-LEAVE16, RESOLVE-LEAVES, LOOP-OPS, X10-XTS, X10-OPS) are reached only by
the overlay's own compiled calls and by the converter, which fills the three
tables by name in the dump. rtloop=2: the converter (tools/layout.py
--headerless) keeps their code, drops their headers - no link, no name, on no
thread - and its chain check expects the rest. A name defined twice keeps its
header (hiding the later would hand the name back to the earlier).

Measured on the development VM (timings within ~9-14%; sizes exact), the
thirteen after-seed-41 patches applied:

| design | rtloop | image | loop | sieve | bubble |
|---|---|---|---|---|---|
| 0ceb043115, the smallest | 0 | 7,518 | 1.32 | 1.30 | 1.33 |
| | 1 | 8,086 (+568) | 0.34 | 1.01 | 1.16 |
| | **2** | **7,978 (+460)** | 0.37 | 1.01 | 1.14 |
| d99e3d9ed9, the knee (JIT) | 0 | 7,318 | 1.41 | 1.25 | 1.33 |
| | 1 | 7,871 (+553) | 0.59 | 1.09 | 1.33 |
| | **2** | **7,763 (+445)** | 0.59 | 1.14 | 1.33 |

The knee founder (rtimm=2, DUP+I, DUP<I), five rounds: without rtloop fib 0.95,
bubble 1.39, loop 1.33, sieve 1.28; with rtloop=2 fib 0.89, bubble 1.29, loop
0.58, sieve 1.09. A first three-round session had shown fib and bubble worse
with rtloop - noise (the founder's own fib moved 0.83 -> 0.95 between
sessions). Checked deterministically: probe words compiled at run time take the
same bytes with and without rtloop - DUP 1 + 8 bytes, DUP 5 < IF 1 THEN 13
(10 and 15 without the forms) - the forms survive the loop overlay; only the
loop shrinks (10 0 DO I DROP LOOP: 25 -> 18).

Sweep: seed 40's recorded designs with rtloop=1 (not loopall): 128. The first
ten rebuilt with rtloop=2: 10 of 10 alive, each 96-104 bytes smaller.
run-tests PASS. Without --headerless the converter's paths are unchanged (every
change guarded by membership in an empty set).

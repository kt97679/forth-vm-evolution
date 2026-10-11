# RECURSE in :NONAME - held back (Iteration 170)

coreexttest's four failures (RN1, RN2) are RECURSE in a :NONAME definition:
the kernel's RECURSE and both byte compilers' RECURSE8 compile a call to LAST's
word, and a :NONAME makes no header. The fix below keeps :NONAME's xt and uses
it while no header is newer than it, else the design's own RECURSE (by xt).

Run directly on s6 it is right (a :NONAME's xt 0x414370 above LAST 0x414342;
after `: FOO`, LAST 0x414375 above it; `3 FOO` recurses to 0) and the whole
coreexttest.fth does not crash - but under lab/evolve/ans-check.py the file
dies with SIGSEGV (exit -11), and without the change it does not. Next: what
the runner does differently (its jail's limits; coreext.4's ALLOCATEs, whose
ior is dropped, would fail into address 0).

```forth
VARIABLE NONAME-XT  0 NONAME-XT !
: :NONAME ( --- xt colon-sys )  ALIGN HERE DUP NONAME-XT ! !CSP ] ;
' RECURSE CONSTANT 'RECURSE
: RECURSE ( --- )
  NONAME-XT @ LAST @ U< IF 'RECURSE EXECUTE ELSE NONAME-XT @ COMPILE, THEN ; IMMEDIATE
```

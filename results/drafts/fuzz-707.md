# fuzz-designs.py runs (Iteration 707) - the logs: x86 both widths (two passes, the second --harsh), ARMv7 under qemu (--harsh --arm), the three ARMv7 designs again with the after-seed-96 batch

## /tmp/fuzz.log
```
923951e8ab 8-byte tos=1 clang JIT: 0 of 40 programs differ
3ea4a69c62 8-byte tos=1 GCC JIT: 0 of 40 programs differ
a4e502f224 8-byte tos=0 clang: 0 of 40 programs differ
d7fb9683c2 8-byte tos=1 clang: 0 of 40 programs differ
94a4605110 8-byte tos=1 GCC: 0 of 40 programs differ
a8d35bdccc 8-byte tos=0 GCC: 0 of 40 programs differ
9b15ba26f7 8-byte tos=1 clang JIT: 0 of 40 programs differ
371bcdcbbc 8-byte tos=1 clang JIT: 0 of 40 programs differ
23f8f8a9b1 8-byte tos=1 clang JIT: 0 of 40 programs differ
79e5a089b2 8-byte tos=1 clang JIT: 0 of 40 programs differ
418be5982a 8-byte tos=0 clang: 0 of 40 programs differ
8f32721fc1 8-byte tos=1 clang: 0 of 40 programs differ
923951e8ab 4-byte tos=1 clang JIT: 0 of 40 programs differ
3ea4a69c62 4-byte tos=1 GCC JIT: 0 of 40 programs differ
a4e502f224 4-byte tos=0 clang: 0 of 40 programs differ
d7fb9683c2 4-byte tos=1 clang: 0 of 40 programs differ
94a4605110 4-byte tos=1 GCC: 0 of 40 programs differ
a8d35bdccc 4-byte tos=0 GCC: 0 of 40 programs differ
9b15ba26f7 4-byte tos=1 clang JIT: 0 of 40 programs differ
371bcdcbbc 4-byte tos=1 clang JIT: 0 of 40 programs differ
23f8f8a9b1 4-byte tos=1 clang JIT: 0 of 40 programs differ
79e5a089b2 4-byte tos=1 clang JIT: 0 of 40 programs differ
418be5982a 4-byte tos=0 clang: 0 of 40 programs differ
8f32721fc1 4-byte tos=1 clang: 0 of 40 programs differ
fuzz-designs: 960 runs, 0 differ from s6; the programs that did in /tmp/fuzz
```

## /tmp/fuzz2.log
```
923951e8ab 8-byte tos=1 clang JIT: 0 of 40 programs differ
3ea4a69c62 8-byte tos=1 GCC JIT: 0 of 40 programs differ
a4e502f224 8-byte tos=0 clang: 0 of 40 programs differ
d7fb9683c2 8-byte tos=1 clang: 0 of 40 programs differ
94a4605110 8-byte tos=1 GCC: 0 of 40 programs differ
a8d35bdccc 8-byte tos=0 GCC: 0 of 40 programs differ
9b15ba26f7 8-byte tos=1 clang JIT: 0 of 40 programs differ
41c54d161a 8-byte tos=1 clang JIT: 0 of 40 programs differ
72060411c1 8-byte tos=1 clang JIT: 0 of 40 programs differ
4daa54d3f5 8-byte tos=1 clang JIT: 0 of 40 programs differ
9070323f9b 8-byte tos=1 clang JIT: 0 of 40 programs differ
3f0bfd1276 8-byte tos=1 clang JIT: 0 of 40 programs differ
be18932863 8-byte tos=0 clang: 0 of 40 programs differ
40b8e3a3a7 8-byte tos=0 clang: 0 of 40 programs differ
33f29b81d6 8-byte tos=1 clang: 0 of 40 programs differ
bee66ec75c 8-byte tos=1 GCC: 0 of 40 programs differ
923951e8ab 4-byte tos=1 clang JIT: 0 of 40 programs differ
3ea4a69c62 4-byte tos=1 GCC JIT: 0 of 40 programs differ
a4e502f224 4-byte tos=0 clang: 0 of 40 programs differ
d7fb9683c2 4-byte tos=1 clang: 0 of 40 programs differ
94a4605110 4-byte tos=1 GCC: 0 of 40 programs differ
a8d35bdccc 4-byte tos=0 GCC: 0 of 40 programs differ
9b15ba26f7 4-byte tos=1 clang JIT: 0 of 40 programs differ
41c54d161a 4-byte tos=1 clang JIT: 0 of 40 programs differ
72060411c1 4-byte tos=1 clang JIT: 0 of 40 programs differ
4daa54d3f5 4-byte tos=1 clang JIT: 0 of 40 programs differ
9070323f9b 4-byte tos=1 clang JIT: 0 of 40 programs differ
3f0bfd1276 4-byte tos=1 clang JIT: 0 of 40 programs differ
be18932863 4-byte tos=0 clang: 0 of 40 programs differ
40b8e3a3a7 4-byte tos=0 clang: 0 of 40 programs differ
33f29b81d6 4-byte tos=1 clang: 0 of 40 programs differ
bee66ec75c 4-byte tos=1 GCC: 0 of 40 programs differ
fuzz-designs: 1280 runs, 0 differ from s6; the programs that did in /tmp/fuzz2
```

## /tmp/fuzz3.log
```
a4e502f224 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
d7fb9683c2 4-byte tos=1 clang ARMv7: 0 of 30 programs differ
21a6cb01ef 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
6284f32b93 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
2324cdfbc9 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
9c9d35e537 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
d3c79f0616 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
5f7e66b12d 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
8fe37f346e 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
dcf620b809 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
c9c73fd981 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
4b0d1c621c 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
022d7fd86e 4-byte tos=1 clang ARMv7: 10 of 30 programs differ - p9, p10, p12, p18, p19, p20, p23, p26
cb03515bc4 4-byte tos=1 clang ARMv7: 10 of 30 programs differ - p9, p10, p12, p18, p19, p20, p23, p26
b575c8d1ff 4-byte tos=1 clang ARMv7: 10 of 30 programs differ - p9, p10, p12, p18, p19, p20, p23, p26
dcc0494fb5 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
1472fb150b 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
3ca1b5bef2 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
2a5009cd63 4-byte tos=0 clang ARMv7: 0 of 30 programs differ
fuzz-designs: 570 runs, 30 differ from s6; the programs that did in /tmp/fuzz3
```

## the three ARMv7 designs again, in a tree with the after-seed-96 batch applied
```
022d7fd86e 4-byte tos=1 clang ARMv7: 0 of 30 programs differ
cb03515bc4 4-byte tos=1 clang ARMv7: 0 of 30 programs differ
b575c8d1ff 4-byte tos=1 clang ARMv7: 0 of 30 programs differ
fuzz-designs: 90 runs, 0 differ from s6
```

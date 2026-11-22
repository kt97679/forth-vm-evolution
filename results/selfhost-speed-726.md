# The self-hosting gate's speed half on portable-fastest (Iteration 726) - pass

The pack's selfhost-speed.md (chain at b0801d04e, fury 2026-11-22 05:36:57-05:38:35 UTC; results/rage-designs-726.md has the chain), its three "pinned to cpu" lines dropped as 725's were (cpus 1-2, each core and its sibling 5-7 % busy). portable-fastest (d727605472), self-built since 722, stays self-built: 0.9974 at 8-byte cells, 0.9867 at 4 (the gate 1.02).

1 designs, self-built against the translator's build, 5 alternations of 10 rounds over kernel, fib, corpus, loop, bubble, ackermann, apps at both widths.

| design | id | 8-byte: self / translator, median (range) | 4-byte: self / translator, median (range) | gate |
|---|---|---|---|---|
| portable-fastest | d727605472 | 0.9974 (0.9887-1.0081) | 0.9867 (0.9755-0.9909) | pass |

{"by4": {"ackermann": 1.0059, "apps": 0.9841, "bubble": 0.9803, "corpus": 0.9614, "fib": 1.0065, "kernel": 0.9649, "loop": 1.014}, "by8": {"ackermann": 0.9836, "apps": 1.0002, "bubble": 1.0728, "corpus": 0.961, "fib": 1.0078, "kernel": 0.9496, "loop": 0.9946}, "gate": "pass", "id": "d727605472", "name": "portable-fastest", "r4": [0.9755188792488882, 0.9866991289982864, 0.9899114296753593, 0.9836575350208592, 0.9908516942681457], "r8": [1.001642472241575, 0.9974276481089119, 0.9961850444407507, 1.0080523268736317, 0.9886748756312369]}

selfhost-speed: 1 of 1 pass the gate (self-built at most 1.02 of the translator's at both widths)

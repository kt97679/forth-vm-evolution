## 8dd8a7a146 - 13 pairs, 21 format-10 words

| workload | dispatches | pairs save | best 8 triples | best 16 | next 16 pairs | test -> branch | calls | EXIT |
|---|---|---|---|---|---|---|---|---|
| kernel | 6934908 | 14.3% | 3.0% | 3.0% | 6.4% | 3.3% | 7.5% | 2.6% |
| fib | 29670998 | 0.0% | 0.0% | 0.0% | 0.0% | 9.1% | 9.1% | 9.1% |
| parse | 27738691 | 13.0% | 2.5% | 2.5% | 12.9% | 2.6% | 3.9% | 1.7% |
| corpus | 5044062 | 14.3% | 3.3% | 3.4% | 8.6% | 2.5% | 4.7% | 2.1% |

the tests before a conditional branch, by workload:
  kernel  eqi 1.3%, sub 1.1%, < 0.4%, sgt 0.3%, eqix 0.1%
  fib     < 9.1%, eqi 0.0%, sub 0.0%, sgt 0.0%, zlt 0.0%
  parse   eqi 1.7%, sub 0.4%, sgt 0.4%, zlt 0.1%
  corpus  eqi 1.3%, sub 0.7%, sgt 0.4%, zlt 0.1%, = 0.0%
the best triples, mean share: SWAP+DUP+>R 0.4%, OVER+C@+SWAP 0.4%, C@+>R+OVER 0.4%, ROT+DUP+C@ 0.4%, >R+OVER+R> 0.4%, >R+OVER+C@ 0.2%

## 60753a0eb0 - 13 pairs, 21 format-10 words

| workload | dispatches | pairs save | best 8 triples | best 16 | next 16 pairs | test -> branch | calls | EXIT |
|---|---|---|---|---|---|---|---|---|
| kernel | 7881789 | 14.1% | 3.3% | 3.4% | 3.9% | 2.6% | 14.8% | 2.7% |
| fib | 32370948 | 0.0% | 0.0% | 0.0% | 0.0% | 8.3% | 16.7% | 8.3% |
| parse | 33708333 | 14.5% | 2.6% | 2.7% | 3.3% | 1.1% | 11.8% | 2.6% |
| corpus | 5884877 | 14.9% | 3.6% | 3.8% | 3.5% | 1.5% | 11.4% | 2.5% |

the tests before a conditional branch, by workload:
  kernel  sub 1.0%, eqi 0.9%, < 0.3%, sgt 0.3%, eqix 0.1%
  fib     < 8.3%, sub 0.0%, eqi 0.0%, sgt 0.0%, zlt 0.0%
  parse   sub 0.3%, eqi 0.3%, sgt 0.3%, zlt 0.0%
  corpus  sub 0.6%, eqi 0.5%, sgt 0.3%, zlt 0.1%, = 0.0%
the best triples, mean share: >R+OVER+C@ 0.4%, SWAP+DUP+>R 0.3%, OVER+C@+SWAP 0.3%, C@+>R+OVER 0.3%, ROT+DUP+C@ 0.3%, >R+OVER+R> 0.3%


**Correction (Iteration 13).** The profiler records two events that are not
dispatches: L_esc profiles its selector (0.03% of kernel), and with the
256-entry dispatch NEXT profiles a call's first byte before do_call
profiles 256. 60753a0eb0's profiling engine has the 256-entry dispatch,
so every call above is counted twice: its dispatches are overstated by
its calls (kernel 7,881,789 is 7,295,465 by address) and its calls
column is doubled (kernel 14.8%, really 8.0%; parse 11.8%, really 6.2%;
fib 16.7%, really 9.1%), and every other share in its row is about 8%
too low. 8dd8a7a146 has no 256-entry dispatch and is right. The
comparisons drawn from the table - pairs overlap, tests before branches
do not - are within a row and stand. lab/evolve/price.py now skips both
events; `results/price-hotcalls-seed3-front.md` has the audit.

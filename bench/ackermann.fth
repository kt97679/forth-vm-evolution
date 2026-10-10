\ ackermann.fth - Ackermann's function: deep recursion and nothing else.
\
\ fib.fth recurses some 25 deep; this goes hundreds deep, and its data stack
\ grows with it - what a call, a return and the stacks cost when nothing is
\ shallow. A(3,5) = 253, by 42,438 calls. The owner's collection has an
\ Ackermann among RelF's old benchmarks (RelF/bench, not in this repository);
\ this is the textbook definition, written as his bench.4 writes fib (Iteration
\ 127). CORE words only; the value is printed, so a design that gets it wrong
\ shows.

: ACK ( m n --- a )
  OVER 0= IF SWAP DROP 1+ EXIT THEN
  DUP 0= IF DROP 1- 1 RECURSE EXIT THEN
  OVER SWAP 1- RECURSE SWAP 1- SWAP RECURSE ;

: BENCH ( --- )  3 5 ACK . CR ;

BENCH
S" BENCH-DONE" TYPE CR

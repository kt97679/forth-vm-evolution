#!/bin/sh
for w in fib loop sieve bubble ackermann parse; do
  for r in 1 2 3; do /home/claude/forth-vm-evolution/build/cputime /tmp/cb/bench-O2 $w 1 /home/claude/forth-vm-evolution/bench/parse.fth 2>&1 >/dev/null | grep CPUNS | awk -v w=$w '{printf "%s %.2f ms\n", w, $2/1e6}'; done
done

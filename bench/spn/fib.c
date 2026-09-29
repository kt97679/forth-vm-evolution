#include <stdio.h>
#include <stdlib.h>
static long fib(long n) { return n < 2 ? 1 : fib(n - 1) + fib(n - 2); }
int main(int argc, char **argv) {
    volatile long n = argc > 1 ? atol(argv[1]) : 30; long s = 0;
    for (int i = 0; i < 10; i++) { s += fib(n); __asm__ volatile("" : "+r"(s)); }
    printf("%ld\n", s); return 0;
}

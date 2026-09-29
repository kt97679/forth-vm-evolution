#include <stdio.h>
#include <stdlib.h>
/* The Forth SUMTO, step for step. The empty asm keeps s and n in
   registers but stops GCC replacing the loop by n(n+1)/2 or vectorising
   it - so this is optimised C doing the same work, one step at a time. */
static long sumto(long n) {
    long s = 0;
    do { s += n; n--; __asm__ volatile("" : "+r"(s), "+r"(n)); } while (n != 0);
    return s;
}
int main(int argc, char **argv) {
    volatile long n = argc > 1 ? atol(argv[1]) : 50000000;
    printf("%ld\n", sumto(n)); return 0;
}

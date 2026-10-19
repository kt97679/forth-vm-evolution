/* Iteration 405 (results/rehearsal-405.md): gcc -m32 -O2 -fno-pie -S -o - THIS - an extern function's indirect tail call after a call is a jmp *%eax; the same in a handler GCC made local (t2call) was not. */
typedef void (*hfn)(unsigned, unsigned, unsigned, unsigned, unsigned);
extern unsigned g1, g2, g3, g4, g5;
hfn inner(unsigned a, unsigned b, unsigned c, unsigned d, unsigned e);
void outer(unsigned a, unsigned b, unsigned c, unsigned d, unsigned e) { hfn f = inner(a, b, c, d, e); if (!f) return; f(g1, g2, g3, g4, g5); }

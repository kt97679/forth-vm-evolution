/*
 *  dispatch.c - the fastest C dispatch loop for Forth, found by measuring.
 *
 *  One small Forth machine, written six ways, running the same three
 *  programs. Every way must give the same answers before any is timed.
 *
 *    switch     a switch on compact word code - the textbook baseline
 *    token      the same code, computed goto through a table of labels
 *               (what the CV8 engine does)
 *    direct     direct threading: the code IS the label addresses, so a
 *               dispatch is one load and one indirect jump
 *    tail       tail-call threading: each primitive a C function, all
 *               machine state in argument registers, each ending in a jump
 *               to the next - the register allocator works per handler
 *    native     as tail, but a Forth CALL is a real machine call and EXIT
 *               a real return, so the processor's return predictor
 *               predicts every Forth return
 *    native2    as native, with the top TWO stack items in registers
 *
 *  Any of them with -s: superinstructions - DUP n < IF and n + fused,
 *  as SPN does.
 *
 *    dispatch VARIANT PROGRAM [-s]      PROGRAM: fib | loop | sieve
 *
 *  prints the program's result. Time it from outside - lab/dispatch/run.py
 *  uses tools/cputime - so every variant is measured the same way.
 *
 *  Programs, in Forth:
 *    fib    : FIB DUP 2 < IF DROP 1 EXIT THEN DUP -1 + FIB SWAP -2 + FIB + ;
 *           32 FIB
 *    loop   : CNT BEGIN -1 + DUP 0= UNTIL DROP ;   50000000 CNT
 *    sieve  the BYTE sieve over 8191 flags, 400 times
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef intptr_t cell;
static uint8_t mem[16384];                  /* data memory; addresses index it */

enum { LIT, DUP, DROP, SWAP, OVER, ADD, SUB, LT, ZEQ, ZBR, BR, CALL, EXIT,
       CFETCH, CSTORE, ADDI, DO, LOOP, I, DUPLTBR, HALT, NOPS };
static const int nargs[NOPS] = { [LIT] = 1, [ZBR] = 1, [BR] = 1, [CALL] = 1,
                                 [ADDI] = 1, [LOOP] = 1, [DUPLTBR] = 2 };

/* ---- the programs, assembled into word code: an int32 opcode, then its
 *      operands; branch targets are word-code indices ---- */
static int32_t wc[1024]; static int wn;
static int lab[32]; static struct { int at, l; } fix[64]; static int nfix;
static int super;
static void E(int op)                      { wc[wn++] = op; }
static void EA(int op, int32_t a)          { wc[wn++] = op; wc[wn++] = a; }
static void EL(int op, int l)              { wc[wn++] = op; fix[nfix].at = wn; fix[nfix++].l = l; wc[wn++] = 0; }
static void L(int l)                       { lab[l] = wn; }
static void LIT_ADD(int32_t n)             { if (super) EA(ADDI, n); else { EA(LIT, n); E(ADD); } }
static void DUP_LT_IF(int32_t n, int l)    /* DUP n < IF ... with l just past the IF's body */
{
    if (super) { wc[wn++] = DUPLTBR; wc[wn++] = n; fix[nfix].at = wn; fix[nfix++].l = l; wc[wn++] = 0; }
    else { E(DUP); EA(LIT, n); E(LT); EL(ZBR, l); }
}
enum { L_MAIN, L_FIB, L_FIB1, L_CNT, L_CNT0, L_SIEVE, L_FILL, L_OUTER, L_SKIP, L_INNER, L_DONE, L_MLOOP };
#define FLAGS 0
#define SIZE 8191

static int assemble(const char *prog)
{
    wn = nfix = 0;
    if (!strcmp(prog, "fib")) {
        L(L_MAIN);  EA(LIT, 32); EL(CALL, L_FIB); E(HALT);
        L(L_FIB);   DUP_LT_IF(2, L_FIB1); E(DROP); EA(LIT, 1); E(EXIT);
        L(L_FIB1);  E(DUP); LIT_ADD(-1); EL(CALL, L_FIB); E(SWAP); LIT_ADD(-2); EL(CALL, L_FIB);
                    E(ADD); E(EXIT);
    } else if (!strcmp(prog, "loop")) {
        L(L_MAIN);  EA(LIT, 50000000); EL(CALL, L_CNT); EA(LIT, 0); E(HALT);
        L(L_CNT);   L(L_CNT0); LIT_ADD(-1); E(DUP); E(ZEQ); EL(ZBR, L_CNT0); E(DROP); E(EXIT);
    } else if (!strcmp(prog, "sieve")) {
        L(L_MAIN);  EA(LIT, 0); EA(LIT, 400); EA(LIT, 0); E(DO);
                    L(L_MLOOP); E(DROP); EL(CALL, L_SIEVE); EL(LOOP, L_MLOOP); E(HALT);
        L(L_SIEVE); EA(LIT, SIZE); EA(LIT, 0); E(DO);                 /* flags all 1 */
                    L(L_FILL); EA(LIT, 1); E(I); LIT_ADD(FLAGS); E(CSTORE); EL(LOOP, L_FILL);
                    EA(LIT, 0);                                        /* count */
                    EA(LIT, SIZE); EA(LIT, 0); E(DO);
                    L(L_OUTER); E(I); LIT_ADD(FLAGS); E(CFETCH); EL(ZBR, L_SKIP);
                      E(I); E(DUP); E(ADD); LIT_ADD(3);                /* count prime */
                      E(DUP); E(I); E(ADD);                            /* count prime k */
                      L(L_INNER); DUP_LT_IF(SIZE, L_DONE);
                        EA(LIT, 0); E(OVER); LIT_ADD(FLAGS); E(CSTORE); E(OVER); E(ADD);
                        EL(BR, L_INNER);
                      L(L_DONE); E(DROP); E(DROP); LIT_ADD(1);
                    L(L_SKIP); EL(LOOP, L_OUTER); E(EXIT);
    } else return 0;
    for (int i = 0; i < nfix; i++) wc[fix[i].at] = lab[fix[i].l];
    return 1;
}

#define STK 1024
static cell dstk[STK + 8], rstk[STK];      /* slack: an empty stack's first pop stays inside */

/* ---- 1. switch --------------------------------------------------------- */
static cell run_switch(void)
{
    const int32_t *ip = wc; cell *sp = dstk + STK, *rp = rstk + STK, tos = 0;
    for (;;) switch (*ip++) {
    case LIT:    *--sp = tos; tos = *ip++; break;
    case DUP:    *--sp = tos; break;
    case DROP:   tos = *sp++; break;
    case SWAP:   { cell t = *sp; *sp = tos; tos = t; } break;
    case OVER:   { cell t = *sp; *--sp = tos; tos = t; } break;
    case ADD:    tos += *sp++; break;
    case SUB:    tos = *sp++ - tos; break;
    case LT:     tos = -(*sp++ < tos); break;
    case ZEQ:    tos = -(tos == 0); break;
    case ZBR:    { cell f = tos; tos = *sp++; ip = f ? ip + 1 : wc + *ip; } break;
    case BR:     ip = wc + *ip; break;
    case CALL:   *--rp = (cell)(ip + 1); ip = wc + *ip; break;
    case EXIT:   ip = (const int32_t *)*rp++; break;
    case CFETCH: tos = mem[tos]; break;
    case CSTORE: mem[tos] = (uint8_t)*sp; tos = sp[1]; sp += 2; break;
    case ADDI:   tos += *ip++; break;
    case DO:     rp -= 2; rp[1] = *sp; rp[0] = tos; tos = sp[1]; sp += 2; break;
    case LOOP:   if (++rp[0] != rp[1]) ip = wc + *ip; else { rp += 2; ip++; } break;
    case I:      *--sp = tos; tos = rp[0]; break;
    case DUPLTBR: ip = tos >= ip[0] ? wc + ip[1] : ip + 2; break;
    case HALT:   return tos;
    }
}

/* ---- 2. token threading: the same word code, computed goto ---------------- */
static cell run_token(void)
{
    static void *const t[NOPS] = { &&lit, &&dup, &&drop, &&swap, &&over, &&add, &&sub, &&lt,
        &&zeq, &&zbr, &&br, &&call, &&exit, &&cfetch, &&cstore, &&addi, &&do_, &&loop, &&i,
        &&dupltbr, &&halt };
    const int32_t *ip = wc; cell *sp = dstk + STK, *rp = rstk + STK, tos = 0;
#define TK goto *t[*ip++]
    TK;
lit:    *--sp = tos; tos = *ip++; TK;
dup:    *--sp = tos; TK;
drop:   tos = *sp++; TK;
swap:   { cell x = *sp; *sp = tos; tos = x; } TK;
over:   { cell x = *sp; *--sp = tos; tos = x; } TK;
add:    tos += *sp++; TK;
sub:    tos = *sp++ - tos; TK;
lt:     tos = -(*sp++ < tos); TK;
zeq:    tos = -(tos == 0); TK;
zbr:    { cell f = tos; tos = *sp++; ip = f ? ip + 1 : wc + *ip; } TK;
br:     ip = wc + *ip; TK;
call:   *--rp = (cell)(ip + 1); ip = wc + *ip; TK;
exit:   ip = (const int32_t *)*rp++; TK;
cfetch: tos = mem[tos]; TK;
cstore: mem[tos] = (uint8_t)*sp; tos = sp[1]; sp += 2; TK;
addi:   tos += *ip++; TK;
do_:    rp -= 2; rp[1] = *sp; rp[0] = tos; tos = sp[1]; sp += 2; TK;
loop:   if (++rp[0] != rp[1]) ip = wc + *ip; else { rp += 2; ip++; } TK;
i:      *--sp = tos; tos = rp[0]; TK;
dupltbr: ip = tos >= ip[0] ? wc + ip[1] : ip + 2; TK;
halt:   return tos;
#undef TK
}

/* ---- threaded code: one cell per operation - a label or a function - then
 *      its operands; branch targets are addresses. Built from the word code. */
static cell tc[1024];
static void thread(void *const *handler)
{
    int pos[1024], p = 0;
    for (int i = 0; i < wn; i += 1 + nargs[wc[i]]) { pos[i] = p; p += 1 + nargs[wc[i]]; }
    for (int i = 0; i < wn; i += 1 + nargs[wc[i]]) {
        int op = wc[i], at = pos[i];
        tc[at] = (cell)handler[op];
        if (op == LIT || op == ADDI) tc[at + 1] = wc[i + 1];
        else if (op == DUPLTBR) { tc[at + 1] = wc[i + 1]; tc[at + 2] = (cell)&tc[pos[wc[i + 2]]]; }
        else if (nargs[op]) tc[at + 1] = (cell)&tc[pos[wc[i + 1]]];
    }
}

/* ---- 3. direct threading ------------------------------------------------ */
static cell run_direct(int init)
{
    static void *const t[NOPS] = { &&lit, &&dup, &&drop, &&swap, &&over, &&add, &&sub, &&lt,
        &&zeq, &&zbr, &&br, &&call, &&exit, &&cfetch, &&cstore, &&addi, &&do_, &&loop, &&i,
        &&dupltbr, &&halt };
    if (init) { thread(t); return 0; }
    const cell *ip = tc; cell *sp = dstk + STK, *rp = rstk + STK, tos = 0;
#define DN goto *(void *)*ip++
    DN;
lit:    *--sp = tos; tos = *ip++; DN;
dup:    *--sp = tos; DN;
drop:   tos = *sp++; DN;
swap:   { cell x = *sp; *sp = tos; tos = x; } DN;
over:   { cell x = *sp; *--sp = tos; tos = x; } DN;
add:    tos += *sp++; DN;
sub:    tos = *sp++ - tos; DN;
lt:     tos = -(*sp++ < tos); DN;
zeq:    tos = -(tos == 0); DN;
zbr:    { cell f = tos; tos = *sp++; ip = f ? ip + 1 : (const cell *)*ip; } DN;
br:     ip = (const cell *)*ip; DN;
call:   *--rp = (cell)(ip + 1); ip = (const cell *)*ip; DN;
exit:   ip = (const cell *)*rp++; DN;
cfetch: tos = mem[tos]; DN;
cstore: mem[tos] = (uint8_t)*sp; tos = sp[1]; sp += 2; DN;
addi:   tos += *ip++; DN;
do_:    rp -= 2; rp[1] = *sp; rp[0] = tos; tos = sp[1]; sp += 2; DN;
loop:   if (++rp[0] != rp[1]) ip = (const cell *)*ip; else { rp += 2; ip++; } DN;
i:      *--sp = tos; tos = rp[0]; DN;
dupltbr: ip = tos >= ip[0] ? (const cell *)ip[1] : ip + 2; DN;
halt:   return tos;
#undef DN
}

/* ---- 3b. indirect threading (Iteration 29) - fig-Forth, eForth, JonesForth,
 *      gforth-itc: every reference is the address of a word's CODE FIELD,
 *      which holds the address of its machine code - two loads before the
 *      jump. A colon word's code field holds docol, and its body follows the
 *      field; a primitive's code field sits in a table of them. ---- */
static cell itc_cf[NOPS];                   /* the primitives' code fields */
static void thread_itc(void *const *handler, void *docol)
{
    int pos[1024], target[1024] = { 0 }, p = 0;
    for (int i = 0; i < wn; i += 1 + nargs[wc[i]]) if (wc[i] == CALL) target[wc[i + 1]] = 1;
    for (int i = 0; i < wn; i += 1 + nargs[wc[i]]) {
        if (target[i]) p++;                   /* a colon word: its code field before its body */
        pos[i] = p; p += wc[i] == CALL ? 1 : 1 + nargs[wc[i]];
    }
    for (int op = 0; op < NOPS; op++) itc_cf[op] = (cell)handler[op];
    for (int i = 0; i < wn; i += 1 + nargs[wc[i]]) {
        int op = wc[i], at = pos[i];
        if (target[i]) tc[at - 1] = (cell)docol;
        if (op == CALL) { tc[at] = (cell)&tc[pos[wc[i + 1]] - 1]; continue; }   /* the callee's code field */
        tc[at] = (cell)&itc_cf[op];
        if (op == LIT || op == ADDI) tc[at + 1] = wc[i + 1];
        else if (op == DUPLTBR) { tc[at + 1] = wc[i + 1]; tc[at + 2] = (cell)&tc[pos[wc[i + 2]]]; }
        else if (nargs[op]) tc[at + 1] = (cell)&tc[pos[wc[i + 1]]];
    }
    tc[1023] = pos[0];                        /* where the program starts */
}
static cell run_itc(int init)
{
    static void *const t[NOPS] = { &&lit, &&dup, &&drop, &&swap, &&over, &&add, &&sub, &&lt,
        &&zeq, &&zbr, &&br, 0, &&exit, &&cfetch, &&cstore, &&addi, &&do_, &&loop, &&i,
        &&dupltbr, &&halt };
    if (init) { thread_itc(t, &&docol); return 0; }
    const cell *ip = tc + tc[1023], *w; cell *sp = dstk + STK, *rp = rstk + STK, tos = 0;
#define IN do { w = (const cell *)*ip++; goto *(void *)*w; } while (0)
    IN;
docol:  *--rp = (cell)ip; ip = w + 1; IN;
lit:    *--sp = tos; tos = *ip++; IN;
dup:    *--sp = tos; IN;
drop:   tos = *sp++; IN;
swap:   { cell x = *sp; *sp = tos; tos = x; } IN;
over:   { cell x = *sp; *--sp = tos; tos = x; } IN;
add:    tos += *sp++; IN;
sub:    tos = *sp++ - tos; IN;
lt:     tos = -(*sp++ < tos); IN;
zeq:    tos = -(tos == 0); IN;
zbr:    { cell f = tos; tos = *sp++; ip = f ? ip + 1 : (const cell *)*ip; } IN;
br:     ip = (const cell *)*ip; IN;
exit:   ip = (const cell *)*rp++; IN;
cfetch: tos = mem[tos]; IN;
cstore: mem[tos] = (uint8_t)*sp; tos = sp[1]; sp += 2; IN;
addi:   tos += *ip++; IN;
do_:    rp -= 2; rp[1] = *sp; rp[0] = tos; tos = sp[1]; sp += 2; IN;
loop:   if (++rp[0] != rp[1]) ip = (const cell *)*ip; else { rp += 2; ip++; } IN;
i:      *--sp = tos; tos = rp[0]; IN;
dupltbr: ip = tos >= ip[0] ? (const cell *)ip[1] : ip + 2; IN;
halt:   return tos;
#undef IN
}

/* ---- 4-6. tail-call threading ------------------------------------------- */
#if defined(__has_attribute)
# if __has_attribute(musttail)
#  define MUSTTAIL __attribute__((musttail))
# endif
#endif
#ifndef MUSTTAIL
# define MUSTTAIL          /* GCC before 15: -O2's sibling calls do it; run.py checks */
#endif
typedef struct { cell *sp; cell tos; } st;                 /* rax:rdx */
typedef st (*fn)(const cell *ip, cell *sp, cell *rp, cell tos);
#define H(n) static st n(const cell *ip, cell *sp, cell *rp, cell tos)
#define NX MUSTTAIL return ((fn)ip[0])(ip + 1, sp, rp, tos)
H(t_lit)    { *--sp = tos; tos = *ip++; NX; }
H(t_dup)    { *--sp = tos; NX; }
H(t_drop)   { tos = *sp++; NX; }
H(t_swap)   { cell x = *sp; *sp = tos; tos = x; NX; }
H(t_over)   { cell x = *sp; *--sp = tos; tos = x; NX; }
H(t_add)    { tos += *sp++; NX; }
H(t_sub)    { tos = *sp++ - tos; NX; }
H(t_lt)     { tos = -(*sp++ < tos); NX; }
H(t_zeq)    { tos = -(tos == 0); NX; }
H(t_zbr)    { cell f = tos; tos = *sp++; ip = f ? ip + 1 : (const cell *)*ip; NX; }
H(t_br)     { ip = (const cell *)*ip; NX; }
H(t_call)   { *--rp = (cell)(ip + 1); ip = (const cell *)*ip; NX; }
H(t_exit)   { ip = (const cell *)*rp++; NX; }
H(t_cfetch) { tos = mem[tos]; NX; }
H(t_cstore) { mem[tos] = (uint8_t)*sp; tos = sp[1]; sp += 2; NX; }
H(t_addi)   { tos += *ip++; NX; }
H(t_do)     { rp -= 2; rp[1] = *sp; rp[0] = tos; tos = sp[1]; sp += 2; NX; }
H(t_loop)   { if (++rp[0] != rp[1]) ip = (const cell *)*ip; else { rp += 2; ip++; } NX; }
H(t_i)      { *--sp = tos; tos = rp[0]; NX; }
H(t_dupltbr){ ip = tos >= ip[0] ? (const cell *)ip[1] : ip + 2; NX; }
H(t_halt)   { (void)ip; (void)rp; return (st){ sp, tos }; }
/* native: CALL is a real call - its return address on the machine stack,
   where the return predictor sees it - and EXIT a real return. */
H(n_call)   { const cell *w = (const cell *)*ip++;
              st r = ((fn)w[0])(w + 1, sp, rp, tos); sp = r.sp; tos = r.tos; NX; }
H(n_exit)   { (void)ip; (void)rp; return (st){ sp, tos }; }

static void *const tail_t[NOPS] = { t_lit, t_dup, t_drop, t_swap, t_over, t_add, t_sub, t_lt,
    t_zeq, t_zbr, t_br, t_call, t_exit, t_cfetch, t_cstore, t_addi, t_do, t_loop, t_i,
    t_dupltbr, t_halt };
static void *const native_t[NOPS] = { t_lit, t_dup, t_drop, t_swap, t_over, t_add, t_sub, t_lt,
    t_zeq, t_zbr, t_br, n_call, n_exit, t_cfetch, t_cstore, t_addi, t_do, t_loop, t_i,
    t_dupltbr, t_halt };
static cell run_tail(void)
{
    st r = ((fn)tc[0])(tc + 1, dstk + STK, rstk + STK, 0);
    return r.tos;
}

/* native2: TOS and NOS both in registers. A call passes both in; a return
   can carry only two values in registers, so EXIT leaves NOS in memory and
   the caller reloads it. */
typedef st (*fn2)(const cell *ip, cell *sp, cell *rp, cell tos, cell nos);
#define H2(n) static st n(const cell *ip, cell *sp, cell *rp, cell tos, cell nos)
#define NX2 MUSTTAIL return ((fn2)ip[0])(ip + 1, sp, rp, tos, nos)
H2(u_lit)    { *--sp = nos; nos = tos; tos = *ip++; NX2; }
H2(u_dup)    { *--sp = nos; nos = tos; NX2; }
H2(u_drop)   { tos = nos; nos = *sp++; NX2; }
H2(u_swap)   { cell x = nos; nos = tos; tos = x; NX2; }
H2(u_over)   { *--sp = nos; cell x = nos; nos = tos; tos = x; NX2; }
H2(u_add)    { tos += nos; nos = *sp++; NX2; }
H2(u_sub)    { tos = nos - tos; nos = *sp++; NX2; }
H2(u_lt)     { tos = -(nos < tos); nos = *sp++; NX2; }
H2(u_zeq)    { tos = -(tos == 0); NX2; }
H2(u_zbr)    { cell f = tos; tos = nos; nos = *sp++; ip = f ? ip + 1 : (const cell *)*ip; NX2; }
H2(u_br)     { ip = (const cell *)*ip; NX2; }
H2(u_call)   { const cell *w = (const cell *)*ip++;          /* in: both in registers */
               st r = ((fn2)w[0])(w + 1, sp, rp, tos, nos);
               sp = r.sp; tos = r.tos; nos = *sp++; NX2; }     /* out: NOS came back in memory */
H2(u_exit)   { (void)ip; (void)rp; *--sp = nos; return (st){ sp, tos }; }
H2(u_cfetch) { tos = mem[tos]; NX2; }
H2(u_cstore) { mem[tos] = (uint8_t)nos; tos = *sp++; nos = *sp++; NX2; }
H2(u_addi)   { tos += *ip++; NX2; }
H2(u_do)     { rp -= 2; rp[1] = nos; rp[0] = tos; tos = *sp++; nos = *sp++; NX2; }
H2(u_loop)   { if (++rp[0] != rp[1]) ip = (const cell *)*ip; else { rp += 2; ip++; } NX2; }
H2(u_i)      { *--sp = nos; nos = tos; tos = rp[0]; NX2; }
H2(u_dupltbr){ ip = tos >= ip[0] ? (const cell *)ip[1] : ip + 2; NX2; }
H2(u_halt)   { (void)ip; (void)rp; *--sp = nos; return (st){ sp, tos }; }
static void *const native2_t[NOPS] = { u_lit, u_dup, u_drop, u_swap, u_over, u_add, u_sub, u_lt,
    u_zeq, u_zbr, u_br, u_call, u_exit, u_cfetch, u_cstore, u_addi, u_do, u_loop, u_i,
    u_dupltbr, u_halt };
static cell run_tail2(void)
{
    st r = ((fn2)tc[0])(tc + 1, dstk + STK, rstk + STK, 0, 0);
    return r.tos;
}

int main(int argc, char **argv)
{
    if (argc < 3) { fprintf(stderr, "usage: dispatch switch|token|direct|itc|tail|native|native2 fib|loop|sieve [-s]\n"); return 2; }
    super = argc > 3 && !strcmp(argv[3], "-s");
    if (!assemble(argv[2])) { fprintf(stderr, "no program %s\n", argv[2]); return 2; }
    const char *v = argv[1]; cell r;
    if      (!strcmp(v, "switch"))  r = run_switch();
    else if (!strcmp(v, "token"))   r = run_token();
    else if (!strcmp(v, "direct"))  { run_direct(1); r = run_direct(0); }
    else if (!strcmp(v, "itc"))     { run_itc(1); r = run_itc(0); }
    else if (!strcmp(v, "tail"))    { thread(tail_t); r = run_tail(); }
    else if (!strcmp(v, "native"))  { thread(native_t); r = run_tail(); }
    else if (!strcmp(v, "native2")) { thread(native2_t); r = run_tail2(); }
    else { fprintf(stderr, "no variant %s\n", v); return 2; }
    printf("%ld\n", (long)r);
    return 0;
}

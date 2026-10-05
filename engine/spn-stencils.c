/*
 *  spn-stencils.c - SPN: Stencil-Patched Native.
 *
 *  Every function here is a STENCIL: one Forth operation written as an
 *  ordinary C function. They are never called. The Forth side reads their
 *  machine code out of this binary, copies it back to back into executable
 *  memory, and patches the holes. See forth/spn.4.
 *
 *  THE STATE. A stencil takes the data stack as (sp, tos): tos is the top
 *  item, sp points at the second. Under the calling convention both arrive
 *  in registers and leave in registers, so the top of stack is register-
 *  cached across the whole native sequence with no allocator anywhere.
 *
 *  THE HOLES. A stencil marks what the patcher must fill in by referring
 *  to one of four things, and the Forth side finds each reference exactly
 *  rather than by guessing:
 *
 *    spn_next(...)   a tail call - "continue with the next operation".
 *                    Found as a 32-bit relative jump whose target is
 *                    exactly &spn_next. Retargeted to the next stencil,
 *                    or dropped when the next stencil follows directly.
 *    spn_jump(...)   a branch target. Same test against &spn_jump.
 *    spn_call(...)   a call to another native word. Same test.
 *    SPN_IMM         a literal. Emitted as an 8-byte immediate, found by
 *                    its value.
 *
 *  A stencil that does not have the expected shape when the Forth side
 *  inspects it is simply not used, so an unexpected compiler makes SPN
 *  slower, never wrong.
 *
 *  RULES for writing a stencil: no calls except through the four markers,
 *  no static data, nothing PC-relative - the code is moved.
 */
#include <stdint.h>
#include "spn-abi.h"       /* cell, spn_st: registers in, registers out */

typedef cell (*spn_io_fn)(cell, cell, cell);
#if defined(__x86_64__)
#define SPN_IMM_VALUE 0x5ea1ed5ea1ed5ea1LL
/* A 32-bit hole, for when the literal fits. The compiler folds it into
   the instruction itself - add $imm32, cmp $imm32 - one instruction where
   the 64-bit hole needs a load and an operation. Chosen so its bytes do
   not occur inside the 64-bit marker's. */
#define IMM32 0x3c1a5e77L
/* Two more 64-bit holes, filled with ENGINE addresses rather than
   literals: the return-stack pointer that >R and R> share with the
   interpreter, and the helper that lets native code call a word that
   was not translated. Distinct values, so each is found unambiguously. */
#define SPN_RP_VALUE 0x7ea1ed5ea1ed5e77LL
#define SPN_FN_VALUE 0x6ea1ed5ea1ed5e66LL
#define IMM_RP() ({ ucell *_v; __asm__("movabs %1, %0" : "=r"(_v) : "i"(SPN_RP_VALUE)); _v; })
#define IMM_FN() ({ void *_v; __asm__("movabs %1, %0" : "=r"(_v) : "i"(SPN_FN_VALUE)); _v; })
/* A fourth 64-bit hole, for READ and WRITE: the engine's I/O helper,
   spn_io(op, c-addr, u) - 0 writes, 1 reads - so native code shares the
   interpreter's buffers instead of crossing into it for every byte. */
#define SPN_IO_VALUE 0x4ea1ed5ea1ed5e44LL
#define IMM_IO() ({ spn_io_fn _v; __asm__("movabs %1, %0" : "=r"(_v) : "i"(SPN_IO_VALUE)); _v; })
#define IMM() ({ cell _v; __asm__("movabs %1, %0" : "=r"(_v) : "i"(SPN_IMM_VALUE)); _v; })
#elif defined(__arm__)
/* 32-bit ARM (Iteration 30): no 64-bit immediate, and none folded into an
   instruction - every hole is a movw/movt pair, which the patcher finds by
   its two 16-bit halves and refills. One pair per hole, each value its own,
   so each is found unambiguously; IMM32 is a hole like the rest. */
#define SPN_IMM_VALUE   0x5ea1ed01
#define SPN_RP_VALUE    0x7ea1ed02
#define SPN_FN_VALUE    0x6ea1ed03
#define SPN_IO_VALUE    0x4ea1ed04
#define SPN_IMM32_VALUE 0x3c1a5e77
#define HOLE(type, v) ({ type _v; __asm__("movw %0, %1\n\tmovt %0, %2" : "=r"(_v) \
                         : "i"((v) & 0xffff), "i"(((unsigned)(v) >> 16) & 0xffff)); _v; })
#define IMM()    HOLE(cell, SPN_IMM_VALUE)
#define IMM32    HOLE(cell, SPN_IMM32_VALUE)
#define IMM_RP() HOLE(ucell *, SPN_RP_VALUE)
#define IMM_FN() HOLE(void *, SPN_FN_VALUE)
#define IMM_IO() HOLE(spn_io_fn, SPN_IO_VALUE)
#endif

/* The markers. Only DECLARED here, and defined in spn-markers.c. That is
   deliberate: if the compiler can see a marker's body it learns the
   marker never returns, clones it, strips its arguments and turns the tail
   jumps into calls - every one of which breaks the stencil. Declared
   extern, a marker is an opaque function and each call to it compiles to
   the plain relative jump or call the patcher expects. */
extern spn_st spn_next(cell *sp, cell tos);
extern spn_st spn_jump(cell *sp, cell tos);
extern spn_st spn_call(cell *sp, cell tos);

#define S(name) __attribute__((noinline, used)) spn_st name(cell *sp, cell tos)
#define GO(sp, tos) return spn_next(sp, tos)

S(st_lit)   { *--sp = tos; GO(sp, IMM()); }
S(st_dup)   { *--sp = tos; GO(sp, tos); }
S(st_drop)  { GO(sp + 1, *sp); }
S(st_swap)  { cell t = *sp; *sp = tos; GO(sp, t); }
S(st_over)  { cell t = *sp; *--sp = tos; GO(sp, t); }
S(st_rot)   { cell a = sp[1], b = sp[0]; sp[1] = b; sp[0] = tos; GO(sp, a); }
S(st_plus)  { GO(sp + 1, tos + *sp); }
S(st_addi)  { GO(sp, tos + IMM()); }
S(st_eq)    { GO(sp + 1, -(*sp == tos)); }
S(st_gt)    { GO(sp + 1, -(*sp > tos)); }
S(st_lt)    { GO(sp + 1, -(*sp < tos)); }
S(st_xor)   { GO(sp + 1, tos ^ *sp); }
S(st_and)   { GO(sp + 1, tos & *sp); }
S(st_negate){ GO(sp, -tos); }

S(st_addi32) { GO(sp, tos + IMM32); }

/* DUP n < IF, fused. IF jumps when the flag is FALSE - when NOT tos < n,
   which is tos > n-1 - so the translator patches in n-1. Written as a
   strict > on purpose: given tos >= C the compiler emits cmp $(C-1),
   moving the constant, and the hole would no longer be found. The
   comparison, the branch and the DUP that feeds it become one cmp and
   one conditional jump, with nothing written to the stack. */
S(st_dup_gti_br) { if (tos > IMM32) return spn_jump(sp, tos); GO(sp, tos); }

/* ?BRANCH fused with the operation that makes its flag: one compare and
   one conditional jump, no flag made and then tested. Each jumps where the
   pair would - when the flag would have been zero - and leaves the stack
   as the pair would. What feeds ?BRANCH, measured on the CV8 interpreter
   (kernel, corpus, parse): 0= about 3% of everything dispatched, DUP 1-2%,
   U< and = around 1%, then -, n= and OR. */
#if SPN_FUSED_BR     /* s8 only: s7's engine scans the whole table at boot, and
                       these would cost it time for stencils it never uses */
S(st_nz_br)  { cell f = tos; tos = *sp++;                   /* 0= IF: jump if non-zero */
               if (f != 0) return spn_jump(sp, tos); GO(sp, tos); }
S(st_dup_br) { if (tos == 0) return spn_jump(sp, tos); GO(sp, tos); }   /* DUP IF */
S(st_ne_br)  { cell a = sp[0], b = tos; tos = sp[1]; sp += 2;           /* = IF */
               if (a != b) return spn_jump(sp, tos); GO(sp, tos); }
S(st_uge_br) { ucell a = (ucell)sp[0], b = (ucell)tos; tos = sp[1]; sp += 2;  /* U< IF */
               if (a >= b) return spn_jump(sp, tos); GO(sp, tos); }
S(st_ge_br)  { cell a = sp[0], b = tos; tos = sp[1]; sp += 2;           /* < IF */
               if (a >= b) return spn_jump(sp, tos); GO(sp, tos); }
S(st_nei_br) { cell f = tos; tos = *sp++;                   /* n= IF, n in the 32-bit hole */
               if (f != IMM32) return spn_jump(sp, tos); GO(sp, tos); }
S(st_eq_br)  { cell a = sp[0], b = tos; tos = sp[1]; sp += 2;           /* - IF: jump if equal */
               if (a == b) return spn_jump(sp, tos); GO(sp, tos); }
S(st_or_br)  { cell x = sp[0] | tos; tos = sp[1]; sp += 2;              /* OR IF */
               if (x == 0) return spn_jump(sp, tos); GO(sp, tos); }
#endif

/* ?BRANCH: take the flag, then either fall through or jump. */
S(st_0branch) {
    cell f = tos; tos = *sp++;
    if (f == 0) return spn_jump(sp, tos);
    GO(sp, tos);
}
S(st_branch) { return spn_jump(sp, tos); }

/* A call to another native word, which hands back the new stack state. */
S(st_call)  { spn_st r = spn_call(sp, tos); GO(SPN_SP(r), SPN_TOS(r)); }

/* EXIT: leave the native word, returning the state to the caller. */
__attribute__((noinline, used)) spn_st st_exit(cell *sp, cell tos)
{ return SPN_ST(sp, tos); }

/* The return stack. The interpreter and native code share one, reached
   through the engine's own pointer - so a >R in native code and an R>
   in an interpreted word that it calls see the same stack. */
S(st_tor)    { ucell *rpp = IMM_RP(); ucell r = *rpp - sizeof(cell);
               *(cell *)r = tos; *rpp = r; GO(sp + 1, *sp); }
S(st_fromr)  { ucell *rpp = IMM_RP(); ucell r = *rpp; cell v = *(cell *)r;
               *rpp = r + sizeof(cell); *--sp = tos; GO(sp, v); }
S(st_rfetch) { ucell *rpp = IMM_RP(); cell v = *(cell *)*rpp;
               *--sp = tos; GO(sp, v); }

/* Memory, and the rest of the arithmetic. Unsigned where the engine is:
   its cells are UNS64, so U<, LSHIFT and RSHIFT must be too. */
S(st_fetch)  { GO(sp, *(cell *)tos); }
S(st_store)  { *(cell *)tos = *sp; GO(sp + 2, sp[1]); }
S(st_cfetch) { GO(sp, *(uint8_t *)tos); }
S(st_cstore) { *(uint8_t *)tos = (uint8_t)*sp; GO(sp + 2, sp[1]); }
S(st_or)     { GO(sp + 1, tos | *sp); }
S(st_ult)    { GO(sp + 1, -(cell)((ucell)*sp < (ucell)tos)); }
S(st_lshift) { GO(sp + 1, (cell)((ucell)*sp << tos)); }
S(st_rshift) { GO(sp + 1, (cell)((ucell)*sp >> tos)); }

/* Call a word that has no native code: run it in the interpreter and
   come back. Both holes are absolute - the helper lives in the engine,
   which can be further from this code than a 32-bit jump reaches. */
typedef spn_st (*spn_interp_fn)(cell *, cell, cell);
S(st_interp) { spn_st r = ((spn_interp_fn)IMM_FN())(sp, tos, IMM()); GO(SPN_SP(r), SPN_TOS(r)); }

/* DO loops, on the shared return stack in the kernel's own layout: the
   index on top, the limit under it. Exactly the arithmetic of (LOOP) and
   (+LOOP) in kernel.4 - +LOOP exits when old-limit and new-limit differ
   in sign - but done UNSIGNED, since C leaves signed overflow undefined
   and a Forth loop counter must wrap. There is no return address between
   a native loop's parameters and an enclosing loop's, so J is rp[2];
   interpreted J adds a cell for its own return address. */
S(st_do)     { ucell *rpp = IMM_RP(); cell *r = (cell *)*rpp - 2;
               r[1] = *sp; r[0] = tos; *rpp = (ucell)r; GO(sp + 2, sp[1]); }
S(st_qdo)    { if (*sp == tos) return spn_jump(sp + 2, sp[1]);
               ucell *rpp = IMM_RP(); cell *r = (cell *)*rpp - 2;
               r[1] = *sp; r[0] = tos; *rpp = (ucell)r; GO(sp + 2, sp[1]); }
S(st_loop)   { ucell *rpp = IMM_RP(); cell *r = (cell *)*rpp;
               ucell ix = (ucell)r[0] + 1;
               if (ix == (ucell)r[1]) { *rpp = (ucell)(r + 2); GO(sp, tos); }
               r[0] = (cell)ix; return spn_jump(sp, tos); }
S(st_ploop)  { ucell *rpp = IMM_RP(); cell *r = (cell *)*rpp;
               ucell o = (ucell)r[0], l = (ucell)r[1], n = o + (ucell)tos;
               if ((cell)((o - l) ^ (n - l)) < 0) { *rpp = (ucell)(r + 2); GO(sp + 1, *sp); }
               r[0] = (cell)n; return spn_jump(sp + 1, *sp); }
S(st_i)      { ucell *rpp = IMM_RP(); cell v = ((cell *)*rpp)[0]; *--sp = tos; GO(sp, v); }
S(st_j)      { ucell *rpp = IMM_RP(); cell v = ((cell *)*rpp)[2]; *--sp = tos; GO(sp, v); }
S(st_unloop) { ucell *rpp = IMM_RP(); *rpp += 2 * sizeof(cell); GO(sp, tos); }
S(st_leave)  { ucell *rpp = IMM_RP(); *rpp += 2 * sizeof(cell); return spn_jump(sp, tos); }

/* PICK. In the kernel it is built on SP@, which native code cannot use,
   so it was refused - and every native PICK went through the re-entry
   trampoline. In the native layout it is one load: tos is u, sp[0] is
   x0, and xu is sp[u]. */
S(st_pick)   { GO(sp, sp[tos]); }

/* The table the Forth side reads. Order matters: SPN-TABLE hands it over
   as-is, and forth/spn.4 names the entries by position. */
#if SPN_IO
/* WRITE ( c-addr u --- ) and READ ( c-addr u1 --- u2 ): one call to the
   engine's helper. A real call, so unlike every other stencil these use
   the machine stack - the compiler saves sp across it itself. */
S(st_write) { spn_io_fn f = IMM_IO(); f(0, *sp, tos); GO(sp + 2, sp[1]); }
S(st_read)  { spn_io_fn f = IMM_IO(); cell n = f(1, *sp, tos); GO(sp + 1, n); }
#endif
const void *const spn_table[] = {
    (const void *)spn_next, (const void *)spn_jump, (const void *)spn_call,
    (const void *)st_lit, (const void *)st_dup, (const void *)st_drop,
    (const void *)st_swap, (const void *)st_over, (const void *)st_rot,
    (const void *)st_plus, (const void *)st_addi, (const void *)st_eq,
    (const void *)st_gt, (const void *)st_lt, (const void *)st_xor,
    (const void *)st_and, (const void *)st_negate, (const void *)st_0branch,
    (const void *)st_branch, (const void *)st_call, (const void *)st_exit,
    (const void *)st_addi32, (const void *)st_dup_gti_br,
    (const void *)st_tor, (const void *)st_fromr, (const void *)st_rfetch,
    (const void *)st_fetch, (const void *)st_store, (const void *)st_cfetch,
    (const void *)st_cstore, (const void *)st_or, (const void *)st_ult,
    (const void *)st_lshift, (const void *)st_rshift, (const void *)st_interp,
    (const void *)st_do, (const void *)st_qdo, (const void *)st_loop,
    (const void *)st_ploop, (const void *)st_i, (const void *)st_j,
    (const void *)st_unloop, (const void *)st_leave, (const void *)st_pick,
#if SPN_FUSED_BR     /* 44- : s8's; appended, so the first 44 keep their numbers */
    (const void *)st_nz_br, (const void *)st_dup_br, (const void *)st_ne_br,
    (const void *)st_uge_br, (const void *)st_ge_br, (const void *)st_nei_br,
    (const void *)st_eq_br, (const void *)st_or_br,
#endif
#if SPN_IO           /* 52- : WRITE, READ - after the fused ones, numbers kept */
    (const void *)st_write, (const void *)st_read,
#endif
};
const int spn_table_len = sizeof spn_table / sizeof spn_table[0];

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

typedef int64_t cell;
typedef struct { cell *sp; cell tos; } spn_st;     /* returned in rax:rdx */

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
#define IMM_RP() ({ uint64_t *_v; __asm__("movabs %1, %0" : "=r"(_v) : "i"(SPN_RP_VALUE)); _v; })
#define IMM_FN() ({ void *_v; __asm__("movabs %1, %0" : "=r"(_v) : "i"(SPN_FN_VALUE)); _v; })
#define IMM() ({ cell _v; __asm__("movabs %1, %0" : "=r"(_v) : "i"(SPN_IMM_VALUE)); _v; })

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

/* ?BRANCH: take the flag, then either fall through or jump. */
S(st_0branch) {
    cell f = tos; tos = *sp++;
    if (f == 0) return spn_jump(sp, tos);
    GO(sp, tos);
}
S(st_branch) { return spn_jump(sp, tos); }

/* A call to another native word, which hands back the new stack state. */
S(st_call)  { spn_st r = spn_call(sp, tos); GO(r.sp, r.tos); }

/* EXIT: leave the native word, returning the state to the caller. */
__attribute__((noinline, used)) spn_st st_exit(cell *sp, cell tos)
{ spn_st r = { sp, tos }; return r; }

/* The return stack. The interpreter and native code share one, reached
   through the engine's own pointer - so a >R in native code and an R>
   in an interpreted word that it calls see the same stack. */
S(st_tor)    { uint64_t *rpp = IMM_RP(); uint64_t r = *rpp - 8;
               *(cell *)r = tos; *rpp = r; GO(sp + 1, *sp); }
S(st_fromr)  { uint64_t *rpp = IMM_RP(); uint64_t r = *rpp; cell v = *(cell *)r;
               *rpp = r + 8; *--sp = tos; GO(sp, v); }
S(st_rfetch) { uint64_t *rpp = IMM_RP(); cell v = *(cell *)*rpp;
               *--sp = tos; GO(sp, v); }

/* Memory, and the rest of the arithmetic. Unsigned where the engine is:
   its cells are UNS64, so U<, LSHIFT and RSHIFT must be too. */
S(st_fetch)  { GO(sp, *(cell *)tos); }
S(st_store)  { *(cell *)tos = *sp; GO(sp + 2, sp[1]); }
S(st_cfetch) { GO(sp, *(uint8_t *)tos); }
S(st_cstore) { *(uint8_t *)tos = (uint8_t)*sp; GO(sp + 2, sp[1]); }
S(st_or)     { GO(sp + 1, tos | *sp); }
S(st_ult)    { GO(sp + 1, -(cell)((uint64_t)*sp < (uint64_t)tos)); }
S(st_lshift) { GO(sp + 1, (cell)((uint64_t)*sp << tos)); }
S(st_rshift) { GO(sp + 1, (cell)((uint64_t)*sp >> tos)); }

/* Call a word that has no native code: run it in the interpreter and
   come back. Both holes are absolute - the helper lives in the engine,
   which can be further from this code than a 32-bit jump reaches. */
typedef spn_st (*spn_interp_fn)(cell *, cell, cell);
S(st_interp) { spn_st r = ((spn_interp_fn)IMM_FN())(sp, tos, IMM()); GO(r.sp, r.tos); }

/* DO loops, on the shared return stack in the kernel's own layout: the
   index on top, the limit under it. Exactly the arithmetic of (LOOP) and
   (+LOOP) in kernel.4 - +LOOP exits when old-limit and new-limit differ
   in sign - but done UNSIGNED, since C leaves signed overflow undefined
   and a Forth loop counter must wrap. There is no return address between
   a native loop's parameters and an enclosing loop's, so J is rp[2];
   interpreted J adds a cell for its own return address. */
S(st_do)     { uint64_t *rpp = IMM_RP(); cell *r = (cell *)*rpp - 2;
               r[1] = *sp; r[0] = tos; *rpp = (uint64_t)r; GO(sp + 2, sp[1]); }
S(st_qdo)    { if (*sp == tos) return spn_jump(sp + 2, sp[1]);
               uint64_t *rpp = IMM_RP(); cell *r = (cell *)*rpp - 2;
               r[1] = *sp; r[0] = tos; *rpp = (uint64_t)r; GO(sp + 2, sp[1]); }
S(st_loop)   { uint64_t *rpp = IMM_RP(); cell *r = (cell *)*rpp;
               uint64_t ix = (uint64_t)r[0] + 1;
               if (ix == (uint64_t)r[1]) { *rpp = (uint64_t)(r + 2); GO(sp, tos); }
               r[0] = (cell)ix; return spn_jump(sp, tos); }
S(st_ploop)  { uint64_t *rpp = IMM_RP(); cell *r = (cell *)*rpp;
               uint64_t o = (uint64_t)r[0], l = (uint64_t)r[1], n = o + (uint64_t)tos;
               if ((int64_t)((o - l) ^ (n - l)) < 0) { *rpp = (uint64_t)(r + 2); GO(sp + 1, *sp); }
               r[0] = (cell)n; return spn_jump(sp + 1, *sp); }
S(st_i)      { uint64_t *rpp = IMM_RP(); cell v = ((cell *)*rpp)[0]; *--sp = tos; GO(sp, v); }
S(st_j)      { uint64_t *rpp = IMM_RP(); cell v = ((cell *)*rpp)[2]; *--sp = tos; GO(sp, v); }
S(st_unloop) { uint64_t *rpp = IMM_RP(); *rpp += 16; GO(sp, tos); }
S(st_leave)  { uint64_t *rpp = IMM_RP(); *rpp += 16; return spn_jump(sp, tos); }

/* PICK. In the kernel it is built on SP@, which native code cannot use,
   so it was refused - and every native PICK went through the re-entry
   trampoline. In the native layout it is one load: tos is u, sp[0] is
   x0, and xu is sp[u]. */
S(st_pick)   { GO(sp, sp[tos]); }

/* The table the Forth side reads. Order matters: SPN-TABLE hands it over
   as-is, and forth/spn.4 names the entries by position. */
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
};
const int spn_table_len = sizeof spn_table / sizeof spn_table[0];

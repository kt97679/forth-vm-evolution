/* gen-jitk.py 3 - the stack-cache stencils (Iteration 259). Generated: do not edit. */
typedef spn_st (*spn_next4_fn)(cell *, cell, cell, cell);
#define SK(name) __attribute__((noinline, used)) spn_st name(cell *sp, cell t0, cell t1, cell t2)
/* the next stencil, the cached cells in the third and fourth argument registers: the JIT
   finds this jump as it finds GO's - its target is exactly spn_next */
#define GO4(sp, a, b, c) return ((spn_next4_fn)(void *)spn_next)(sp, a, b, c)
SK(stk_lit_0) { cell v0 = IMM(); GO4(sp, v0, t1, t2); }
SK(stk_lit_1) { cell v0 = IMM(); GO4(sp, v0, t0, t2); }
SK(stk_lit_2) { cell v0 = IMM(); GO4(sp, v0, t0, t1); }
SK(stk_lit_3) { cell v0 = IMM(); *--sp = t2; GO4(sp, v0, t0, t1); }
SK(stk_dup_0) { cell m0 = *sp++; cell v0 = m0; cell v1 = m0; GO4(sp, v0, v1, t2); }
SK(stk_dup_1) { cell v0 = t0; cell v1 = t0; GO4(sp, v0, v1, t2); }
SK(stk_dup_2) { cell v0 = t0; cell v1 = t0; GO4(sp, v0, v1, t1); }
SK(stk_dup_3) { cell v0 = t0; cell v1 = t0; *--sp = t2; GO4(sp, v0, v1, t1); }
SK(stk_drop_0) { cell m0 = *sp++; GO4(sp, t0, t1, t2); }
SK(stk_drop_1) {  GO4(sp, t0, t1, t2); }
SK(stk_drop_2) {  GO4(sp, t1, t1, t2); }
SK(stk_drop_3) {  GO4(sp, t1, t2, t2); }
SK(stk_swap_0) { cell m0 = *sp++; cell m1 = *sp++; cell v0 = m1; cell v1 = m0; GO4(sp, v0, v1, t2); }
SK(stk_swap_1) { cell m0 = *sp++; cell v0 = m0; cell v1 = t0; GO4(sp, v0, v1, t2); }
SK(stk_swap_2) { cell v0 = t1; cell v1 = t0; GO4(sp, v0, v1, t2); }
SK(stk_swap_3) { cell v0 = t1; cell v1 = t0; GO4(sp, v0, v1, t2); }
SK(stk_over_0) { cell m0 = *sp++; cell m1 = *sp++; cell v0 = m1; cell v1 = m0; cell v2 = m1; GO4(sp, v0, v1, v2); }
SK(stk_over_1) { cell m0 = *sp++; cell v0 = m0; cell v1 = t0; cell v2 = m0; GO4(sp, v0, v1, v2); }
SK(stk_over_2) { cell v0 = t1; cell v1 = t0; cell v2 = t1; GO4(sp, v0, v1, v2); }
SK(stk_over_3) { cell v0 = t1; cell v1 = t0; cell v2 = t1; *--sp = t2; GO4(sp, v0, v1, v2); }
SK(stk_plus_0) { cell m0 = *sp++; cell m1 = *sp++; cell v0 = (m1 + m0); GO4(sp, v0, t1, t2); }
SK(stk_plus_1) { cell m0 = *sp++; cell v0 = (m0 + t0); GO4(sp, v0, t1, t2); }
SK(stk_plus_2) { cell v0 = (t1 + t0); GO4(sp, v0, t1, t2); }
SK(stk_plus_3) { cell v0 = (t1 + t0); GO4(sp, v0, t2, t2); }
SK(stk_addi_0) { cell m0 = *sp++; cell v0 = (m0 + IMM()); GO4(sp, v0, t1, t2); }
SK(stk_addi_1) { cell v0 = (t0 + IMM()); GO4(sp, v0, t1, t2); }
SK(stk_addi_2) { cell v0 = (t0 + IMM()); GO4(sp, v0, t1, t2); }
SK(stk_addi_3) { cell v0 = (t0 + IMM()); GO4(sp, v0, t1, t2); }
SK(stk_eq_0) { cell m0 = *sp++; cell m1 = *sp++; cell v0 = -(cell)(m1 == m0); GO4(sp, v0, t1, t2); }
SK(stk_eq_1) { cell m0 = *sp++; cell v0 = -(cell)(m0 == t0); GO4(sp, v0, t1, t2); }
SK(stk_eq_2) { cell v0 = -(cell)(t1 == t0); GO4(sp, v0, t1, t2); }
SK(stk_eq_3) { cell v0 = -(cell)(t1 == t0); GO4(sp, v0, t2, t2); }
SK(stk_gt_0) { cell m0 = *sp++; cell m1 = *sp++; cell v0 = -(cell)(m1 > m0); GO4(sp, v0, t1, t2); }
SK(stk_gt_1) { cell m0 = *sp++; cell v0 = -(cell)(m0 > t0); GO4(sp, v0, t1, t2); }
SK(stk_gt_2) { cell v0 = -(cell)(t1 > t0); GO4(sp, v0, t1, t2); }
SK(stk_gt_3) { cell v0 = -(cell)(t1 > t0); GO4(sp, v0, t2, t2); }
SK(stk_lt_0) { cell m0 = *sp++; cell m1 = *sp++; cell v0 = -(cell)(m1 < m0); GO4(sp, v0, t1, t2); }
SK(stk_lt_1) { cell m0 = *sp++; cell v0 = -(cell)(m0 < t0); GO4(sp, v0, t1, t2); }
SK(stk_lt_2) { cell v0 = -(cell)(t1 < t0); GO4(sp, v0, t1, t2); }
SK(stk_lt_3) { cell v0 = -(cell)(t1 < t0); GO4(sp, v0, t2, t2); }
SK(stk_and_0) { cell m0 = *sp++; cell m1 = *sp++; cell v0 = (m1 & m0); GO4(sp, v0, t1, t2); }
SK(stk_and_1) { cell m0 = *sp++; cell v0 = (m0 & t0); GO4(sp, v0, t1, t2); }
SK(stk_and_2) { cell v0 = (t1 & t0); GO4(sp, v0, t1, t2); }
SK(stk_and_3) { cell v0 = (t1 & t0); GO4(sp, v0, t2, t2); }
SK(stk_xor_0) { cell m0 = *sp++; cell m1 = *sp++; cell v0 = (m1 ^ m0); GO4(sp, v0, t1, t2); }
SK(stk_xor_1) { cell m0 = *sp++; cell v0 = (m0 ^ t0); GO4(sp, v0, t1, t2); }
SK(stk_xor_2) { cell v0 = (t1 ^ t0); GO4(sp, v0, t1, t2); }
SK(stk_xor_3) { cell v0 = (t1 ^ t0); GO4(sp, v0, t2, t2); }
SK(stk_fetch_0) { cell m0 = *sp++; cell v0 = *(cell *)m0; GO4(sp, v0, t1, t2); }
SK(stk_fetch_1) { cell v0 = *(cell *)t0; GO4(sp, v0, t1, t2); }
SK(stk_fetch_2) { cell v0 = *(cell *)t0; GO4(sp, v0, t1, t2); }
SK(stk_fetch_3) { cell v0 = *(cell *)t0; GO4(sp, v0, t1, t2); }
SK(stk_store_0) { cell m0 = *sp++; cell m1 = *sp++; *(cell *)m0 = m1; GO4(sp, t0, t1, t2); }
SK(stk_store_1) { cell m0 = *sp++; *(cell *)t0 = m0; GO4(sp, t0, t1, t2); }
SK(stk_store_2) { *(cell *)t0 = t1; GO4(sp, t0, t1, t2); }
SK(stk_store_3) { *(cell *)t0 = t1; GO4(sp, t2, t1, t2); }
SK(stk_cfetch_0) { cell m0 = *sp++; cell v0 = (cell)*(uint8_t *)m0; GO4(sp, v0, t1, t2); }
SK(stk_cfetch_1) { cell v0 = (cell)*(uint8_t *)t0; GO4(sp, v0, t1, t2); }
SK(stk_cfetch_2) { cell v0 = (cell)*(uint8_t *)t0; GO4(sp, v0, t1, t2); }
SK(stk_cfetch_3) { cell v0 = (cell)*(uint8_t *)t0; GO4(sp, v0, t1, t2); }
SK(stk_i_0) { cell *rr_ = (cell *)RP_VALUE(); cell v0 = rr_[0]; GO4(sp, v0, t1, t2); }
SK(stk_i_1) { cell *rr_ = (cell *)RP_VALUE(); cell v0 = rr_[0]; GO4(sp, v0, t0, t2); }
SK(stk_i_2) { cell *rr_ = (cell *)RP_VALUE(); cell v0 = rr_[0]; GO4(sp, v0, t0, t1); }
SK(stk_i_3) { cell *rr_ = (cell *)RP_VALUE(); cell v0 = rr_[0]; *--sp = t2; GO4(sp, v0, t0, t1); }
SK(stk_canon_0) { cell t = *sp++; GO4(sp, t, t1, t2); }
SK(stk_canon_2) { *--sp = t1; GO4(sp, t0, t1, t2); }
SK(stk_canon_3) { *--sp = t2; *--sp = t1; GO4(sp, t0, t1, t2); }
const void *const spn_ktable[] = {
    (const void *)stk_lit_0,
    (const void *)stk_lit_1,
    (const void *)stk_lit_2,
    (const void *)stk_lit_3,
    (const void *)stk_dup_0,
    (const void *)stk_dup_1,
    (const void *)stk_dup_2,
    (const void *)stk_dup_3,
    (const void *)stk_drop_0,
    (const void *)stk_drop_1,
    (const void *)stk_drop_2,
    (const void *)stk_drop_3,
    (const void *)stk_swap_0,
    (const void *)stk_swap_1,
    (const void *)stk_swap_2,
    (const void *)stk_swap_3,
    (const void *)stk_over_0,
    (const void *)stk_over_1,
    (const void *)stk_over_2,
    (const void *)stk_over_3,
    (const void *)stk_plus_0,
    (const void *)stk_plus_1,
    (const void *)stk_plus_2,
    (const void *)stk_plus_3,
    (const void *)stk_addi_0,
    (const void *)stk_addi_1,
    (const void *)stk_addi_2,
    (const void *)stk_addi_3,
    (const void *)stk_eq_0,
    (const void *)stk_eq_1,
    (const void *)stk_eq_2,
    (const void *)stk_eq_3,
    (const void *)stk_gt_0,
    (const void *)stk_gt_1,
    (const void *)stk_gt_2,
    (const void *)stk_gt_3,
    (const void *)stk_lt_0,
    (const void *)stk_lt_1,
    (const void *)stk_lt_2,
    (const void *)stk_lt_3,
    (const void *)stk_and_0,
    (const void *)stk_and_1,
    (const void *)stk_and_2,
    (const void *)stk_and_3,
    (const void *)stk_xor_0,
    (const void *)stk_xor_1,
    (const void *)stk_xor_2,
    (const void *)stk_xor_3,
    (const void *)stk_fetch_0,
    (const void *)stk_fetch_1,
    (const void *)stk_fetch_2,
    (const void *)stk_fetch_3,
    (const void *)stk_store_0,
    (const void *)stk_store_1,
    (const void *)stk_store_2,
    (const void *)stk_store_3,
    (const void *)stk_cfetch_0,
    (const void *)stk_cfetch_1,
    (const void *)stk_cfetch_2,
    (const void *)stk_cfetch_3,
    (const void *)stk_i_0,
    (const void *)stk_i_1,
    (const void *)stk_i_2,
    (const void *)stk_i_3,
    (const void *)stk_canon_0,
    (const void *)stk_canon_2,
    (const void *)stk_canon_3
};
const int spn_ktable_len = 67;

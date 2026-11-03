/* gen-jitk.py 3 - the stack-cache map for engine/jit.c (Iteration 259). Generated. */
#define JITK_K 3
#define JITK_N 67
extern const void *const spn_ktable[];
extern const int spn_ktable_len;
/* a base stencil's variant for each entry state, as index + 1 into spn_ktable (0: none) */
static const unsigned char jitk_v1[S_N][JITK_K + 1] = {
    [S_LIT] = { 1, 2, 3, 4 },
    [S_DUP] = { 5, 6, 7, 8 },
    [S_DROP] = { 9, 10, 11, 12 },
    [S_SWAP] = { 13, 14, 15, 16 },
    [S_OVER] = { 17, 18, 19, 20 },
    [S_PLUS] = { 21, 22, 23, 24 },
    [S_ADDI] = { 25, 26, 27, 28 },
    [S_EQ] = { 29, 30, 31, 32 },
    [S_GT] = { 33, 34, 35, 36 },
    [S_LT] = { 37, 38, 39, 40 },
    [S_AND] = { 41, 42, 43, 44 },
    [S_XOR] = { 45, 46, 47, 48 },
    [S_FETCH] = { 49, 50, 51, 52 },
    [S_STORE] = { 53, 54, 55, 56 },
    [S_CFETCH] = { 57, 58, 59, 60 },
    [S_I] = { 61, 62, 63, 64 },
};
/* the state each variant leaves */
static const unsigned char jitk_vout[JITK_N] = { 1, 2, 3, 3, 2, 2, 3, 3, 0, 0, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 1, 1, 1, 2, 1, 1, 2, 3, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 3, 0, 0, 0, 1, 1, 1, 2, 3, 1, 2, 3, 3, 1, 1, 1 };
/* the canonicaliser from each state to state 1, as index + 1 (0: none - state 1 itself) */
static const unsigned char jitk_canon1[JITK_K + 1] = { 65, 0, 66, 67 };

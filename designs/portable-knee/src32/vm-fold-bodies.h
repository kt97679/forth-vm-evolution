LX_lit:     /* lit     */ PUSH(OPND16(ip)); ip += 2; EXITNEXT();
LX_drop:    /* drop    */ dsp += CELL_BYTES; EXITNEXT();
LX_fetch:   /* @       */ DS0 = CELL(DS0); EXITNEXT();
LX_xor:     /* xor     */ DS1 ^= DS0; dsp += CELL_BYTES; EXITNEXT();
LX_plus:    /* +       */ DS1 += DS0; dsp += CELL_BYTES; EXITNEXT();
LX_rshift:  /* rshift  */ DS1 >>= DS0; dsp += CELL_BYTES; EXITNEXT();

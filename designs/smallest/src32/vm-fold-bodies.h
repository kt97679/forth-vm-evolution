LX_lit:     /* lit     */ PUSH(OPND16(ip)); ip += 2; EXITNEXT();
LX_drop:    /* drop    */ dsp += CELL_BYTES; EXITNEXT();
LX_store:   /* !       */ CELL(DS0) = DS1; dsp += 2 * CELL_BYTES; EXITNEXT();
LX_plus:    /* +       */ DS1 += DS0; dsp += CELL_BYTES; EXITNEXT();

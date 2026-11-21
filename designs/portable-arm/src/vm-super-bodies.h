LS_0: /* @ + */
   /* @       */ DS0 = CELL(DS0); goto LSB_0;
LSB_0:
    /* +       */ DS1 += DS0; dsp += CELL_BYTES; NEXT();
LS_1: /* R> DROP */
   /* r>      */ PUSH(RS); rp += CELL_BYTES; goto LSB_1;
LSB_1:
    /* drop    */ dsp += CELL_BYTES; NEXT();

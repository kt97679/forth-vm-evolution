LS_0: /* + @ */
    /* +       */ DS1 += DS0; dsp += CELL_BYTES; goto LSB_0;
LSB_0:
   /* @       */ DS0 = CELL(DS0); NEXT();
LS_1: /* DUP >R */
     /* dup     */ PUSH(DS1); goto LSB_1;
LSB_1:
     /* >r      */ RPUSH(DS0); dsp += CELL_BYTES; NEXT();

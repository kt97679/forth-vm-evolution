LS_0: /* + @ */
    /* +       */ DS1 += DS0; dsp += CELL_BYTES; goto LSB_0;
LSB_0:
   /* @       */ DS0 = CELL(DS0); NEXT();
LS_1: /* DUP >R */
     /* dup     */ PUSH(DS1); goto LSB_1;
LSB_1:
     /* >r      */ RPUSH(DS0); dsp += CELL_BYTES; NEXT();
LS_2: /* C! R> */
  /* c!      */ BYTE(DS0) = (UNS8)DS1; dsp += 2 * CELL_BYTES; goto LSB_2;
LSB_2:
   /* r>      */ PUSH(RS); rp += CELL_BYTES; NEXT();
LS_3: /* >R C! */
     /* >r      */ RPUSH(DS0); dsp += CELL_BYTES; goto LSB_3;
LSB_3:
  /* c!      */ BYTE(DS0) = (UNS8)DS1; dsp += 2 * CELL_BYTES; NEXT();
LS_4: /* ROT DUP */
     /* rot     */ t = DS2; DS2 = DS1; DS1 = DS0; DS0 = t; goto LSB_4;
LSB_4:
     /* dup     */ PUSH(DS1); NEXT();
LS_5: /* R@ ROT */
  /* r@      */ PUSH(RS); goto LSB_5;
LSB_5:
     /* rot     */ t = DS2; DS2 = DS1; DS1 = DS0; DS0 = t; NEXT();

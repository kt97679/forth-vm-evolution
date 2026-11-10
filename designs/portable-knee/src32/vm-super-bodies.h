LS_0: /* OVER C@ */
 t = NOS; PUSHT(t); goto LSB_0;
LSB_0:
 tos = BYTE(tos); NEXT();
LS_1: /* + @ */
 tos += NOS; dsp += CELL_BYTES; goto LSB_1;
LSB_1:
 tos = CELL(tos); NEXT();
LS_2: /* @ + */
 tos = CELL(tos); goto LSB_2;
LSB_2:
 tos += NOS; dsp += CELL_BYTES; NEXT();

LS_0: /* + C! */
 tos += NOS; dsp += CELL_BYTES; goto LSB_0;
LSB_0:
 BYTE(tos) = (UNS8)NOS; tos = CELL(dsp + CELL_BYTES); dsp += 2 * CELL_BYTES; NEXT();

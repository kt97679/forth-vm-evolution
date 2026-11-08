LS_0: /* @ AND */
 tos = CELL(tos); goto LSB_0;
LSB_0:
 tos &= NOS; dsp += CELL_BYTES; NEXT();

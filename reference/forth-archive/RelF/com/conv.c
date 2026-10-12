#include <stdio.h>

#define  UNS8 unsigned char  /*     Virtual    */
#define UNS32 unsigned long  /* internal types */
#define CELL(reg) (*(UNS32*)(reg)) /* cell (word) memory access macros */
#define MEMSIZE 64 * 1024    /* how much memory do we allocate for VM */
UNS8 mem[MEMSIZE + 3];
UNS8 *base;

swap_mem(UNS32 start, UNS32 len) {
    UNS32 i, m;

    for (i = start & (-4); i < len + start; i += 4) {
        m = CELL(i);
        m = (m >> 16) | (m << 16);
        m = ((m & 0xff00ff00) >> 8) | ((m & 0x00ff00ff) << 8);
        CELL(i) = m;
    }
}

load_image(char *name, char *name2) {
    UNS32 len;
    FILE *infile, *outfile;

    if ((infile = fopen(name, "rb")) == NULL) {
        fprintf(stderr, "Cannot open input file.\n");
        exit(2);
    }
    base = (UNS8*)(((UNS32)mem + 3) & (-4));
    len = fread(base, 1, MEMSIZE, infile);
    swap_mem((UNS32)base, len);
    if ((outfile = fopen(name2, "wb")) == NULL) {
        fprintf(stderr, "Cannot open output file.\n");
        exit(2);
    }
    fwrite(base, 1, len, outfile);
}

main(int argc,char **argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: conv <filename1> <filename2>\n");
    } else {
        load_image(argv[1], argv[2]);
    }
    return 0;
}

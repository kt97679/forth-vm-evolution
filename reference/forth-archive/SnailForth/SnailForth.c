/* SOD32 the Stack Oriented Design computer.
   Copyright 1994, L.C. Benschop, Eindhoven, The Netherlands.
   The program is released under the GNU General Public License version 2.
   There is NO WARRANTY.
*/

#include <stdio.h>

#define UNS8  unsigned char
#define INT32 int
#define UNS32 unsigned int

#define MEMSIZE 1024 * 1024 /* must be a power of two */
#define MEMMASK MEMSIZE - 1 /* mask for addresses to force them into range */

UNS8 mem[MEMSIZE];
UNS32 count[32];

#define CELL(reg) (*(UNS32*)(mem + ((reg) & MEMMASK)))
#define CELLMASK (~3)
#define sp CELL(0)
#define rp CELL(4)

#ifdef BIG_ENDIAN
    #define BYTEMASK 0
#else
    #define BYTEMASK 3
#endif

#define BYTE(reg) mem[((reg) & MEMMASK) ^ BYTEMASK]

#define SWAP swap_mem(addr&CELLMASK,len+3);
#define CLIP addr&=MEMMASK;len&=MEMMASK;if(addr+len>MEMSIZE)len=MEMSIZE-addr;
#define FILEID(n) if((n)>=20){ior=-201;goto end;}if(!fileids[n])\
                  {ior=-201;goto end;} fp=fileids[n];

char *filemodes[]={"r", "rb", "w", "wb", "r+", "r+b"};

char filename[256];

void report(void) {
    FILE *dfp;
    int i;
    dfp = fopen("report", "w");
    if (dfp == NULL) {
        printf("Can't open report file\n");
        return;
    }
    for (i = 0; i < 32; i++) {
        fprintf(dfp, "%d %d\n", i, count[i]);
    }
    fclose(dfp);
}

/* Perform byte swap of 32-bit words in region of memory of virtual machine*/
void swap_mem(UNS32 start,UNS32 len) {
#ifndef BIG_ENDIAN
    UNS32 i,m;
    for (i = 0; i < len; i += 4) {
        m = CELL(start + i);
        m = (m >> 16) | (m << 16);
        m = ((m & 0xff00ff00) >> 8) | ((m & 0x00ff00ff) << 8);
        CELL(start + i) = m;
    }
#endif
}

void do_os(void)
{
 UNS32 addr,len,ior=0;
 int res;
 static FILE *fileids[20];
 FILE *fp;
 UNS32 code=CELL(sp);sp+=4;
 switch(code) {
  case 0: /*exit*/ 
//    echo();
//    endwin();
    report();
    exit(0);
    break;
  case 1: /*read char */ sp-=4;
//    CELL(sp)=wgetch(stdscr);
    CELL(sp)=getchar();
    break;
  case 2: /*print char*/ putchar(CELL(sp));sp+=4;break;
  case 7: /*open-file*/  sp+=4;len=CELL(sp);addr=CELL(sp+4);
                         CLIP SWAP if(!make_name(mem+addr,len)) {ior=-202;
                         SWAP goto end;} SWAP
                         {
                          int i;
                          for(i=0;i<20;i++) {
                           if(!fileids[i])break;
                          }
                          if(i==20){ior=-201;goto end;}
                                                  if(CELL(sp-4)>5){ior=-203;goto end;}
                                                  fp=fopen(filename,filemodes[CELL(sp-4)]);
                          if(!fp)ior=200;
                          fileids[i]=fp;
                                                  CELL(sp+4)=i;
                                                 }goto end;
  case 8: /*close-file*/ FILEID(CELL(sp)) fclose(fp);
                                                 fileids[CELL(sp)]=0;
                        goto end;;
  case 9: /*write-line*/ sp+=8;FILEID(CELL(sp-8)) len=CELL(sp-4);
                                                 addr=CELL(sp);CLIP SWAP clearerr(fp);
                         fwrite(mem+addr,1,len,fp);SWAP
                         fputc('\n',fp);if(ferror(fp))ior=-200;
                         goto end;
  case 10: /*read-line*/ FILEID(CELL(sp)) len=CELL(sp+4)+2;
                                                 addr=CELL(sp+8);CLIP SWAP
                         clearerr(fp);
                         fgets((char *)(mem+addr),len,fp);
                         if(ferror(fp)){ior=-200;SWAP goto end;}
                         res=strlen(mem+addr);
                                                 if(!res || feof(fp))CELL(sp+4)=0;
                         else {
                                                   CELL(sp+4)=0xffffffff;
                          if(*(mem+addr+res-1)=='\n') res--;
                         }
                                                 CELL(sp+8)=res;
                         SWAP goto end;
  case 11: /*write-file*/sp+=8;FILEID(CELL(sp-8)) len=CELL(sp-4);
                                                 addr=CELL(sp);CLIP SWAP clearerr(fp);
                         fwrite(mem+addr,1,len,fp);SWAP if(ferror(fp))ior=-200;
                         goto end;
  case 12: /*read-file*/ sp+=4;FILEID(CELL(sp-4)) len=CELL(sp);
                                                 addr=CELL(sp+4);CLIP SWAP  clearerr(fp);
                         res=fread(mem+addr,1,len,fp);SWAP
                                                 CELL(sp+4)=res;if(ferror(fp)) ior=-200;goto end;
  case 13: /*delete-file*/ sp+=4;len=CELL(sp-4);addr=CELL(sp);
                         CLIP SWAP if(!make_name(mem+addr,len)) {ior=-202;
                         SWAP goto end;} SWAP remove(filename); goto end;
  case 14: /*reposition-file*/ sp+=8;FILEID(CELL(sp-8))
                                                  fseek(fp,CELL(sp),SEEK_SET);goto end;

  case 15: /*file-position*/ sp-=8;FILEID(CELL(sp+8))
                                                  CELL(sp+8)=ftell(fp);CELL(sp+4)=0;
                          goto end;
  case 16: /*system */   sp+=4;len=CELL(sp-4);addr=CELL(sp);
                                                 CLIP SWAP if(!make_name(mem+addr,len)) {ior=-202;
                          SWAP goto end;} SWAP ior=system(filename); goto end;
  case 17: /* file-size*/ sp-=8;FILEID(CELL(sp+8))
                          {long oldpos;
                           oldpos=ftell(fp);
                           fseek(fp,0L,SEEK_END);
                                                   CELL(sp+8)=ftell(fp);CELL(sp+4)=0;
                           fseek(fp,oldpos,SEEK_SET);
                          }
                          goto end;
 } return;
 end: CELL(sp)=ior;
}

void virtual_machine(void) {
    register UNS32 ret, ip, ireg, t;
    for (t = 0; t < 32; t++) count[t] = 0;
    sp = MEMSIZE - 4;
    rp = MEMSIZE - 1024;
    ip = 32;
    while (1) {
        ireg = CELL(ip);
        ip += 4;
        if (!(ireg & 1)) {
            if (ireg & 2) /*jumpz*/ {
//                t = CELL(sp); sp += 4;
//                if (!t) ip = ireg & CELLMASK;
            } else /*call*/ {
                rp -= 4;
                CELL(rp) = ip;
                ip = ireg & CELLMASK;
            }
        } else {
            ret = ireg & 0x80000000;
            ireg = (ireg & 0x7fffffff) >> 1;
            do {
                count[ireg & 31]++;
                switch (ireg & 31) {
                    case 0: /* nop  */ break;
                    case 1: /* exit */ ip = (CELL(rp)) & CELLMASK; rp += 4; break;
                    case 7: /* @    */ CELL(sp) = CELL(CELL(sp) & CELLMASK); break;
                    case 17:/* um+  */ t = CELL(sp) + CELL(sp + 4); CELL(sp) = (t < CELL(sp)); CELL(sp + 4) = t; break;
                    case 19:/* io   */ do_os(); break;
                    case 23:/* !    */ sp += 8; CELL(CELL(sp - 8)) = CELL((sp - 4) & CELLMASK); break;
                    case 29:/* nand */ sp += 4; CELL(sp) = ~(CELL(sp) & CELL(sp - 4)); break;
                    case 31:/* lit  */ sp -= 4; CELL(sp) = CELL(ip); ip += 4; break;
                }
                ireg >>= 5;
            } while (ireg);
            if (ret)/*return*/ {
                ip = (CELL(rp)) & CELLMASK;
                rp += 4;
            }
        }
    }
}

int make_name(unsigned char *addr,UNS32 len)
{
 int i;
 for(i=0;i<len && i<256;i++) {
  filename[i]=addr[i];
  if(filename[i]=='/' || filename[i]=='\\' || filename[i]==':') return 0;
   /* Prohibit filenames in other directories */
 }
 filename[i]='\0';
 return 1;
}

load_image (char *name) {
    UNS32 len;
    FILE *infile;
    if ((infile = fopen(name, "rb")) == NULL) {
        fprintf(stderr, "Cannot open image file.\n");
        exit(2);
    }
    len = fread(mem, 1, MEMSIZE, infile);
    swap_mem(0, len);
}

main (int argc, char **argv) {
    if(argc<2) {
        fprintf(stderr, "Usage: sod32 <filename>\n");
        exit(1);
    }
    load_image(argv[1]);
    virtual_machine();
    return 0;
}

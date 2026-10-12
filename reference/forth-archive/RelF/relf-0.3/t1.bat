c:\bin\lcc\bin\lcc t2.c
nasmw -O9 -f win32 -l t1.lst -o t1.obj t1.asm
c:\bin\lcc\bin\lcclnk -o t2.exe t1.obj t2.obj
t2.exe
@nasmw -O9 -f win32 -l t3.lst -o t3.obj t3.asm
@c:\bin\lcc\bin\lcclnk -o t3.exe t3.obj
@t3.exe

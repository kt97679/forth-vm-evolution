rem @c:\bin\lcc\bin\lcc relf2.c
rem @nasmw -O9 -f win32 -l vm.lst -o vm.obj vm.asm
rem @c:\bin\lcc\bin\lcclnk -o relf2.exe relf2.obj vm.obj
@c:\bin\lcc\bin\lcc relf2.c
@c:\bin\lcc\bin\lcclnk -o relf2.exe relf2.obj

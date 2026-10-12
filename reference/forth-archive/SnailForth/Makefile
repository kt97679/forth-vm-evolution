CFLAGS= -O2  #-DBIG_ENDIAN
# Uncomment -DBIG_ENDIAN for big-endian processors (m68k etc)
CC=gcc

all: sod32

sod32: engine.o special.o main.o
	$(CC) -o sod32 engine.o special.o main.o -lcurses -ltermcap

engine.o: engine.c sod32.h

special.o: special.c sod32.h

main.o: main.c sod32.h


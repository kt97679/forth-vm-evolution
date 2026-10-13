#!/bin/sh
W=/tmp/rs4; rm -rf $W; mkdir -p $W; cd /tmp/b46
cc -O2 -o $W/relf-64 engine/relf.c
cp forth/kernel.4 forth/extend.4 forth/cross.4 $W/
sed 's/^8 TARGET-CELL-BYTES !/4 TARGET-CELL-BYTES !/' forth/cross.4 > $W/cross32.4
cd $W
xc() { cp "$1" kernel.img; printf 'S" extend.4" INCLUDED\nS" %s" INCLUDED\n' "$2" | ./relf-64 kernel.img > "$3.log" 2>&1; cp kernel.img "$3"; }
xc /tmp/b46/forth/kernel-seed.img cross.4 s1.img
xc /tmp/b46/forth/kernel-seed.img cross32.4 k32-old.img
xc s1.img cross32.4 k32-new.img

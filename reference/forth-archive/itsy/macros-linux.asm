%define link 0
%define immediate 080h

%macro head 4
%%link dd link
%define link %%link
%strlen %%count %1
db %3 + %%count,%1
xt_ %+ %2 dd %4
%endmacro

%macro primitive 2-3 0
head %1,%2,%3,$+4
%endmacro

%macro colon 2-3 0
head %1,%2,%3,docolon
%endmacro

%macro constant 3
head %1,%2,0,doconst
val_ %+ %2 dd %3
%endmacro

%macro variable 3
head %1,%2,0,dovar
val_ %+ %2 dd %3
%endmacro

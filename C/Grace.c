#include <stdio.h>
#define MAIN int main() {quine(SELF);return 0;};

#define quine(str) char var32 = 32;char var10 = 10;char var34 = 34;FILE *stream = fopen("Grace_kid.c","w"); fprintf(stream, str, var32, var10, var34, str); fclose(stream)
#define SELF "#include%1$c<stdio.h>%2$c#define%1$cMAIN%1$cint%1$cmain()%1$c{quine(SELF);return%1$c0;};%2$c%2$c#define%1$cquine(str)%1$cchar%1$cvar32%1$c=%1$c32;char%1$cvar10%1$c=%1$c10;char%1$cvar34%1$c=%1$c34;FILE%1$c*stream%1$c=%1$cfopen(%3$cGrace_kid.c%3$c,%3$cw%3$c);%1$cfprintf(stream,%1$cstr,%1$cvar32,%1$cvar10,%1$cvar34,%1$cstr);%1$cfclose(stream)%2$c#define%1$cSELF%1$c%3$c%4$s%3$c%2$c%2$c//This%1$cMAIN%1$cmacro%1$cruns%1$cthe%1$cprogram%2$cMAIN%2$c"

//This MAIN macro runs the program
MAIN

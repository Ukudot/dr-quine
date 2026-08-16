#include <stdio.h>

/*
 This comment is outside the main function
*/


void quine() {
	char var32 = 32;
	char var9 = 9;
	char var10 = 10;
	char var34 = 34;
	char *self = "#include%1$c<stdio.h>%3$c%3$c/*%3$c%1$cThis%1$ccomment%1$cis%1$coutside%1$cthe%1$cmain%1$cfunction%3$c*/%3$c%3$c%3$cvoid%1$cquine()%1$c{%3$c%2$cchar%1$cvar32%1$c=%1$c32;%3$c%2$cchar%1$cvar9%1$c=%1$c9;%3$c%2$cchar%1$cvar10%1$c=%1$c10;%3$c%2$cchar%1$cvar34%1$c=%1$c34;%3$c%2$cchar%1$c*self%1$c=%1$c%4$c%5$s%4$c;%3$c%3$c%2$cprintf(self,%1$cvar32,%1$cvar9,%1$cvar10,%1$cvar34,%1$cself);%3$c}%3$c%3$cint%1$cmain()%1$c{%3$c%2$cquine();%3$c%2$c/*%3$c%2$c%1$cThis%1$ccomment%1$cis%1$cinside%1$cthe%1$cmain%1$cfunction%3$c%2$c*/%3$c%2$creturn%1$c(0);%3$c};%3$c";

	printf(self, var32, var9, var10, var34, self);
}

int main() {
	quine();
	/*
	 This comment is inside the main function
	*/
	return (0);
};

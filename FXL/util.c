#include "util.h"

extern void outb(unsigned char value,unsigned short port);
extern unsigned char inb(unsigned short port);
extern unsigned short inw(unsigned short port);

void kmemcpy(void * dest,void * src,int n)
{
	//do stuff
	char *a = (char*)dest;
	char *b = (char*)src;
	while(n--)
	{
		//*a++=*b++;
		*a=*b;
		a++;
		b++;
	}
		
	//clearLine(23,0);
}

int kmemcmp(void* x,void* y,int c)
{
	signed char *xx = (signed char *)x;
	signed char *yy = (signed char *)y;
	
	while(c>0)
	{
		if(*xx!=*yy)
			return *xx-*yy;
		c--;
		x++;
		y++;
	}
	return 0;
}
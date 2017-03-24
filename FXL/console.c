#include "console.h"
#include "util.h"
#include "kprintf.h"

//row ends at row 25
//col ends at col 80

int rctr,colctr,exrctr;
int ccc;// = color
int hhh;
int cursorduderow;
int cursordudecol;

void halt()
{
	while(1)
		asm("hlt");
}

void bspetter(int fclr,int cl)
{
	console_init(fclr,cl);
}

void delClear(int color)
{
	int siz = 2800;
	int j=0;
	chh = (char*)0xb8000;
	
	while(j<siz)
	{
		*chh = ' ';
		*(chh+1) = color;
		chh+=2;
		j++;
	}
	chh+=bspacectr;
}

void clearLine(int row,int col)
{
	int j=0;
	int siz = 80;//cols per row
	chh = (char*)0xb8000;
	
	int p = row*80+col;
	chh+=p;
	
	while(j<siz)//clear one row
	{
		*chh = ' ';
		*(chh+1) = 0x1f;
		chh+=2;
		j++;
	}
}

void kmemcopy(void * dest,void * src,int n)
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
		
	clearLine(23,0);
}

void console_clear(int color)
{
	/**/
	int siz = 2800;
	int j=0;
	chh = (char*)0xb8000;
	
	while(j<siz)
	{
		*chh = ' ';
		*(chh+1) = color;
		chh+=2;
		j++;
	}
	chh = (char*)0xb8000;
	/**/
}

void console_init(int fclr,int color)
{
	console_clear(color);
	chh = (char*)0xb8000;
	colctr=0;
	rctr=0;
	exrctr=0;
	if(fclr==1)
		bspacectr=2;
	if(hhh==0xf)
		ccc = 0x1f;
	else
		ccc = color;
}

void console_putc(char ch)
{
	//Width = 0-160 bytes?
	
	if(ch=='\n')
	{
		*chh = ' ';
		int movby = 2;
		while(colctr<80)
		{
			chh+=(movby);
			colctr++;
		}
		//chh-=0;
		colctr=0;
		rctr++;
		exrctr++;
	}
	/**/
	else if(ch==127)//backspace
	{
		if(colctr>=0&&colctr<80)
		{
			chh=chh-bspacectr;
			colctr--;
			*chh=' ';
			*(chh+1) = ccc;
			bspacectr=bspacectr+2;
		}
	}
	/**/
	else if(ch == '\t')
	{
		*chh = ' ';
		//*chh = 't';
		int movby = 2;
		while(colctr<=8)
		{
			chh+=(movby);
			colctr++;
		}
	}
	else
	{
		*chh = ch;
		*(chh+1) = ccc;
		chh+=2;
		colctr++;
		bspacectr=bspacectr-2;
	}
	
	/*
	*(chh+1) = ccc;
	chh+=2;
	colctr++;
	bspacectr=bspacectr-2;
	*/
	
	if(colctr>79)
	{
		colctr=0;
		rctr++;
		exrctr++;
	}
	
	//Cursor
	/**/
	if(crow>4)
		crow=4;
	int p = crow*80+colctr;
	unsigned low = p & 0xff;
	unsigned high = (p>>8) & 0xff;
	
	outb(15,0x3d4);
	outb(low,0x3d5);
	outb(14,0x3d4);
	outb(high,0x3d5);
	/**/
}

void displr(int nn,char* q,int clr)
{
	console_clear(clr);
	chh = (char*)0xb8000;
	colctr=0;
	rctr=0;
	exrctr=0;
	//bspacectr=2;
	hhh=ccc;
	ccc = clr;
	
	int l;
	kprintf(q);
	for(l=0;l<2048;++l)
	{
		console_putc(nn);
	}
}

void sdoc(int nn)
{
	char* llpp = "You found the secret document";
	displr(nn,llpp,0xf);
}

void sdocone(int nn)
{
	char* llpp = "Page One";
	displr(nn,llpp,0x1f);
}

void sdoctwo(int nn)
{
	char* llpp = "Page Two";
	displr(nn,llpp,0x2f);
}

void sdocthree(int nn)
{
	char* llpp = "Page Three";
	displr(nn,llpp,0x3f);
}

void sdocfour(int nn)
{
	char* llpp = "Page Four";
	displr(nn,llpp,0x4f);
}

void sdocfive(int nn)
{
	char* llpp = "Page Five";
	displr(nn,llpp,0x5f);
}

void sdocsix(int nn)
{
	char* llpp = "Page Six";
	displr(nn,llpp,0x6f);
}

void sdocseven(int nn)
{
	char* llpp = "Page Seven";
	displr(nn,llpp,0x7f);
}

void sdoceight(int nn)
{
	char* llpp = "Page Eight";
	displr(nn,llpp,0x8f);
}

void sdocnine(int nn)
{
	char* llpp = "Page Nine";
	displr(nn,llpp,0x9f);
}
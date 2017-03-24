#include "console.h"
#include "keyboard.h"
#include "kprintf.h"
#include "util.h"
#include "disk.h"

char scancodes[]={' ',' ','1','2','3','4','5','6','7','8',
					'9','0','-','=',14,'\t','q','w','e','r',
					't','y','u','i','o','p','[',']',28,29,
					'a','s','d','f','g','h','j','k','l',';',
					'\'','`',42,'\\','z','x','c','v','b','n',
					'm',',','.','/',54,55,56,' ',58,59,
					60,61,62,63,64,65,66,67,68,69,
					70,71,72,73,74,75,76,77,78,79,
					80,81,82,83,84,' ',' ',87,88,' '};
					
char shcodes[]={' ',' ','!','@','#','$','%','^','&','*',
				'(',')','_','+',' ',' ','Q','W','E','R',
				'T','Y','U','I','O','P','{','}',28,29,
				'A','S','D','F','G','H','J','K','L',':',
				'"','~',42,'|','Z','X','C','V','B','N',
				'M','<','>','?',54,55,56,' ',58,59,
				60,61,62,63,64,65,66,67,68,69,
				70,71,72,73,74,75,76,77,78,79,
				80,81,82,83,84,' ',' ',87,88,' '};
					
char shiftedscancodes[]={' ',' ','!','@','#','$','%','^','&','*',
							'(',')','_','+',' ',' ','Q','W','E','R',
							'T','Y','U','I','O','P','{','}',1,29,
							'A','S','D','F','G','H','J','K','L',':',
							'"','~',42,'|','Z','X','C','V','B','N',
							'M','<','>','?',54,55,56,' ',58,59,
							60,61,62,63,64,65,66,67,68,69,
							70,71,72,73,74,75,76,77,78,79,
							80,81,82,83,84,' ',' ',87,88,' '};

							
/*
Important scancodes:
Esc:1
Return:28
Backspace:14
LShift:42
RShift:54
SpaceBar:57
1:2
2:3
3:4
4:5
5:6
Apostrophe:40
*/

/*files*/
File files[7];
/*Offsets*/
int oneoffset=0;
/*Buffers*/

/*Byte counters*/
int onecounter=0;
int twocounter=0;
int threecounter=0;
int fourcounter=0;
int fivecounter=0;
int sixcounter=0;
int sevencounter=0;

int keyboard_getline(char* q)
{
	linesize=0;
	buffer_ready=0;
	
	while(buffer_ready==0)
		asm("hlt");
	kmemcopy(q,linebuff,linesize);
	q[linesize]=0;
	linesize=0;
	buffer_ready=0;
	return 0;
}

/*
void keyboard_inturrupt()
{
}
*/

static volatile int linebuf_ready=0;
void keyboard_inturrupt()
{
	//Translate scancode
	char q=0;
	q = inb(0x60);
	//if(q==2 && q>0)//1
	
	bool press = !(q&0x80);
	q = q&0x7f;
	if(press)
	{
		//input keycode stuff(kcode numbers)
		
		if(q==14)//backspace
		{
			kprintf("BACKSPACE");
			if( linesize > 0 )
			{
				linesize -= 1;
				kprintf("%c",127);//delete
			}
		}
		if(q==3)//2
			kprintf("Article Two");
		if(q==4)//3
			kprintf("Article Three");
		if(q==5)//4
			kprintf("Article Four");
		if(q==6)//5
			kprintf("Article Five");
		if(q==7)//6
			kprintf("Article Six");
		if(q==8)//7
			kprintf("Article Seven");
		if(q==9)
			kprintf("ConstTXT");
	}
	//Translated scancode
	if(linebuf_ready==1)
		return;
	//else if(q=='\n')
	//	linebuf_ready=1;
	//else if(linebuff[4095]!=NULL)//buffer is full
		//kprintf("BUFFER IS FULL");
	//else if(key is printable && linesize < MAX_SIZE)
	//{
	//	linebuff[linesize++]=key;
	//	print ASCII value
	//}
}
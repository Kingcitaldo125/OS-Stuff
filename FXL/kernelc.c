//Paul Arelt FX Lab
// /cygdrive/c/users/paul/documents/FXL/
/*
SOURCES:
http://www.tek-tips.com/viewthread.cfm?qid=76828
http://www.cse.buffalo.edu/~bina/amrita/RTOS/xinudocs/kprintf_8c-source.html
http://stackoverflow.com/questions/6090561/how-to-use-high-and-low-bytes
http://stackoverflow.com/questions/22744624/keyboard-interrupt-handler-for-own-kernel-c
*/

#include "kprintf.h"
#include "console.h"
#include "keyboard.h"
#include "util.h"
#include "disk.h"
#include "stdio.h"
#include "string.h"

#define INT_DISABLE 0
#define INT_ENABLE  0x200
#define PIC1 0x20
#define PIC2 0xA0

#define ICW1 0x11
#define ICW4 0x01
//#include disk.h

int black = 0xf;
int blue = 0x1f;
int limegreen = 0x2f;
int cyan = 0x3f;
int crimson = 0x4f;
int purple = 0x5f;
int tan = 0x6f;
int grey = 0x7f;

void pics(int pic1, int pic2)
{
   /* send ICW1 */
   outb(PIC1, ICW1);
   outb(PIC2, ICW1);

   /* send ICW2 */
   outb(PIC1 + 1, pic1);   
   outb(PIC2 + 1, pic2);   

   /* send ICW3 */
   outb(PIC1 + 1, 4);   
   outb(PIC2 + 1, 2);

   /* send ICW4 */
   outb(PIC1 + 1, ICW4);
   outb(PIC2 + 1, ICW4);

   /* disable all IRQs */
   outb(PIC1 + 1, 0xFF);
}

void highlevel_handler
(unsigned edi,unsigned esi,unsigned ebp,unsigned esp,unsigned ebx,unsigned edx,unsigned ecx,unsigned eax,
int intnum,int errorcode,unsigned eip,int cs,char eflags)
{
	kprintf("Highlevel triggered\n");
	
	if(intnum==0)
	{
		//Division by zero
		kprintf("%x ",eip);
		kprintf("Division by zero error. \n");
		asm("hlt");
	}
	if(intnum==1)
	{
		//debug
		kprintf("Bad Debug Mode? \n");
		asm("hlt");
	}
	if(intnum==2)
	{
		//nmi
		kprintf("Nmi error \n");
		asm("hlt");
	}
	if(intnum==3)
	{
		//int 3
		kprintf("Int 3 error \n");
		asm("hlt");
	}
	if(intnum==4)
	{
		//overflow
		kprintf("Overflow error \n");
		asm("hlt");
	}
	if(intnum==5)
	{
		//bound
		kprintf("Bounds error \n");
		asm("hlt");
	}
	if(intnum==6)
	{
		//illegal operation code
		kprintf("Illegal OpCode\n");
		asm("hlt");
	}
	if(intnum==7)
	{
		//no fpu unit
		kprintf("Missing FPU chip \n");
		asm("hlt");
	}
	if(intnum==8)
	{
		//fault handler
		kprintf("Fault handle error: begin \n");
		asm("hlt");
	}
	if(intnum==9)
	{
		//fpu overrun
		kprintf("FPU Overflow error \n");
		asm("hlt");
	}
	if(intnum==10)
	{
		//bad tss
		kprintf("Bad TSS \n");
		asm("hlt");
	}
	if(intnum==11)
	{
		//seg absent
		kprintf("Absent Segmentation \n");
		asm("hlt");
	}
	if(intnum==12)
	{
		//stack fault
		kprintf("Stack Fault \n");
		asm("hlt");
	}
	if(intnum==13)
	{
		//illegal address
		kprintf("Unidentifiable address error \n");
		asm("hlt");
	}
	if(intnum==14)
	{
		//page fault
		kprintf("Page Fault error. \n");
		asm("hlt");
	}
	if(intnum==15)
	{
		//reserved
		kprintf("Reserved \n");
		asm("hlt");
	}
	if(intnum==16)
	{
		//fpu error
		kprintf("FPU Error \n");
		asm("hlt");
	}
	if(intnum==17)
	{
		//unaligned data
		kprintf("Unaligned data error \n");
		asm("hlt");
	}
	if(intnum==18)
	{
		//machine check
		kprintf("Machine Check error \n");
		asm("hlt");
	}
	if(intnum==19)
	{
		//sse error
		kprintf("SSE Error \n");
		asm("hlt");
	}
	if(intnum==20)
	{
		//virtualization error
		kprintf("Visualization Error \n");
		asm("hlt");
	}
	if(intnum>20 && intnum <=31)
	{
		//reserved...
		kprintf("Reserved Error Section Triggered. \n");
		asm("hlt");
	}
	if(intnum==33)
	{
		kprintf("KeyPressed");
	}
}

void refreshPage(int fclr)
{
	bspetter(fclr,blue);
	kprintf(" Paul Arelt FX Lab");
	console_putc('\n');
	kprintf(" Hello!");
	console_putc(1);
	kprintf("Type some text..\n");
	console_putc('\n');
	crow=3;
}

void deleteKey()
{
	if(global_counter>=0)
	{
		linebuff[global_counter]=' ';
		linesize=linesize-1;
		global_counter--;
	}
	
	kprintf("%c",127);
	refreshPage(0);
	
	int o;
	for(o=0;o<linesize;++o)
	{
		console_putc(linebuff[o]);
	}
	/**/
}

bool capslock = false;
bool shift = false;
bool controller = false;
bool clock = false;

void handleK(char c)
{
	//kprintf(" handelkey ");
	
	if(global_counter>=LINEBUF_SIZE-1)
	{
		refreshPage(1);
		kprintf("You Entered--->");
		int i;
		for(i=0;i<global_counter;++i)
		{
			console_putc(linebuff[i]);
			linebuff[i]=0;
		}
		kprintf("<---");
		console_putc('\n');
		crow++;
	}
	if(c==1||c==63)//escape and refresh
		refreshPage(1);
	if(c==88)
		sdoc(3);
	/**/
	else if(c==14)//backspace
	{
		//console_putc(127);
		deleteKey();
	}
	/**/
	else if (c==15)//tab
	{
		console_putc('\t');
		int x;
		for(x=0;x<9;++x)
			linebuff[global_counter]=' ';
		linesize=linesize+8;
		global_counter+=8;
	}
	else if (c==28)//enter key
	{
		refreshPage(1);
		kprintf("You Entered--->");
		int i;
		for(i=0;i<global_counter;++i)
		{
			console_putc(linebuff[i]);
			linebuff[i]=0;
		}
		kprintf("<---");
		console_putc('\n');
		crow++;
	}
	else if(c==58)//CapsLock
	{
		
	}
	else if(c==29)
	{
		
	}
	else if(c==42||c==54)
	{
		
	}
	else if(c==72)
	{
		//kprintf("up");
		console_putc(24);
	}
	else if(c==77)
	{
		//kprintf("right");
		console_putc(26);
	}
	else if(c==75)
	{
		//kprintf("left");
		console_putc(27);
	}
	else if(c==80)
	{
		//kprintf("down");
		console_putc(25);
	}
	else if(c>=69&&c<=80)
	{
		
	}
	else
	{
		if(controller==true)
		{
			kprintf("contrue");
			
			if(c==2)
				sdocone(1);
			if(c==3)
				sdoctwo(2);
			if(c==4)
				sdocthree(3);
			if(c==5)
				sdocfour(4);
			if(c==6)
				sdocfive(5);
			if(c==7)
				sdocsix(6);
			if(c==8)
				sdocseven(7);
			if(c==9)
				sdoceight(8);
			if(c==10)
				sdocnine(206);
		}
		else
		{
			char translator;
			if(shift==true||clock==true)
				translator = shcodes[(int)c];
			else
				translator = scancodes[(int)c];
			linebuff[global_counter]=translator;
			linesize=linesize+1;
			console_putc(translator);
			global_counter++;
		}
	}
}

void kmain(void)
{
	console_init(1,blue);
	refreshPage(1);
	//linebuff[LINEBUF_SIZE]='\0';
	global_counter=0;
	linesize=0;
	crow=3;
	
	unsigned char c;//=1;
	pics(0x20, 0x28);
	do
	{
		if(inb(0x60)!=c)
		{
			//c = inb(0xe0);
			c = inb(0x60);
			if(c>0)
			{
				bool press = !(c&0x80);
				bool release = c&0x80;
				c = c&0x7f;
				
				/*
				if(c==29&&press)
					controller=true;
				if(c==29&&release)
					controller=false;
				
				if((c==42||c==54)&&press)
					shift=true;
				if((c==42||c==54)&&release)
					shift=false;
				handleK(c);
				*/
				
				/**/
				if(release)
				{
					//console_putc('r');
					if(c==42||c==54)
						shift=false;
					else if(c==29)
						controller=false;
				}
				else if(press)
				{
					
					/*
					if(c==26)
						handleK(c);
					else if(c==27)
						handleK(c);
					else if(c==14)
					{
						kprintf("%c",127);
						deleteKey();
					}
					*/
					
					if(c==58)
					{
						if(clock)
						{
							clock=false;
							kprintf(" CAPSLOCK OFF ");
						}
						else
						{
							clock=true;
							kprintf(" CAPSLOCK ON ");
						}
					}
					else if(c==42||c==54)
					{
						shift=true;
						//controller=false;
					}
					else if(c==29)
					{
						kprintf("ctrl");
						controller=true;
						//shift=false;
					}
					else
						handleK(c);
				}
			}
		}
	}
	while(c!=0);
	kprintf("Halting...");
    halt();
}

int main(){return 0;}
int _main(){return 0;}
int __main(){return 0;}
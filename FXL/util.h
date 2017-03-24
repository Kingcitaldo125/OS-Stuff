extern void outb(unsigned char value,unsigned short port);
extern unsigned char inb(unsigned short port);
extern unsigned short inw(unsigned short port);

int kmemcmp(void* x,void* y,int c);
void kmemcpy(void * dest,void * src,int n);

//Colors!
//int white = 0x1f;
//int limegreen = 0x2f;
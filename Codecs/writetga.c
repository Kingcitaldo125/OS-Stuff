
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#pragma pack(push,1)
typedef struct Header_{
    uint8_t idsize;
    uint8_t colormaptype;
    uint8_t imagetype;
    uint8_t colormap[5];
    uint16_t originx;
    uint16_t originy;
    uint16_t width;
    uint16_t height;
    uint8_t bpp;
    uint8_t desc;
} Header ;
#pragma pack(pop)

const char* format(){
    return "tga";
}

int save(const char* s, char* idata, int w, int h)
{
	
	FILE* fp = fopen(s,"wb");
    if(!fp)
        return 0;
        
	Header hdr;
	
	hdr.idsize = 0;
	hdr.colormaptype = 0;
	hdr.imagetype = 2;		//uncompressed RGB
	memset(hdr.colormap,0,sizeof(hdr.colormap));
	hdr.originx = 0;
	hdr.originy = 0;
	hdr.width = w;
	hdr.height = h;
	hdr.bpp = 32;
	hdr.desc= 8;
	
	
	fwrite(&hdr,1,sizeof(Header),fp);
	
    char* one_row = (char*) malloc(w*4);
    int r;
    for(r=0;r<h;++r){
        char* S = idata + (h-r-1)*w*4;
        int c;
        for(c=0;c<w;++c,S+=4){
            one_row[c*4  ]=S[2];
            one_row[c*4+1]=S[1];
            one_row[c*4+2]=S[0];
            one_row[c*4+3]=S[3];
        }
        fwrite(one_row,w,4,fp);
    }
    
	fclose(fp);
    free(one_row);
	return 1;
	
}

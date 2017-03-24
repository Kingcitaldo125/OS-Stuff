
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

int  can_decode(const char* infile){
    
	FILE* fp = fopen(infile,"rb");
    if(!fp)
        return 0;
        
	Header hdr;
	fread(&hdr, 1, sizeof(Header), fp);
	fclose(fp);
    
	if( hdr.imagetype != 2 && hdr.imagetype != 10)
        return 0;
        
    if( hdr.bpp != 24 &&  hdr.bpp != 32  )
        return 0;
        
    return 1;
}

//format from Astle & Hawkins, Beginning OpenGL Game Programming
//and http://www.fileformat.info/format/tga/egff.htm
int load(const char* infile, char** idata, int *pw, int* ph)
{
    *idata = NULL;
    
	FILE* fp = fopen(infile,"rb");
    if(!fp)
        return 0;
        
	Header hdr;
	fread(&hdr, 1, sizeof(Header), fp);
	
	//skip id info
	fseek(fp,hdr.idsize,SEEK_CUR);
	
	if( hdr.imagetype != 2 && hdr.imagetype != 10){
		fprintf(stderr, "File %s: Not a truecolor Targa (appears to be indexed or grayscale):\n", infile);
		fprintf(stderr, "File's type is %d; should be %d!\n",
			hdr.imagetype,2);
        fclose(fp);
		return 0;
	}
	
	int compressed = (hdr.imagetype == 10);
	
	int bytes_per_pixel;
	if( hdr.bpp == 24 )
		bytes_per_pixel = 3;
	else if( hdr.bpp == 32 )
		bytes_per_pixel = 4;
	else{
		fprintf(stderr,"File %s: must be 24 or 32 bpp; file has %d bpp\n", infile, hdr.bpp);
        fclose(fp);
		return 0;
	}
	
	int w = hdr.width;
	int h = hdr.height;
	
    *pw=w;
    *ph=h;
    
	//always 4 bytes per pixel in our internal storage.
	char* bdata = (char*) malloc(w*h*4);
	*idata = bdata;
    
	if( !compressed ){
		uint8_t* one_row = (uint8_t*) malloc(w*4);
        int r;
		for( r=0;r<h;++r){
			fread(one_row,bytes_per_pixel,w,fp);
            char* D = bdata + (h-r-1)*4*w;
            uint8_t* S = one_row;
            int c;
			for(c=0;c<w;++c){
                D[2] = S[0];
                D[1] = S[1];
                D[0] = S[2];
                if( bytes_per_pixel == 3 )
                    D[3] = 255;
                else
                    D[3] = S[3];
                D+=4;
                S+=bytes_per_pixel;
			}
		}
		free(one_row);
	}
	else{
		//need to read & decode
        char* D = bdata;
        char* end = D + w*4*h;
        while( D < end ){
            uint8_t count;
			fread(&count,1,1,fp);
			if( count & 0x80 ){
				//compressed: several copies of next pixel
                char dat[4];
				count &= 0x7f;
				count++;
                
                //read next pixel
                dat[3]=255;
				fread( dat, 1, bytes_per_pixel, fp);
                
				while(count > 0 ){
                    D[0] = dat[2];
                    D[1] = dat[1];
                    D[2] = dat[0];
                    D[3] = dat[3];
                    D += 4;
                    count--;
				}
			}
			else{
				//uncompressed run
				count++;
                char dat[4];
                dat[3] = 255;
				while(count > 0 ){
					fread( dat, 1, bytes_per_pixel, fp);
                    D[0] = dat[2];
                    D[1] = dat[1];
                    D[2] = dat[0];
                    D[3] = dat[3];
                    D += 4;
                    count--;
				}
			}
		}
	}
	//done reading. Clean up.
	fclose(fp);
	return 1;
}

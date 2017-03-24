#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

//header format from web:
//256-color VGA programming in C
#pragma pack(push,1)
typedef struct Header_{
    uint16_t sig;		//always string BM
    uint32_t size;		//the whole thing
    uint32_t reserved;		//0
    uint32_t offset;		//how far from here to data?
    uint32_t header_size;	//guess :-)
    uint32_t width;		//bitmap size
    uint32_t height;		//ditto
    uint16_t planes;		//always 1
    uint16_t bpp;		//24 = true color
    uint32_t compression;	//0 = none
    uint32_t img_size;		//bytes in the image
    uint32_t ppm_x;		//pixels per meter, x
    uint32_t ppm_y;		//same for y dimension
    uint32_t ncolors;		//how many colors?
    uint32_t icolors;		//important ones
} Header; 
#pragma pack(pop)

int can_decode(const char* infile){
	FILE* fp = fopen(infile,"rb");
    if(!fp)
        return 0;
        
	Header hdr;
	fread(&hdr, 1, sizeof(Header), fp);
    fclose(fp);
    
    if( hdr.sig != 0x4d42 )
        return 0;
        
	if( hdr.bpp != 24 ){
		return 0;
	}
	
	if( hdr.compression != 0 ){
		return 0;
	}

    return 1;
}

int load (const char* infile, char** idata, int* pw, int *ph){
    *idata = NULL;
	FILE* fp = fopen(infile,"rb");
    if(!fp)
        return 0;
        
	Header hdr;
	fread(&hdr, 1, sizeof(Header), fp);
	
	
	if( hdr.bpp != 24 ){
		fprintf(stderr,"File %s: Not a truecolor (24bpp) BMP\n",infile);
		return 0;
	}
	
	if( hdr.compression != 0 ){
		fprintf(stderr,"File %s: Cannot read compressed BMP\n",infile);
		return 0;
	}

	//amount of padding on each row of data
	int padding;
	if( (hdr.width*3) % 4 == 0 )
		padding = 0;
	else
		padding = 4 - ((hdr.width*3)%4);

    fseek(fp, hdr.offset, SEEK_SET);
	
	int w = hdr.width;
	int h = hdr.height;
	
    *pw=w;
    *ph=h;
    
	//always 4 bytes per pixel in our internal storage.
	char* bdata = (char*) malloc(w*h*4);
	*idata = bdata;
    
	uint8_t* one_row = (uint8_t*) malloc(w*3);

    
    int r;
	for( r=0;r<h;++r){
		fread(one_row,3,w,fp);
		fseek(fp,padding,SEEK_CUR);
        uint8_t* S = one_row;
        char* D = bdata + (h-r-1)*w*4;
        int j;
        for(j=0;j<w;++j){
            D[0] = S[2];
            D[1] = S[1];
            D[2] = S[0];
            D[3] = 255;
            D+=4;
            S+=3;
        }
	}
	
    free(one_row);
	
	//done reading. Clean up.
	fclose(fp);
	return 1;
}

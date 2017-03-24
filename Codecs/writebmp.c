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

const char* format(){
    return "bmp";
}

//Write bitmap file
//Return 0 for success, nonzero for failure
int save(const char* outfile, char* idata, int w, int h){
	
	FILE* fp;
	Header hdr;
	
	int padnum;

	//binary mode is important on windows!	
	fp = fopen(outfile,"wb");
	
	if(!fp){
		printf("Cannot open bmp!\n");
		return 0;
	}
	
	hdr.sig = 0x4D42;	//string: BM
	hdr.size = sizeof(hdr);
	if( w % 4 == 0 )
		hdr.size += 3*w*h;
	else
		hdr.size += (3*w+ 4-(3*w)%4)*h;
	hdr.reserved = 0;
	hdr.offset = sizeof(hdr);
	hdr.header_size = 40;
	hdr.width = w;
	hdr.height = h;
	hdr.planes = 1;
	hdr.bpp = 24;
	hdr.compression = 0;
	hdr.img_size = 3*w*h;
	hdr.ppm_x = 2834;	//pixels per meter = 72 ppi
	hdr.ppm_y = 2834;
	hdr.ncolors = 0;	
	hdr.icolors = 0;	


	//we assume we are running on a little endian system
	//(ie, intel x86). If not, adjust accordingly.
	fwrite(&hdr,1,sizeof(Header),fp);
	
    uint8_t* one_row = (uint8_t*) malloc(w*3);
    int r,c;
	for(r=0;r<h;++r){
        char* cp = idata + (h-r-1)*w*4;
        int i;
		for( c=0,i=0;c<w;c++,cp+=4,i+=3){
			one_row[i+2] = cp[0]; //blue
			one_row[i+1] = cp[1]; //green
			one_row[i  ] = cp[2]; //red
		}
		
		fwrite(one_row,1,3*w,fp);
		padnum = 4 - ((w*3)%4);
		while(padnum < 4 && padnum > 0 ){
			fputc(0,fp);
			--padnum;
		}
	}
			
    free(one_row);
    
	fclose(fp);
	return 1;
}


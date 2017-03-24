#!/usr/bin/env python3

#//ssu jh etec3701 au 2007
#//revised au 2012
#revised au 2015

from ctypes import *
import sys
import random
import time
import os
import re



def debug(*x):
    return
    lst=[str(q) for q in x]
    print(" ".join(lst))
   
   
lst = [250,252,49,192,142,216,142,192,190,0,124,191,0,122,185,0,2,243,164,184,
24,122,255,224,102,139,14,198,123,187,0,124,186,247,1,236,168,128,117,251,
186,246,3,176,2,238,186,242,1,176,1,238,186,243,1,136,200,238,66,136,
232,238,66,102,193,233,16,136,200,238,66,136,232,12,224,238,186,247,1,176,
32,238,186,247,1,236,168,128,117,251,236,168,8,116,251,185,0,1,186,240,
1,237,137,7,67,67,73,133,201,117,246,184,1,232,205,21,102,49,246,137,
222,102,193,230,16,102,129,198,0,0,0,1,102,137,54,4,0,190,252,122,
191,8,0,185,40,0,243,164,15,1,22,36,123,15,32,192,102,131,200,1,
15,34,192,235,0,184,8,0,142,216,142,192,142,224,142,232,142,208,102,185,
48,0,0,0,102,191,0,138,11,0,102,190,204,122,0,0,243,103,164,234,
0,124,16,0,78,7,111,7,119,7,32,7,108,7,111,7,97,7,100,7,
105,7,110,7,103,7,32,7,116,7,104,7,101,7,32,7,86,7,66,7,
82,7,46,7,46,7,46,7,32,7,32,7,0,0,0,0,0,0,0,0,
255,255,0,0,0,146,207,0,255,255,0,0,0,154,207,0,255,255,0,0,
0,242,207,0,255,255,0,0,0,250,207,0,40,0,8,0,0,0,
]
mbrcode =  (c_uint8*446)( *lst )

lst = [235,60,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,
144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,
144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,
144,144,252,250,190,0,124,0,0,191,0,0,16,0,185,0,2,0,0,243,
164,184,88,0,16,0,255,224,188,0,16,16,0,189,158,143,11,0,15,183,
5,22,0,16,0,141,92,0,1,3,29,28,0,16,0,83,191,0,16,0,
0,232,82,0,0,0,139,53,28,16,0,0,137,247,193,238,9,129,231,255,
1,0,0,116,1,70,133,246,15,132,227,0,0,0,91,15,183,5,17,0,
16,0,193,232,4,1,195,191,0,16,0,0,133,246,116,23,129,255,0,0,
9,0,15,141,181,0,0,0,83,232,14,0,0,0,91,67,78,235,229,49,
228,184,0,16,0,0,255,224,106,0,232,104,0,0,0,131,196,4,102,186,
246,3,176,2,238,102,186,242,1,176,1,238,102,66,136,216,238,102,66,136,
248,238,102,66,193,235,16,136,216,238,102,66,136,248,12,224,238,102,66,176,
32,238,106,1,232,50,0,0,0,131,196,4,102,186,240,1,102,185,0,1,
102,237,102,137,7,71,71,102,73,102,133,201,117,242,198,69,0,46,198,69,
1,7,129,253,128,140,11,0,116,3,77,77,195,189,158,143,11,0,195,102,
186,241,1,236,132,192,117,21,102,186,247,1,236,168,128,117,238,131,124,36,
4,0,116,4,168,8,116,227,195,190,137,1,16,0,185,20,0,0,0,191,
0,128,11,0,243,164,244,235,253,190,157,1,16,0,185,28,0,0,0,235,
234,190,185,1,16,0,185,18,0,0,0,235,222,68,79,105,79,115,79,107,
79,32,79,69,79,114,79,114,79,111,79,114,79,75,79,101,79,114,79,110,
79,101,79,108,79,32,79,116,79,111,79,111,79,32,79,98,79,105,79,103,
79,78,79,111,79,32,79,107,79,101,79,114,79,110,79,101,79,108,79,
]
vbrcode = (c_uint8*510)( *lst )

class PTE(Structure):
    _pack_=1
    _fields_ = [
        ("bootable",c_int8),
        ("starthead",c_int8),
        ("startsectcyl",c_int16),
        ("type",c_uint8),
        ("endhead",c_uint8),
        ("endcylsect",c_uint16),
        ("start",c_uint32),
        ("size",c_uint32)
    ]
assert sizeof(PTE) == 16

class MBR(Structure):
    _pack_=1
    _fields_ = [
        ("mbr",c_uint8*446),
        ("ptable" , PTE*4),
        ("signature", c_uint8*2)
    ]

assert sizeof(MBR) == 512

class VBR(Structure):
    _pack_=1
    _fields_=[
        ("jmp" , c_uint8*3           ),
        ("oem" , c_char*8                   ),
        ("bytes_per_sector" , c_uint16          ),
        ("sectors_per_cluster" , c_uint8           ),
        ("vbr_sectors" , c_uint16          ),
        ("num_fats" , c_uint8           ),
        ("num_root_dir_entries" , c_uint16          ),
        ("num_sectors_small" , c_uint16          ),
        ("id" , c_uint8           ),
        ("sectors_per_fat" , c_uint16          ),
        ("sectors_per_track" , c_uint16          ),
        ("num_heads" , c_uint16          ),
        ("first_sector" , c_uint32            ),
        ("num_sectors_big" , c_uint32            ),
        ("drive_number" , c_uint8           ),
        ("reserved" , c_uint8           ),
        ("sig1" , c_uint8           ),
        ("serial_number" , c_uint32            ),
        ("label" , c_char*11                    ),
        ("fstype" , c_char*8                   ),
        ("code", c_uint8*448),
        ("signature",c_uint8*2)

    ]
assert sizeof(VBR) == 512

valid_filename_chars=set("ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890-~")
READONLY_BIT=1
HIDDEN_BIT=2
SYSTEM_BIT=4
LABEL_BIT=8
DIRECTORY_BIT = 16
ARCHIVE_BIT = 32 
class DirEntry(Structure):
    _pack_=1
    _fields_ = [
        ("base",c_uint8*8),
        ("ext",c_uint8*3),
        ("attrib",c_uint8),
        ("reserved",c_uint8),
        ("ctime_centiseconds",c_uint8),
        ("ctime",c_uint16),
        ("cdate",c_uint16),
        ("adate",c_uint16),
        ("clusterhigh",c_uint16),
        ("time",c_uint16),
        ("date",c_uint16),
        ("start",c_uint16),
        ("size",c_uint32)
    ]
    def __str__(self):
        b=[]
        if all( [q == 0 for q in self.base] ):
            return "<0>"
        else:
            for c in self.base:
                if c < 32 or c > 126:
                    b.append("<"+str(c)+">")
                else:
                    b.append(chr(c))
            
        e=[chr(c) for c in self.ext]
        
        return "["+"".join(b)+"."+"".join(e)+"@"+str(self.start)+"/"+str(self.size)+"]"
    def __repr__(self):
        return str(self)
        
assert sizeof(DirEntry) == 32
 
class Disk:
    def __init__(self,fname):
        fp=open(fname,"r+b")
        self.fp=fp
        self.mbr = MBR()
        b = fp.read(512)
        self.mbr = MBR.from_buffer_copy(b)
        fp.seek(self.mbr.ptable[0].start*512)
        b=fp.read(512)
        self.vbr = VBR.from_buffer_copy(b)

        self.fp.seek( (self.vbr.first_sector+self.vbr.vbr_sectors)*512 )
        tmp = self.fp.read(self.vbr.sectors_per_fat*512)
        ne = self.vbr.sectors_per_fat*512//2
        self.fat = (c_uint16*ne).from_buffer_copy(tmp)


    def allocate_clusters(self, filesize, randomize ):
        """Mark some clusters as allocated in the fat.
        filesize = number of bytes to allocate.
        randomize = true if we should select random clusters;
           false = select first free clusters
        Allocate clusters for a file. Mark the clusters
        as occupying a complete chain in the fat; return
        list of cluster numbers."""
        
        clustersize = self.vbr.sectors_per_cluster * 512
        
        numclusters = filesize // clustersize
        if filesize % clustersize != 0:
            numclusters += 1        #round up

        free = filter(lambda x: self.fat[x]==0 , range(2,len(self.fat)))
        free = list(free)

        if len(free) < numclusters:
            raise RuntimeError("Not enough space on the disk")

        clist=[]
        for j in range(numclusters):
            if not randomize:
                ri = 0
            else:
                ri = random.randrange(len(free))
            clist.append(free[ri])
            del free[ri]

        clist.append(0xffff)
        
        for i in range(len(clist)-1):
            c = clist[i]
            nc = clist[i+1]
            self.fat[c] = nc
            
        self.flush_fat()
        return clist[:-1]
     
    def free_clusters(self,cluster_list):
        """mark clusters as unused in fat"""
        for c in cluster_list:
            self.fat[c]=0
        self.flush_fat()
        
    def flush_fat(self):
        self.fp.seek( (self.vbr.first_sector+self.vbr.vbr_sectors)*512 )
        self.fp.write( string_at(addressof(self.fat),len(self.fat)*2) )
        self.fp.flush()
        
    def write_root_directory_entry(self, idx, de ):
        assert idx < self.vbr.num_root_dir_entries
        
        #move to start of root dir + location of new direntry
        self.fp.seek( (self.vbr.first_sector+self.vbr.vbr_sectors + 
            self.vbr.sectors_per_fat*self.vbr.num_fats)*512 + 32*idx)
        self.fp.write( string_at(addressof(de),32) )
        self.fp.flush()
        
    def write_cluster( self, cluster, data ):
        #write data for one cluster. Don't update
        #FAT.
        assert len(data) <= self.vbr.sectors_per_cluster*512
        self.fp.seek( self.cluster_start(cluster) )
        debug("Writing",len(data),"bytes of data (",data[:20],"...) to cluster",cluster,"=offset",self.fp.tell())
        self.fp.write(data)
        self.fp.flush()
        
    def get_name_from_direntry(self,de):
        """Convert a direntry to a name in 8.3 format"""
        for c in de.base:
            if c == 32:
                break
            tmp += chr(c)
        flag=0
        for c in de.ext:
            if c == 32:
                break
            if not flag:
                tmp += "."
                flag=True
            tmp += chr(c)
        return tmp
      
    def alloc_root_direntry(self,de):
        """Allocate a direntry in the root and copy contents of de to it"""
        self.ensure_unique(self.read_dir(None),de.base,de.ext)

        #move to start of root dir
        self.fp.seek( (self.vbr.first_sector+self.vbr.vbr_sectors + 
            self.vbr.sectors_per_fat*self.vbr.num_fats)*512)
        for i in range(self.vbr.num_root_dir_entries):
            tmp = self.fp.read(32)
            if tmp[0] == 0 or tmp[0] == 0xe5:
                self.write_root_directory_entry(i,de)
                return i
        
        raise RuntimeError("No free directory entries")
        
    def get_dir_entry_index(self,owning_dir, de ):
        L = self.read_dir(owning_dir)
        
        assert type(de) == DirEntry
        
        base = [q for q in de.base]
        ext = [q for q in de.ext]
        for i in range(len(L)):
            tmp = L[i]
            b1 = [q for q in tmp.base]
            e1 = [q for q in tmp.ext]
            if b1 == base and e1 == ext:
                assert type(i) == int
                return i
        raise RuntimeError("Does not exist")
        
    def get_dir_entry(self,fname):
        """Get directory entry for a particular filename.
        Return DirEntry"""
        
        #debug("get_dir_entry",fname)

        #replace multiple consecutive slashes with one slash
        fname=re.sub(r"/+","/",fname)
        
        #remove leading slash; all paths are always absolute
        if fname.startswith("/"):
            fname=fname[1:]
            
        #trailing slashes don't mean anything
        if fname.endswith("/"):
            fname=fname[:-1]
            
        if len(fname) == 0:
            return None     #empty string = the root
        else:
            lst=fname.split("/")
            
        cwd = self.read_dir(None)
        dbug = lst[:]
        while 1:
            #debug("get_dir_entry: Considering",lst[0],"from original list",dbug)
            base,ext = self.splitFilename(lst.pop(0))
            for i in range(len(cwd)):
                e=cwd[i]
                if e.base[0] == 0 or e.base[0] == 0xe5:
                    continue
                nm=0
                for c in range(8):
                    if base[c] == e.base[c]:
                        nm+=1
                for c in range(3):
                    if ext[c] == e.ext[c]:
                        nm+=1
                if nm == 11:
                    #we have a match
                    if len(lst) == 0:   #done chaining through directories
                        #print("get_dir_entry: All done",dbug,e,i)
                        return e
                    else:
                        #debug("get_dir_entry: Reading directory",e)
                        cwd = self.read_dir(e)
                        break
            else:
                raise RuntimeError("No such file '"+fname+"' in get_dir_entry")

    def read_dir(self,de):
        """Return list of DirEntry items from the directory whose DirEntry
            is de."""
            
        assert de == None or type(de) == DirEntry
        
        if not de:
            #reading the root
            self.fp.seek( (self.vbr.first_sector+self.vbr.vbr_sectors + 
                self.vbr.sectors_per_fat*self.vbr.num_fats)*512 )
            b=self.fp.read(self.vbr.num_root_dir_entries * 32 )
            root = (DirEntry * self.vbr.num_root_dir_entries).from_buffer_copy(b)
            L=[]
            for i in range(self.vbr.num_root_dir_entries):
                L.append(root[i])
            return L
        
        if de.attrib & DIRECTORY_BIT:
            #it's a directory, so read its contents
            tmp=self.read_file(de)
            debug("read_dir: contents of dir=",tmp)
            cwd=[]
            for j in range(0,len(tmp),32):
                cwd.append(DirEntry.from_buffer_copy(tmp[j:j+32]))
            debug("read_dir: returning",len(cwd),"DirEntry structs")
            return cwd
        else:
            raise RuntimeError("read_dir:"+str(de)+": Not a directory")
        
    def splitFilename(self,fname):
        #convert filename ("foo.c") to base,ext pair:
        # "foo    ","c  "
        #return as two byte arrays
        if fname.find(".") == -1:
            base=fname.upper()
            ext=""
        else:
            base,ext = fname.upper().split(".",1)
            
        if len(base) > 8 or len(ext) > 3:
            raise RuntimeError("Bad filename:"+base+" "+ext)
            
        for c in base+ext:
            if c not in valid_filename_chars:
                raise RuntimeError("Bad character in filename: "+c)

        base1 = (c_uint8 * 8)()
        ext1 = (c_uint8 * 3)()
    
        for i in range(8):
            base1[i]=32  #space
        for i in range(3):
            ext1[i]=32 #space
            
        for i in range(len(base)):
            base1[i] = ord(base[i])
        for i in range(len(ext)):
            ext1[i] = ord(ext[i])

        return base1,ext1

    def clusters_for_file(self,e):
        #e=direntry
        assert type(e) == DirEntry
        cn = e.start
        if cn == 0:
            return []
            
        L=[]
        while cn != 0xffff:
            assert cn != 0 and cn < 0xfff7
            L.append(cn)
            cn=self.fat[cn]
        return L

    def ensure_unique(self,list_of_direntries, base,ext):
        """Ensure that the given base,ext pair does not appear in
        the list. If parent_direntry
        is None, look in the root. As a side effect, return
        the number of files in parent_direntry"""
        
        assert type(list_of_direntries) == list
        flist = list_of_direntries  #self.read_dir(parent_direntry)
        numf=0
        for e in flist:
            l1 = [q for q in e.base]
            l2 = [q for q in base]
            l3 = [q for q in e.ext]
            l4 = [q for q in ext]
            if l1 == l2 and l3 == l4:
                tmp="".join([chr(q) for q in base])
                tmp += "".join([chr(q) for q in ext])
                raise RuntimeError("File",tmp,"already exists")
                numf+=1
        return numf

    def read_file(self,de):
        """Read and return contents of the given file"""
        cl = self.clusters_for_file(de)
        debug("read_file:",de,": clusters=",cl)
        data=[]
        for c in cl:
            data.append( self.read_cluster(c) )
        tmp=[]
        for d in data:
            tmp += d
        debug("read_file: direntry",de,"says size=",de.size)
        return bytes(tmp[:de.size])
 
    def read_cluster(self,c):
        assert c >= 2 and c < 0xfff8
        cs = self.cluster_start(c)
        self.fp.seek( cs )
        debug("read_cluster: cluster",c,"= fp.seek(",cs,")")
        buf = self.fp.read(self.vbr.sectors_per_cluster*512)
        return buf
 
    def verify_direntry_valid(self,de):
        tmp=[q for q in de.base]
        
        if chr(de.base[0]) not in valid_filename_chars:
            raise RuntimeError("Bad character in filename",de)
            
        for q in [ [y for y in de.base],[y for y in de.ext] ]:
            for i in range(len(q)):
                c=q[i]
                if c == 32 :
                    if any( [x!=32 for x in q[i:]]):
                        raise RuntimeError("Bad directory entry: non-space after space")
                    break
                if chr(c) not in valid_filename_chars:
                    raise RuntimeError("Bad character in filename:"+chr(c)+"("+str(c)+")")
        
        if de.start == 1 or de.start == 2 or (de.start == 0 and de.size != 0 ) or de.start >= self.vbr.sectors_per_fat*256:
            raise RuntimeError("Bad starting cluster:"+str(de.start))
            
        
    def create_empty_file( self, grandparentdirentry, parentdirentry, direntry):
        """Let grandparentdirentry be the direntry of a folder. Call it G.
            Let parentdirentry be the direntry of a folder inside G. Call it P.
            Create a new entry in P, using the data in direntry. Note that the size in 'direntry' should be 
                zero, and so should its starting cluster.
            This might cause P to become larger (if it's not the root), so we would need to
                update P's direntry. P's direntry can be found in G, which is why we need G here.
            Either G or P can be None to indicate the root (the root has no grandparent, so if P is None,
                G is also None, as a special case).
        The return value is the index of the newly created direntry in P.
        """

        debug("create_empty_file: owning dir=",parentdirentry,"new entry=",direntry)
        
        self.verify_direntry_valid(direntry)
        
        if not parentdirentry:
            #in root. Just create the new entry in the root and stop.
            newfile_index = self.alloc_root_direntry(direntry)
            return newfile_index
        else:
            assert grandparentdirentry == None or type(grandparentdirentry) == DirEntry
            assert type(parentdirentry) == DirEntry
            assert type(direntry) == DirEntry
        
            if not (parentdirentry.attrib & DIRECTORY_BIT):
                raise RuntimeError("Bad path for create file: Not a directory: "+str(parentdirentry))
                
                
            #verify we don't already have this filename
            L = self.read_dir(parentdirentry)
            for x in L:
                if self.direntry_names_match(x,direntry):
                    raise RuntimeError("Duplicate filename:"+str(direntry))
                    
            #read the parent directory into RAM so we can add the new file's entry to it
            dat = self.read_file(parentdirentry)
            
            debug("The parent has these contents before:",dat)
            
            #append new data to old data
            
            tmp = string_at(addressof(direntry),32)
            
            #the index of the newly created file
            newfile_index = len(dat)//32
            dat = dat + bytes([q for q in tmp])

            debug("this is the data to write:",(dat))
            
            #rewrite the parent direntry's content (i.e., the list of files
            #which now includes the newly created file)
            

            #now we are ready to write the data for the parent directory.

            #this is the index of the parent directory (which is being rewritten)
            #in *its* parent (the grandparent of the newly created file)
            parentindex = self.get_dir_entry_index(grandparentdirentry, parentdirentry)

            debug("create_empty_file: rewriting file number",parentindex,"found in directory",grandparentdirentry,"with",len(dat),"bytes of data")
            self.rewrite_file(
                grandparentdirentry,
                parentindex,
                dat)


            
            #need to make sure the caller sees the updated DirEntry data
            tmp = self.read_dir(grandparentdirentry)[parentindex]
            assert self.direntry_names_match(tmp,parentdirentry)
            parentdirentry.size = tmp.size
            parentdirentry.start = tmp.start 
            
 
            
            
            debug("create_empty_file: done; returning",newfile_index)
            
            #return index of the newly created file's direntry
            return newfile_index
     
    def byte_offset(self, direntry, offs ):
        """Return the location in the disk file (if we did fp.seek())
            that holds the byte at offset offs within the file direntry."""
        clist = self.clusters_for_file(direntry)
        clusters_to_skip = offs // (self.vbr.sectors_per_cluster*512)
        cluster = clist[clusters_to_skip]
        offset_in_cluster = offs % (self.vbr.sectors_per_cluster*512)
        return self.cluster_start(cluster) + offset_in_cluster
        
    def cluster_start(self,cluster):
        """returns location in hard drive file where cluster starts"""
        
        return 512*(self.vbr.first_sector + 1 + 2 * self.vbr.sectors_per_fat) + \
            self.vbr.num_root_dir_entries*32 + \
            (cluster-2)*self.vbr.sectors_per_cluster*512
        
    def direntry_names_match(self,d1,d2):
        b1 = [q for q in d1.base]
        e1 = [q for q in d1.ext]
        b2 = [q for q in d2.base]
        e2 = [q for q in d2.ext]
        return b1==b2 and e1==e2
        
        
    def rewrite_file(self,parent_direntry, index, data):
        """This rewrites the data for the given file.
            parent_direntry = DirEntry for the directory which holds the file
            index = index of the file in parent_direntry to be rewritten
            data = the data to store to the file
        """
        debug("rewrite_file: begin: parent=",parent_direntry,"index=",index,"data=",len(data),"bytes=",data[:10]+b"...")

        assert type(index)==int
        assert index >= 0
        
        #is this the first file? We treat it specially
        if parent_direntry == None and index == 0:
            randomize_clusters = False
        else:
            randomize_clusters = True
            
        
        
        #get contents of the directory that holds the file which is to be rewritten.
        #scan through and locate the entry for the file we are rewriting.
        parent_dircontents = self.read_dir(parent_direntry)
        
        
        direntry = parent_dircontents[index]
        
        #determine what clusters our file currenty occupies
        L = self.clusters_for_file(direntry)

        cluster_size = self.vbr.sectors_per_cluster*512

        #either add more or drop unneeded ones
        
        needed_clusters = len(data) // cluster_size
        if len(data) % cluster_size != 0:
            needed_clusters += 1
          
        debug("rewrite_file: needed clusters=",needed_clusters,"file currently has",L)
        
        if needed_clusters > len(L):
            tmp = needed_clusters * cluster_size
            L += self.allocate_clusters(tmp, randomize_clusters)
            discard=[]
        elif needed_clusters < len(L):
            num_excess = len(L) - needed_clusters
            discard = L[len(L)-num_excess:]
            L = L[0:len(L)-num_excess]
            self.free_clusters(discard)
        else:
            #exactly equal
            discard=[]
            
        cluster_list = L

        debug("rewrite_file: final cluster_list=",cluster_list,"discard=",discard)
        assert len(cluster_list) == needed_clusters 
        
        if len(cluster_list) == 0:
            assert len(data) == 0
            direntry.start = 0
        else:
            direntry.start = cluster_list[0]

        direntry.size = len(data)
        
        #we need to update the parent's metadata for the newly rewritten file
        
        if parent_direntry:
            #a direntry never crosses a sector boundary,
            #so we don't have to worry about that.
            #The only two fields that can change are the starting cluster
            #and the size (we don't update the date). 
            #Since no new entries are being added to any directories,
            #we don't have to worry about the directory's metadata changing.
            offs = self.byte_offset(parent_direntry, index*32 )
            
            
            self.fp.seek(offs)
            dbug=self.fp.read(32)
            #debug("rewrite_file: this should be a direntry:",[chr(q) for q in dat1])
            dbug = DirEntry.from_buffer_copy(dbug)
            
            self.fp.seek(offs+26)
            #little endian; write the start and size
            tmp=direntry.start
            self.fp.write( bytes([tmp & 0xff, (tmp>>8)&0xff ]) )
            tmp=len(data)
            self.fp.write( bytes( [tmp & 0xff, (tmp>>8) & 0xff, (tmp>>16) & 0xff , (tmp>>24) & 0xff ]) )
        else:
            #it's in the root, so we write it in a special way.
            #We write the entire entry since it's easier than
            #just updating part of it.
            debug("rewrite_file: updating root dir entry",index,"with data",direntry,"and start",direntry.start,"and size",direntry.size)
            self.write_root_directory_entry(index,direntry)
        
        #now write the contents of the file
        i=0
        j=0
        debug("rewrite_file: Update clusters:",cluster_list,"data=",len(data),"bytes")
        while i < len(data):
            self.write_cluster(cluster_list[j],data[i:i+cluster_size])
            i += cluster_size
            j+=1

        debug("rewrite_file: Done")
        return
        
    def remove_file(self,fname):
        """Remove a file. fname = the full path to the file."""
        
        parent,filename = self.splitPath(fname)
        grandparent,junk = self.splitPath(parent)
        
        e = self.get_dir_entry(fname)
        parent_direntry = self.get_dir_entry(parent)
        
        index = self.get_dir_entry_index(parent_direntry,e)
        
        self.free_clusters(self.clusters_for_file(e))
        
        if not parent_direntry:
            #file was in the root
            e.base[0]=0xe5
            self.write_root_directory_entry(index,e)
        else:
            assert parent_direntry & DIRECTORY_BIT

            if grandparent:
                grandparent_direntry = self.get_dir_entry(grandparent)
                assert grandparent_direntry & DIRECTORY_BIT
                
            #get index of deleted file in parent directory
            deleted_file_index = self.get_dir_entry_index(parent_direntry,e)
            parent_contents = self.read_file(parent_direntry)
            parent_contents.pop(deleted_file_index)
            self.rewrite_file(
                grandparent_direntry,
                self.get_dir_entry_index(grandparent_direntry,parent_direntry),
                parent_contents)
        
    def make_direntry(self,base,ext,attrib,randomize_time=False):
        """create a directory entry with the given data
            Start and size will be zero.
            This does not store the entry anywhere
            """
        de = DirEntry()
        
        de.base=base
        de.ext=ext
        de.attrib=attrib
        ctime=time.time()
        mtime=time.time()
        atime=time.time()
        
        if randomize_time:
            #any time in the last year...
            tmp=random.randrange(365*24*60*60)
            mtime -= tmp
            ctime = mtime - random.randrange(365*24*60*60)
            atime = mtime + random.randrange(0,tmp)
            
        mtime = time.localtime(mtime)
        ctime = time.localtime(ctime)
        atime = time.localtime(atime)

        #debugging
        #de.reserved=(c_uint8*10)(*[q for q in base])

        
        tm_sec = mtime.tm_sec
        tm_min = mtime.tm_min
        tm_hour = mtime.tm_hour
        tm_mday = mtime.tm_mday
        tm_mon = mtime.tm_mon
        tm_year = mtime.tm_year

        de.time = (tm_sec//2) | (tm_min<<5) | (tm_hour<<11)
        de.date = (tm_mday) | (tm_mon<<5) | ((tm_year-1980)<<9)

        tm_sec = ctime.tm_sec
        tm_min = ctime.tm_min
        tm_hour = ctime.tm_hour
        tm_mday = ctime.tm_mday
        tm_mon = ctime.tm_mon
        tm_year = ctime.tm_year
        
        de.ctime_centiseconds = (tm_sec%2)*100
        de.ctime = (tm_sec//2) | (tm_min<<5) | (tm_hour<<11)
        de.cdate = (tm_mday) | (tm_mon<<5) | ((tm_year-1980)<<9)
        
        tm_sec = atime.tm_sec
        tm_min = atime.tm_min
        tm_hour = atime.tm_hour
        tm_mday = atime.tm_mday
        tm_mon = atime.tm_mon
        tm_year = atime.tm_year
        
        de.adate = (tm_mday) | (tm_mon<<5) | ((tm_year-1980)<<9)
        
        de.clusterhigh = 0
        
        de.start = 0
        de.size = 0

        return de

    def splitPath(self,path):
        """Input: A pathname, possibly with slashes
            Returns: tuple: Everything up to the last path element , last path element
        """
        i=path.rfind("/")
        if i != -1:
            head = path[:i]
            tail = path[i+1:]
        else:
            head=""
            tail = path 
            
        return head,tail
            
def mcat(d,fname):
    de = d.get_dir_entry(fname)
    data = d.read_file(de)
    print(data)
    
def mkdir(d,dname):
    debug("----------------------\n----------------------\n---------------------\nmkdir:",dname)
    parentdirname, filename = d.splitPath(dname)
    grandparentdirname , junk = d.splitPath(parentdirname)
    base,ext = d.splitFilename(filename)
    if [q for q in ext] != [32,32,32]:
        raise RuntimeError("You are not allowed to have an extension on a directory name!")

    de= d.make_direntry(base=base,ext=ext,attrib=DIRECTORY_BIT)
    if parentdirname:
        parentdirentry = d.get_dir_entry(parentdirname)
    else:
        parentdirentry = None
    if grandparentdirname:
        grandparentdirentry = d.get_dir_entry(grandparentdirname)
    else:
        grandparentdirentry = None
        
    d.create_empty_file(grandparentdirentry,parentdirentry,de)

def mcp(d,infile,outfile,randomize):
    debug("------------------------------")
    debug("------------------------------")
    debug("------------------------------")
    debug("mcp: begin: copy",infile,"to",outfile)
    
    if outfile.endswith("/"):
        outfile += infile.split("/")[-1]
        
    try:
        de = d.get_dir_entry(outfile)
        if de.attrib & DIRECTORY_BIT:
            outfile += "/"+infile.split("/")[-1]
            print("Note: Copying",infile,"to",outfile)
    except RuntimeError:
        pass
    
    debug("mcp: really copying",infile,"to",outfile)
    
    parentdirname, filename = d.splitPath(outfile)
    if parentdirname:
        parentdirentry = d.get_dir_entry(parentdirname)
        if not (parentdirentry.attrib & DIRECTORY_BIT):
            raise RuntimeError("Path component is not a directory")
        grandparentdirname , junk = d.splitPath(parentdirname)
        if grandparentdirname:
            grandparentdirentry = d.get_dir_entry(grandparentdirname)
            if not (grandparentdirentry.attrib & DIRECTORY_BIT):
                raise RuntimeError("Path is not directory")
        else:
            grandparentdirentry = None
            grandparentdirname = None
            
        parentdirentry_index = d.get_dir_entry_index(grandparentdirentry,parentdirentry)

    else:
        debug("mcp: copying to root")
        parentdirentry = None
        grandparentdirentry = None
        grandparentdirname = None
    
    
    ifp=open(infile,"rb")
    fdata = ifp.read()
    sz = len(fdata)
    
    debug("mcp: parent=",parentdirname,"grandparent=",grandparentdirname)
    base,ext = d.splitFilename(filename)
    
    #create a direntry object
    de = d.make_direntry(base=base,ext=ext,attrib=0,randomize_time=randomize)
    debug("Made direntry object:",de)
    
    #create an empty file in the parent directory.
    debug("mcp: creating empty file: gp=",grandparentdirentry,"par=",parentdirentry,"de=",de)
    L1 = d.read_dir(parentdirentry)
    debug("~~~~~Before:")
    debug(L1)
    
    newfile_index = d.create_empty_file(grandparentdirentry, parentdirentry,de)
    
    debug("Debugging: ~~~after")
    L2 = d.read_dir(parentdirentry)
    debug("~~~~~After:")
    debug(L2)
    
    assert parentdirentry==None or len(L1)+1 == len(L2)
    #debugging
    debug("create_empty_file: new file is at index",newfile_index)
    L = d.read_dir(parentdirentry)
    
    if not len(L) > newfile_index:
        assert 0
        
    
    assert newfile_index != None
    d.rewrite_file(
        parentdirentry, 
        newfile_index,
        fdata)

def mfat(d,fname):
    if fname != '-':
        e = d.get_dir_entry(fname)
        cl = d.clusters_for_file(e)
        print(cl)
    print("Sectors per cluster:",d.vbr.sectors_per_cluster,
        "=",d.vbr.sectors_per_cluster*512,"bytes")
    print("Root dir entries:",d.vbr.num_root_dir_entries)
    print("Sectors per fat:",d.vbr.sectors_per_fat)
    print("First sector:",d.vbr.first_sector)
    print("PTE start: Sector",d.mbr.ptable[0].start)
    print("PTE size:",d.mbr.ptable[0].size,"sectors =",
        d.mbr.ptable[0].size*512,"bytes")
    lost = d.mbr.ptable[0].size-d.vbr.sectors_per_fat*256*d.vbr.sectors_per_cluster
    print("Lost space:", lost,"sectors =",lost*512,"bytes")
    
def mkdisk(fname,size):
    fp=open(fname,"wb")
    fp.seek(size*1024*1024-1)
    fp.write(b'0')
    bsize=fp.tell()
    fp.close()
    fname2 = fname + ".vmdk"
    fp=open(fname2,"w")
    #https://forums.virtualbox.org/viewtopic.php?f=7&t=52947
    print("version=1",file=fp)
    print("CID=deadbeef",file=fp)
    print("parentCID=ffffffff",file=fp)
    print('createType="fullDevice"',file=fp)
    print("RW "+str(bsize//512)+' FLAT "'+os.path.abspath(fname)+'" 0',file=fp)
    print("#DDB",file=fp)
    print('ddb.virtualHWVersion = "4"',file=fp)
    print('ddb.geometry.cylinders = "16383"',file=fp)
    print('ddb.geometry.heads = "16"',file=fp)
    print('ddb.adapterType = "lsilogic"',file=fp)
    print('ddb.toolsVersion = "7240"',file=fp)
    print('ddb.geometry.biosCylinders="1024"',file=fp)
    print('ddb.geometry.biosHeads="255"',file=fp)
    print('ddb.geometry.biosSectors="63"',file=fp)
    fp.close()

def mkpartition(fname):
    fp=open(fname,"r+b")
    fp.seek(0,2)
    sz=fp.tell()
    fp.seek(0)


    #Determine cyl/head/sector count
    #cyls must be a ten bit number
    #head is an 8 bit number
    #sector is a six bit number, but these start from one, not zero...

    #every head = 16MB
    numcyls = 1024
    numsects = 32
    #need to round down to nearest multiple of 16MB
    numheads = sz//16//1024//1024;

    if numheads > 256 or numcyls > 1024 or numsects > 64 :
        raise RuntimeError("Disk is too big:"+str(sz)+" "+str(numheads)+" "+str(numcyls)+" "+str(numsects))

    m=MBR()
    
    #write to partition table entry 1
    m.ptable[0].bootable=0x80
    
    m.ptable[0].shead = 1
    m.ptable[0].ssector = 1
    m.ptable[0].scyl = 0

    m.ptable[0].type = 0xe   #hardcode DOS type

    m.ptable[0].ehead = numheads-1
    m.ptable[0].esector = (( (numcyls-1) & 0xff00 )>>2) | (numsects)
    m.ptable[0].ecyl = ( (numcyls-1) & 0xff) 


    #always start on a track boundary
    m.ptable[0].start = numsects*( random.randrange(0,8) + 1);
    m.ptable[0].size = sz//512-m.ptable[0].start;

    m.signature[0] = 0x55
    m.signature[1] = 0xaa
    
    assert len(mbrcode) == 446
    m.mbr = mbrcode
    
    fp.write( string_at(addressof(m),512 ))
        
def mkfs(diskfile):
    fp=open(diskfile,"r+b")
    
    b=fp.read(512)
    m = MBR.from_buffer_copy(b)

    if m.signature[0] != 0x55 or m.signature[1] != 0xaa:
        raise RuntimeError("No valid partition table")

    ptable = m.ptable
    
    #size of disk in megabytes
    szm = ptable[0].size * 512//1024//1024 + 1;

    #compute sectors per cluster
    if( szm <= 16):     spc = 4;
    elif( szm <= 32):   spc = 1;    #(!)
    elif( szm <= 64):   spc = 2;
    elif( szm <= 128):  spc = 4;
    elif( szm <= 256):  spc = 8;
    elif( szm <= 512):  spc = 16;
    elif( szm <= 1024):  spc = 32;
    elif( szm <= 2048): spc = 64;
    else:           spc = 128;

    
    vbr = VBR()
    vbr.oem=b"mkfs    "
    vbr.jmp[0] = vbrcode[0]
    vbr.jmp[1] = vbrcode[1]
    vbr.jmp[2] = vbrcode[2]
    for i in range(62,len(vbrcode)):
        vbr.code[i-62] = vbrcode[i]
    
    
    
    num_fat_entries = ptable[0].size // spc
    assert ptable[0].size % spc == 0
    
    bytes_per_fat = num_fat_entries * 2 
    
    #round down
    bytes_per_fat &= ~511
    
    #sectors per fat
    sectors_per_fat = bytes_per_fat // 512
    
    #fixup value
    num_fat_entries = bytes_per_fat // 2
    
    assert bytes_per_fat % 512 == 0
    assert sectors_per_fat*256 == num_fat_entries
    assert sectors_per_fat < 256
    
    num_sectors = sectors_per_fat * 256 * spc
    assert num_sectors <= ptable[0].size 
    
    vbr.bytes_per_sector = 512
    vbr.sectors_per_cluster = spc
    vbr.vbr_sectors = 1
    vbr.num_fats = 2
    nrde = 512-32*(random.randrange(0,4))
    vbr.num_root_dir_entries = nrde
    if num_sectors < 65535:
        vbr.num_sectors_small = num_sectors
    else:
        vbr.num_sectors_small = 0
        
    vbr.id = 0xf8
    
    vbr.sectors_per_fat = sectors_per_fat

    assert vbr.sectors_per_fat * 256 == num_fat_entries
    
    vbr.sectors_per_track = 0  #ignored...
    vbr.num_heads = 0 #ignored
    vbr.first_sector = ptable[0].start
    vbr.num_sectors_big = num_sectors
    vbr.drive_number = 0x80;
    vbr.sig1 = 0x29;
    vbr.serial_number = 314159265;
    vbr.label = b"hello world"
    vbr.fstype = b"FAT16   "
    vbr.signature[0] = 0x55
    vbr.signature[1] = 0xaa
    
    fp.seek(m.ptable[0].start*512)
    fp.write( string_at(addressof(vbr),512) )

    #first two entries are allocated...
    fat=b'\xf8\xff\xff\xff' + bytes(512-4) + bytes(512)*(vbr.sectors_per_fat-1)
    fp.write(fat)
    fp.write(fat)

    #write root directory
    root = b'\x00' * vbr.num_root_dir_entries * 32
    fp.write(root)

def mchattr(d,path,mode):
    
    attr=0
    if "r" in mode:
        attr |= READONLY_BIT
    if "h" in mode:
        attr |= HIDDEN_BIT
    if "s" in mode:
        attr |= SYSTEM_BIT
    if "l" in mode:
        attr |= LABEL_BIT
    if "a" in mode:
        attr |= ARCHIVE_BIT

    #the entry we are changing
    dirent = d.get_dir_entry(path)
    dirent.attrib = (dirent.attrib & DIRECTORY_BIT) | attr 
    
    #the folder that holds the entry that is to be changed
    parentpath,junk = d.splitPath(path)
    parentdirent = d.get_dir_entry(parentpath)
    idx = d.get_dir_entry_index(parentdirent,dirent)
    
    if not parentdirent:
        #the file whose dirent we are changing is at the top level
        d.write_root_directory_entry(idx,dirent)
    else:
        #we need to rewrite the contents of the owning directory (the parent dir)
        tmp=bytearray(d.read_file(parentdirent))
        print("setting attrib on entry",idx,"to",dirent.attrib)
        tmp[idx*32+8+3]=dirent.attrib 
        
        grandparentpath,junk = d.splitPath(parentpath)
        grandparentdirent = d.get_dir_entry(grandparentpath)
        idx2 = d.get_dir_entry_index(grandparentdirent,parentdirent)
        d.rewrite_file(grandparentdirent,idx2,tmp)
        
    
def mls(d,path,verbose):
    
    if not path or path == '/':
        r = d.read_dir(None)
    else:
        e = d.get_dir_entry(path)
        if not (e.attrib & DIRECTORY_BIT ):
            raise RuntimeError("Not a directory")
            
        tmp = d.read_file(e)
        r=[]
        for i in range(0,len(tmp),32):
            r.append( DirEntry.from_buffer_copy(tmp[i:i+32]) )
            
    months = ["***","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    fbytes=0
    
    print("Name     Ext     Size Attr   Modified             Clusters") 
    for de in r:
        if de.base[0] != 0 and (verbose or de.base[0] != 0xe5):
            a=""
            if de.attrib & ARCHIVE_BIT: a += "A"
            else: a += " "
            if de.attrib & LABEL_BIT: a += "L"
            else: a += " "
            if de.attrib & DIRECTORY_BIT: a += "D"
            else: a += " "
            if de.attrib & HIDDEN_BIT: a += "H"
            else: a += " "
            if de.attrib & SYSTEM_BIT: a += "S"
            else: a += " "
            if de.attrib & READONLY_BIT: a += "R"
            else: a += " "
                
                
            hour = de.time >> 11
            minute = (de.time >> 5 ) & 0x3f
            sec = de.time & 0x1f
            sec *= 2
            year = (de.date >> 9) & 0x7f
            month = (de.date >> 5) & 0xf
            day = (de.date) & 0x1f
            print("%-8.8s %-3.3s %8d %6s %04d-%s-%02d %02d:%02d:%02d" %
                ( 
                "".join([chr(b) for b in de.base]),
                "".join([chr(b) for b in de.ext]),
                de.size, a,
                year+1980,months[month],day,hour,minute,sec
                ),
                end=" "
            )
            if de.base[0] != 0 and de.base[0] != 0xe5:
                c=d.clusters_for_file(de)
            else:
                c=[de.start]
                
            c=str(c)
            if len(c) > 30:
                c=c[:30]
                i=c.rfind(",")
                c=c[:i]
                c+="...]"
            print(c)
            
            fbytes += de.size
                
    
    #determine free space: free and used clusters
    fc=0;
    uc=0;
    for i in range(len(d.fat)):
        if( d.fat[i] == 0 ):
            fc+=1
        else:
            uc+=1

    print( 
        "{0:,} bytes free in {1:,} clusters\n{2:,} bytes used in {3:,} clusters".format(
            fc*d.vbr.sectors_per_cluster*512,fc,
            uc*d.vbr.sectors_per_cluster*512,uc
    ))
    print("{0:,} bytes per cluster\n{1:,} total clusters\n".format(d.vbr.sectors_per_cluster*512,
        len(d.fat) ))

def mrm(d,fname):
    d.remove_file(fname)
    
def main():
    diskfile = sys.argv[1]
    d = None
    
    args = sys.argv[2:]
    try:
        while len(args):
            action = args.pop(0)
            
            opts={}
            while len(args) > 0 and args[0].startswith("-"):
                tmp=args.pop(0)
                tmp=tmp.split("=",1)
                while tmp[0].startswith("-"):
                    tmp[0]=tmp[0][1:]
                if len(tmp) > 1:
                    opts[tmp[0]]=tmp[1]
                else:
                    opts[tmp[0]]=True
                
            if action == "mkdisk":
                size = int(opts["size"])
                mkdisk(diskfile,size)
                mkpartition(diskfile)
                mkfs(diskfile)
            elif action == "mcp":
                if not d: d = Disk(diskfile)
                randomize = ("r" in opts)
                src=args.pop(0)
                dst=args.pop(0)
                mcp(d,src,dst,randomize)
            elif action == "mfat":
                if not d: d = Disk(diskfile)
                src=args.pop(0)
                mfat(d,src)
            elif action == "mls":
                if not d: d = Disk(diskfile)
                path=args.pop(0)
                mls(d,path,"v" in opts)
            elif action == "mrm":
                if not d: d = Disk(diskfile)
                src=args.pop(0)
                mrm(d,src)
            elif action == "mkdir":
                if not d: d = Disk(diskfile)
                dname = args.pop(0)
                mkdir(d,dname)
            elif action == "mcat":
                if not d: d = Disk(diskfile)
                fname = args.pop(0)
                mcat(d,fname)
            elif action == "mchattr":
                if not d: d=Disk(diskfile)
                mode = args.pop(0)
                fname = args.pop(0)
                mchattr(d,fname,mode)
            else:
                print("Bad arguments: action=",action)
                sys.exit(1)
    except RuntimeError as e:
        print("Error:",e.args[0])
        raise


        
#import cProfile
#cProfile.run("main()")
main()
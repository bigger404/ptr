from random import randint

class ptr():

    def __init__(self,size,allocation):
        self.size=size                  #size in pages
        self.limit=100                  #max process size in pages
        self.allocation=allocation      #max frames to allocate

        self.ptr=[]
#        self.ram=[None]*64

        self.disk=[]                    #initialize sector list
        for page in range(self.size):
            ind=randint(0,len(self.disk))
            self.disk.insert(ind,page)

        self.loadPage(0)

    def loadPage(self,page_num):        #load page into ram and update PTR
        print("\t\t** Page fault occured **")
        sector = self.disk.index(page_num)
        frame_num=None
        if not self.isfull():                #add ptr entry at next free
            frame_num=len(self.ptr)
            self.ptr.append([page_num,frame_num,sector,0])
        else:
            frame_num=0
            self.ptr[0]=[page_num,frame_num,sector,0]#add to front of the ptr
        return frame_num

    def getPhysical(self,logical):
        offset = logical%16
        page_num = int(logical/16)
        frame_num=None
        found=False
        for record in self.ptr:
             if page_num==record[0]:
                frame_num=record[1]
                found=True
        if not found:
            frame_num = self.loadPage(page_num)
        return (frame_num*16) + offset

    def printPtr(self):
        print("P#,F#,Sector#, Valid/Invalid")
        for record in self.ptr:
            print(record)

    def isfull(self):
        return len(self.ptr)==self.allocation

def get_address(size):
    return randint(0,size*16)

if __name__ == '__main__':

    size=int(input("Size of program in pages: "))
    if size <1 or size > 100:
        size=100

    allocation=int(input("Maximum number of frames to allocate: "))
    if allocation <1 or allocation >64:
        allocation=64 

    p=ptr(size,allocation)

    while (True):
        logical = get_address(size)     #create a random logical address
        print("Logical Address: "+str(logical))
        print("Physical address: "+ str(p.getPhysical(logical)))
        p.printPtr()

        if input("Return for more. Q to quit \n").lower()=="q":
            break

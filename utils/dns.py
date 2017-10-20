import os
DIR="/root/working"
DNSLIST=[]
CNAMEDNSLIST=[]
def ddr():
    LIST=os.listdir(DIR)
    for i in range(0,len(LIST)):
        FILENAME=LIST[i]
        FILEDIR=os.path.join(DIR, LIST[i])
        TOPDNS=dnsnameget(FILENAME)
        file_obj=open(FILEDIR)
        lines=file_obj.readlines()
        for line in lines:
            if line.find('A')==-1:
                continue
            elif line.find('SOA')!=-1:
                continue
            elif line.find(';')!=-1:
                continue
            elif line.find('CNAME')!=-1:
                listline=line.split()
                CNAMEDNSLIST.append(listline[0]+'.'+TOPDNS+" CNAME "+listline[2][0:-1])
            elif line.find('A')!=-1:
                listline=line.split()
                if len(listline)==2:
                    DNSLIST.append(TOPDNS+" "+listline[1])
                elif len(listline)==3:
                    DNSLIST.append(listline[0]+'.'+TOPDNS+" "+listline[2])
    return DNSLIST+CNAMEDNSLIST

def writeFile(LIST):
    NEWFILE="/root/a.dns"
    output=open(NEWFILE,'w')
    for i in LIST:
        output.writelines(i+"\n")
    output.close()

def dnsnameget(filename):
    list=filename.split('.')
    dnsname=""
    for i in list:
        if i == "zone":
            break
        else:
            dnsname+=i+"."
    return dnsname[0:-1]

if __name__ == "__main__":
    writeFile(ddr())
import struct,sys,re
d=open(sys.argv[1],'rb').read()
t,hs,size,pkgc=struct.unpack_from('<HHII',d,0); o=hs
t2,hs2,sz2,cnt,stc,flags,ss,sts=struct.unpack_from('<HHIIIIII',d,o)
offs=struct.unpack_from('<%dI'%cnt,d,o+hs2)
def rd(i):
    p=o+ss+offs[i]; n=d[p];p+=1
    if n&0x80: p+=1
    b=d[p];p+=1
    if b&0x80: b=((b&0x7f)<<8)|d[p];p+=1
    return d[p:p+b]
w=open(sys.argv[2],'w')
for i in range(cnt):
    r=rd(i)
    if b'Instagram' in r and not re.fullmatch(rb'[^\s]*[./_:][^\s]*',r):
        s=r.decode('utf8','replace')
        w.write('%d\t%s\t=>\t%s\n'%(i,s.replace('\n',' '),s.replace('Instagram','Sohel').replace('\n',' ')))

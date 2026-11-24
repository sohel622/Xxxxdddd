import struct,sys,re
src,dst=sys.argv[1],sys.argv[2]
d=open(src,'rb').read()
t,hs,size,pkgc=struct.unpack_from('<HHII',d,0)
o=hs
t2,hs2,sz2,cnt,stc,flags,ss,sts=struct.unpack_from('<HHIIIIII',d,o)
assert t2==1 and flags&0x100 and stc==0 and sts==0
offs=struct.unpack_from('<%dI'%cnt,d,o+hs2)
def rd(i):
    p=o+ss+offs[i]
    n=d[p];p+=1
    if n&0x80: p+=1
    b=d[p];p+=1
    if b&0x80: b=((b&0x7f)<<8)|d[p];p+=1
    return d[p:p+b]
def enc(s):
    b=s.encode('utf8'); n=len(s.encode('utf-16-le'))//2
    def v(x): return bytes([x]) if x<0x80 else bytes([0x80|(x>>8),x&0xff])
    return v(n)+v(len(b))+b+b'\x00'
data=bytearray(); newoffs=[]; changed=0
for i in range(cnt):
    raw=rd(i)
    newoffs.append(len(data))
    if b'Instagram' in raw and not re.fullmatch(rb'[^\s]*[./_:][^\s]*',raw):
        k=raw.count(b'Instagram'); nb=raw.replace(b'Instagram',b'Sohel')
        p=o+ss+offs[i]; n=d[p]
        if n&0x80: n=((n&0x7f)<<8)|d[p+1]
        n-=4*k
        v=lambda x: bytes([x]) if x<0x80 else bytes([0x80|(x>>8),x&0xff])
        data+=v(n)+v(len(nb))+nb+b'\x00'; changed+=1
    else:
        p=o+ss+offs[i]; q=p+(2 if d[p]&0x80 else 1); q+=(2 if d[q]&0x80 else 1)
        data+=d[p:q+len(raw)+1]
while len(data)%4: data.append(0)
pool=struct.pack('<HHIIIIII',1,hs2,0,cnt,0,flags,hs2+4*cnt,0)+struct.pack('<%dI'%cnt,*newoffs)+bytes(data)
pool=pool[:4]+struct.pack('<I',len(pool))+pool[8:]
rest=d[o+sz2:]
out=struct.pack('<HHII',t,hs,hs+len(pool)+len(rest),pkgc)+pool+rest
open(dst,'wb').write(out)
print('changed',changed,'old',len(d),'new',len(out))

"""InstaZen V8.5: resources.arsc-এর ভেতরে একমাত্র "InstaZen" লেখাটা একই দৈর্ঘ্যে "Sohel" করে দেয়।
ব্যবহার: python3 patch_instazen_label.py resources.arsc
"""
import sys
p=sys.argv[1]
d=bytearray(open(p,'rb').read())
old=b'\x08\x08InstaZen\x00'
new=b'\x05\x05Sohel\x00\x00\x00\x00'
i=d.find(old)
if i<0: sys.exit('InstaZen পাওয়া যায়নি')
d[i:i+len(old)]=new
open(p,'wb').write(d)
print('patched at offset',i)

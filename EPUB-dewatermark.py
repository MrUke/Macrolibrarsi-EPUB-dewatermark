#!/usr/bin/env python
import zipfile, sys, re, os, time, datetime

filename=sys.argv[1]

workplace='/tmp/'+filename+'/'
output='/home/luca/'+filename+'.epub'
fakedate=time.mktime(datetime.datetime.strptime("01/01/1970", "%d/%m/%Y").timetuple())

#extracting .epub files
f = open('uploads/'+sys.argv[1], 'rb')
fz = zipfile.ZipFile(f)
for filename in fz.namelist():
    fz.extract(filename, workplace)
f.close()

#removing watermark
os.remove(workplace+'OEBPS/_license0.xhtml')
os.remove(workplace+'OEBPS/img/_img_license0.png')
os.rmdir(workplace+'OEBPS/img/')
for filename in os.listdir(workplace+'OEBPS'):
	if '.html' in filename:
		data=open(workplace+'OEBPS/'+filename,'r').read()
		f=open(workplace+'OEBPS/'+filename,'w')
		f.write(re.sub('<div style="display:none;visibility: hidden;">(.*?)</div>', '', data))
		f.close()
		os.utime(workplace+'OEBPS/'+filename, (fakedate,fakedate))

data=open(workplace+"OEBPS/content.opf",'r').read()
f=open(workplace+"OEBPS/content.opf",'w')
data=data.replace('\n    <item id="_img_license0" href="img/_img_license0.png" media-type="image/png" />','')
data=data.replace('\n    <item id="_license0" href="_license0.xhtml" media-type="application/xhtml+xml" />','')
f.write(data)
f.close()
os.utime(workplace+"OEBPS/content.opf", (fakedate,fakedate))

#rebuild the .epub
os.system('cd '+workplace+'&& zip -r '+output+' .')

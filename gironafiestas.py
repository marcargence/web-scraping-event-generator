from lxml.html import parse
import lxml.html
from urllib2 import urlopen
import re
from datetime import date

from dbconnectors import InsertDB

urlgironafiestas = "https://yourexamplesite"
mesos = ["January","February","March","April","May","June","July","August","September","October","November","December"]
da = date.today()
try:
    doc = parse(urlgironafiestas).getroot()
except IOError:
    doc = parse(urlopen(urlgironafiestas)).getroot()

li = doc.xpath("//ul[@id='fiestas']/li")
for element in li:
	diaI,mesI,anyI,mesF,diaF,anyF,url=("","","","","","","")
	dI,dF = None,None
	lloc =  element.xpath(".//a[@class='town']/text()")[0]
	data =  element.xpath(".//span[@class='dates']/text()")[0]
	titol2 = element.xpath(".//a[@class='name']")
	if titol2:
		titol = titol2[0].text
		url = titol2[0].get('href')
	else:
		titol2 = element.xpath(".//span[@class='name']")
		titol = titol2[0].text
		urlcode = element.xpath(".//a")
		if len(urlcode) > 0:
			url = urlcode[0].get('href')	
	if titol.strip() == "Festa major" or titol.strip() == "Festa Major":
		titol += " "+lloc
	if data:
		m = re.search("(del |de l.)(\d+) (de |d.)(\w+)", data)
		if m:
			diaI = m.group(2)
			mesI = m.group(4)	

			m = re.search("(al |a l.)(\d+) (de |d.)(\w+)", data)
			if m:
				diaF = m.group(2)
				mesF = m.group(4)
		else:
			m = re.search("(del |de l.)(\d+) (al |a l.)(\d+) (de |d.)(\w+)", data)
			if m:
				diaI = m.group(2)
				mesI = m.group(6)
				diaF = m.group(4)
				mesF = m.group(6)			
			else:	
				m = re.search('(\d+) (de |d.)(\w+)', data)
				if m:
					diaI = m.group(1)
					mesI = m.group(3)
		mesI = mesos.index(mesI)+1					
		anyI = da.year				
		if da.month	> mesI:
			anyI = da.year + 1	
		dI = date(int(anyI), int(mesI), int(diaI))		
		if mesF:
			mesF = mesos.index(mesF)+1		
			anyF = da.year				
			if da.month	> mesI:
				anyF = da.year + 1			
			dF = date(int(anyF), int(mesF), int(diaF))							
	print "----------------------------------------------------------------"	
	print "data: "+data.encode('utf-8')			
	print "lloc: "+lloc.encode('utf-8')
	print "titol: -"+titol.encode('utf-8')+"-"	
	print "diaI diaF: "+str(diaI)+"/"+str(mesI)+"/"+str(anyI)+"-"+(diaF)+str(mesF)		
	url = "https://festamajor.de"+url	
	print "url: "+url
	InsertDB(titol,dI,dF,"",lloc,'','','','',url)

import lxml.html
import re
from datetime import date
import time

from dbconnectors import InsertDB

urldescobrircat = "http://www.examplesite.com"
mesos = ["January","February","March","April","May","June","July","August","September","October","November","December"]
da = date.today()

doc = lxml.html.parse(urldescobrircat).getroot()
time.sleep(1)

divs = doc.xpath("//div[@class='itemInici']")
for element in divs:
	diaI,mesI,anyI,mesF,diaF,anyF,dies,dies2,dataF,contacteweb1=("","","","","","","1","1","","")
	url = element.find('.//a').get('href')
	imatge = element.find('.//img').get('src')
	data = element.xpath(".//p[@class='data']/text()")[0]
	titol = element.xpath(".//p[@class='titol']/text()")[0]
	desc = element.xpath(".//p[@class='text']/text()")[0]
	
	if data:
		m = re.search("(DEL |DE L.)(\d+) (DE |D.)(\w+)", data)
		if m:
			diaI = m.group(2)
			mesI = m.group(4)	

			m = re.search("(AL |A L.)(\d+) (DE |D.)(\w+)", data)
			if m:
				diaF = m.group(2)
				mesF = m.group(4)
		else:
			m = re.search("(DEL |DEL L.)(\d+) (AL |A L.)(\d+) (DE |D.)(\w+)", data)
			if m:
				diaI = m.group(2)
				mesI = m.group(6)
				diaF = m.group(4)
				mesF = m.group(6)			
			else:	
				m = re.search('(\d+) (DE |D.)(\w+)', data)
				if m:
					diaI = m.group(1)
					mesI = m.group(3)
		#print "Dia:"+diaI+"/"+mesI+"/"+anyI+"/"+diaF+"/"+mesF+"/"+anyF	
		if mesI:
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
	
			if any( x in titol for x in["Fira","Festival","Tast","tast","fira","festival"] ):
				print "----------------------------------------------------------------"
				print "imatge: "+imatge
				url = "http://exampleurldetails"+url		
				print "url: "+url
				print "titol: "+titol.encode('utf-8')
				print "data: "+data
				print "Dia:"+str(diaI)+"/"+str(mesI)+"/"+str(anyI)+"-"+(diaF)+"/"+str(mesF)+"/"+str(anyF)
				print "desc:"+desc.encode('utf-8')
				InsertDB(titol,dI,dF,imatge,"","","",desc,'',url)
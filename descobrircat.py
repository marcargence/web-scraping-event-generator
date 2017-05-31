import lxml.html
import re
from datetime import date

from dbconnectors import InsertDB

diespermesos = 30
urldescobrircat = "http://www.examplesite.com"
doc = lxml.html.parse(urldescobrircat).getroot()
mesos = ["January","February","March","April","May","June","July","August","September","October","November","December"]
da = date.today()

divs = doc.xpath("//div[@class='v-list-item']")
for element in divs:
	diaI,mesI,anyI,mesF,diaF,anyF,urlimg,diesEvent=("","","","","","","","1")
	dF = None
	imgcode = element.find('.//img')
	if imgcode is not None:
		urlimg = imgcode.get('src')
	text = element.xpath(".//div[@class='v-list-item-title']")[0]
	urlart = text.find(".//a").get('href')
	titol = text.find(".//h2").text
	text2 = element.xpath(".//div[@class='v-list-item-info']")[0]
	data = text2.find(".//span").text
	lloc = text2.xpath(".//p/text()")[1]
	lloc = lloc.replace(" - ","")
	#lloc = lxml.html.tostring(lloc1)
	text3 = element.xpath(".//div[@class='v-list-item-desc']")[0]
	#descripcio1 = text3.find(".//p")
	#descripcio = lxml.html.tostring(descripcio1)
	descripcio = text3.xpath(".//p/text()")[0]
	if data:
		m = re.search("(Del |De l\')(\d+) (de |d\')(\w+)", data)
		if m:
			diaI = m.group(2)
			mesI = m.group(4)	

			m = re.search("(al |a l\')(\d+) (de |d\')(\w+)", data)
			if m:
				diaF = m.group(2)
				mesF = m.group(4)
		else:
			m = re.search("(Del |De l\')(\d+) (al |a l\')(\d+) (de |d\')(\w+)", data)
			if m:
				diaI = m.group(2)
				mesI = m.group(6)
				diaF = m.group(4)
				mesF = m.group(6)			
			else:	
				m = re.search('(\d+) (de |d\')(\w+)', data)
				if m:
					diaI = m.group(1)
					mesI = m.group(3)
		mesI = mesos.index(mesI)+1					
		anyI = da.year				
		if da.month	< mesI:
			anyI = da.year + 1	
		dI = date(int(anyI), int(mesI), int(diaI))		
		if mesF:
			mesF = mesos.index(mesF)+1		
			anyF = da.year				
			if da.month	< mesI:
				anyF = da.year + 1			
			dF = date(int(anyF), int(mesF), int(diaF))	
			delta = dF - dI	
			diesEvent = str(delta.days)
		delta2 = dI - da
		diesPerInici = str(abs(delta2.days))			
	m = re.search("(.*) \((.*)\)", lloc)
	if m:
			lloc1 = m.group(1)
			lloc2 = m.group(2)
	m = re.search("(Vic|Giron)", lloc)
	#print "lloc: "+lloc	
	#print "dies:"+diesEvent+" "+diesPerInici		
	if m and int(diesEvent) < diespermesos and int(diesPerInici) < diespermesos:			
		print "----------------------------------------------------------------"	
		print "data: "+data				
		print "urlimg: "+urlimg	
		print "lloc: "+lloc.encode('utf-8')+"-"+lloc1.encode('utf-8')+"-"+lloc2.encode('utf-8')
		print "descripcio: "+descripcio.encode('utf-8').strip()
		print "titol: "+titol.encode('utf-8')	
		print "diaI diaF: "+str(diaI)+"/"+str(mesI)+"/"+str(anyI)+"-"+(diaF)+str(mesF)	
		print "mesF: "+str(mesF)
		InsertDB(titol,dI,dF,urlimg,lloc1,'',lloc2,descripcio,'','')

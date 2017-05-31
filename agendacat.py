import lxml.html
import re
from datetime import date
import time
from lepl.apps.rfc3696 import HttpUrl
validator = HttpUrl()

from dbconnectors import InsertDB

diespermesos = 16
urldescobrircat = "http://www.examplesite.com"
da = date.today()

for n in range(1, 10):
	doc = lxml.html.parse(urldescobrircat+str(n)).getroot()
	time.sleep(1)

	divs = doc.xpath("//div[@class='listItem  noLogo']")
	for element in divs:
		diaI,mesI,anyI,mesF,diaF,anyF,dies,dies2,dataF,contacteweb1,desc,lloc1,lloc2=("","","","","","","1","1","","","","","")
		dI,dF = None,None
		diesEvent,diesPerInici=1,1
		imatge = element.find('.//img').get('src')
		contingut = element.xpath(".//span[@class='title']")[0]
		url2 = contingut.find('.//a').get('href')
		url2 = "http://www.exmapledetailedsite"+url2
		titol = contingut.find('.//a').text
		#print "-----titol: "+titol.encode('utf-8')+"----"
		
		#busquem dins de cada link entrada detallada
		url2 = url2.encode('utf-8')
		#print url2
		if validator(url2):
			doc2 = lxml.html.parse(url2.encode('utf-8')).getroot()
			descr = doc2.xpath("//div[@class='itemDesc']")[0]
			rows = descr.xpath("//div[@class='row']")
			for row in rows:
				if row.find(".//b") is not None:
					bold = row.find(".//b")
					if bold.text.find("inici") != -1:
						datain = row.find(".//span").text
						m = re.search("(\d\d)\/(\d\d)\/(\d\d\d\d)", datain)
						if m:
							diaI = m.group(1)
							mesI = m.group(2)
							anyI = m.group(3)		
					if bold.text.find("final") != -1:
						datafi = row.find(".//span").text
						m = re.search("(\d\d)\/(\d\d)\/(\d\d\d\d)", datafi)
						if m:
							diaF = m.group(1)
							mesF = m.group(2)
							anyF = m.group(3)
							dF = date(int(anyF), int(mesF), int(diaF))	
					if bold.text.find("Municipi") != -1:
						lloc1 = row.find(".//span").text.strip()
						#print "lloc1"+lloc1	
					#if bold.text.find("Localitat") != -1:
					#	lloc1 += " "+row.find(".//span").text
					if bold.text.find("Marca Tur") != -1:
						lloc2 = row.find(".//span").text.strip()
						#print "lloc2"+lloc2					
					if bold.text.find("Web") != -1:
						contacteweb1 = row.find(".//a").get("href")				
			
			#print "dia"+diaI+" "+mesI+" "+anyI
			dI = date(int(anyI), int(mesI), int(diaI))
			if(diaF):
				dF = date(int(anyF), int(mesF), int(diaF))
				delta = dF - dI	
				diesEvent = str(delta.days)
				#print "diesevent "+diesEvent
				dataF = diaF+"/"+mesF+"/"+anyF
			delta2 = dI - da
			diesPerInici = str(abs(delta2.days))
			#print "diesperinici "+diesPerInici
			
			if((lloc2 in ["place"] or lloc1 in ["country1","country2"]) and int(diesEvent) < diespermesos and int(diesPerInici) < diespermesos):
				print "----------------------------------------------------------------"
				print "imatge: "+imatge
				print "url2: "+url2
				print "titol: "+titol.encode('utf-8')
				print "Dia:"+diaI+"/"+mesI+"/"+anyI+"/"+diaF+"/"+mesF+"/"+anyF	
				print "dies:"+diesEvent+" "+diesPerInici	
				print "lloc: "+lloc1.encode('utf-8')+"/"+lloc2.encode('utf-8')	
				#print "contacte"+correuitelf.encode('utf-8')+" "+direccio.encode('utf-8')	
				print "web"+contacteweb1.encode('utf-8')	
				print "desc:"+desc.encode('utf-8').strip()	
				#titol = titol.encode('utf-8')
				#desc = desc.encode('utf-8').strip()
				InsertDB(titol,dI,dF,imatge,lloc1,contacteweb1,lloc2,desc,'',url2)


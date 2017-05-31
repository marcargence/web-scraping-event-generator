from datetime import date
import mysql.connector

dbwordpress="wordpressdb";
usuaridb="username";
passdb="password";
taula="wp_posts";

def InsertDB(titol,dataI,dataF,img,lloc,adreca,municipi,descripcio,web,urlmesinfo):
	(htmlImg,htmlData,contingut)=("","","")
	currentdate = date.today()	
	cnx = mysql.connector.connect(user=usuaridb, password=passdb, database=dbwordpress)
	cursor = cnx.cursor(buffered=True)
	titol = titol.replace(':','')
	
	#SELECT
	query = ("SELECT post_title FROM "+taula+" WHERE `post_title`=%s")
	cursor.execute(query, (titol,))
	#lastid = cursor.lastrowid
	#print "POP"+cursor
	if cursor.rowcount:
		print "***UPDATE***: "+titol.encode('utf-8')+"!\n";
	else:
		query = "SELECT max(ID) as maxid FROM "+taula
		cursor.execute(query)		
		for (maxid) in cursor:
		  lastid = int(maxid[0])
		lastid += 1
		if(img):
			htmlImg = "<div style='float: left;'><img style='max-width: 250px; width: 100%; height: auto;' src='"+img+"'></div>"
		if(dataI):
			htmlData = "<b>Data Inici:</b> "+str(dataI.day)+"/"+str(dataI.month)+"/"+str(dataI.year)+"<br>"
		if(dataF):			
			htmlData += "<b>Data Final:</b> "+str(dataF.day)+"/"+str(dataF.month)+"/"+str(dataF.year)
		if(web):
			web = "<a href='"+web+"'>WEB OFICIAL</a>"
		if(urlmesinfo):
			urlmesinfo = "<a href='"+urlmesinfo+"'>M&eacute;s info</a>"
		
		contingut = htmlImg
		contingut += "<div  style='float: left; margin-left: 5px;'><div><b>"+titol+"</b></div>"
		contingut += "<div>"+htmlData+"</div>"
		if municipi:
			municipi = ", "+municipi
		if lloc or adreca or municipi:
			contingut += "<div style='margin-top: 5px;'><b>Direccio:</b> "+lloc+" "+adreca+municipi+"</div>"
		contingut += "</div><div style='float: left; clear: left; margin-left: 5px;'><div style='margin-top: 5px;'>"+descripcio+"</div>"
		contingut += "<div style='margin-top: 5px;'>"+web+urlmesinfo+"</div></div>"
		
		#contingut = cnx.converter.escape(contingut)
		#contingut = htmlImg+titol+"\r\n "+htmlData+"\r\n  <b>Direccio:</b> "+lloc+" "+adreca+", "+municipi+"\r\n"+descripcio+"\r\n"+web+urlmesinfo
			
		#INSERT
		add_insert = "INSERT INTO "+taula+" (ID, post_author, post_date, post_date_gmt, post_content, "
		add_insert += "post_title, post_excerpt, post_status, comment_status, ping_status, post_password, "
		add_insert += "post_name, to_ping, pinged, post_modified, post_modified_gmt, post_content_filtered, "
		add_insert += "post_parent, guid, menu_order, post_type, post_mime_type, comment_count) VALUES "
		add_insert += "("+str(lastid)+", 1, %s, %s, %s, %s, '', 'publish', 'open', 'open', '', %s, '', '', %s, %s, "
		add_insert += "'', 0, 'http://82.223.29.109/?p="+str(lastid)+"', 0, 'post', '', 0)"
		
		#print "lastid: "+lastid
		#currentdate =str(currentdate) dataI
		if(dataF):	
			datamod = dataF
		else:
			datamod = dataI
		data_insert = (dataI, currentdate, contingut, titol, titol, datamod, currentdate)

		#print data_insert
		cursor.execute(add_insert, data_insert)
		blog_id = cursor.lastrowid
		if(not blog_id):
			print "***ERROR INSERT*** last log_id"
		else:
			print "***INSERT***: "+titol.encode('utf-8')+"\n";		

	# Make sure data is committed to the database
	cnx.commit()
	cursor.close()
	cnx.close()
	return

def borrarAntics():
	currentdate = date.today()	
	cnx = mysql.connector.connect(user=usuaridb, password=passdb, database=dbwordpress)
	cursor = cnx.cursor(buffered=True)
	add_insert = "UPDATE "+taula+" SET post_status='trash' WHERE `post_modified`<%s;";
	data_insert = (currentdate,)
	cursor.execute(add_insert, data_insert)
	cnx.commit()
	cursor.close()
	cnx.close()
	return
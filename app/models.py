
import sqlite3 as sql


def retrieveUsers(username, password, x):
	con = sql.connect("EBL.db")
	cur = con.cursor()


	#cur = con.cursor(pymysql.cursor)
	#cur = con.cursor(MySQLdb.cursors.DictCursor)
#cursor.execute("SELECT name, category FROM animal")



	#cur.execute("SELECT username, password FROM user")
	cur.execute('SELECT username from user where username = (?) and password = (?)', (username, password))

	users = cur.fetchall()
	
	
	
	if x==0:
		if users == []:
			users = 'False'
		else:	
			users = "True"
	

	con.close()
	
	return users




def retrieve(username):
	con = sql.connect("EBL.db")
	cur = con.cursor()


	#cur = con.cursor(pymysql.cursor)
	#cur = con.cursor(MySQLdb.cursors.DictCursor)
#cursor.execute("SELECT name, category FROM animal")



	#cur.execute("SELECT username, password FROM user")
	cur.execute('SELECT * from user where username = (?)', (username,))

	users = cur.fetchall()
	
	
	
	
	con.close()
	
	return users


def retrieveallcompany():
	con = sql.connect("EBL.db")
	cur = con.cursor()


	cur.execute('SELECT * from bankname ')

	companies = cur.fetchall()
	
	
	
	
	con.close()
	
	return companies



def retrievecompanystartdate():
	con = sql.connect("EBL.db")
	cur = con.cursor()

	startdate = []
	cur.execute('SELECT * from bankname ')

	companies = cur.fetchall()
	
	for row in companies:
		name = row[1]
		cur.execute('SELECT * from {} where id = 1 '.format(name))
		rows = cur.fetchone()
		x = rows[1]
		startdate.append(x) 			
	
	con.close()
	
	return startdate


def retrievecompanyenddate():
	con = sql.connect("EBL.db")
	cur = con.cursor()
	enddate = []
	cur.execute('SELECT * from bankname ')
	companies = cur.fetchall()
	for row in companies:
		name = row[1]
		cur.execute('SELECT * from {} where id = (SELECT max(id) FROM {} )'.format(name, name))
		rows = cur.fetchone()
		y = rows[1]
		enddate.append(y) 			
	
	con.close()
	
	return enddate

def retrievestartdate(path):
	con = sql.connect("EBL.db")
	cur = con.cursor()

	startdate = []
	cur.execute('SELECT * from {} where id = 12'.format(path))
	
	date = cur.fetchall()
	
	for row in date:
		startdate= row[1]

	con.close()
	
	return startdate


def retrieveenddate(path):

	con = sql.connect("EBL.db")
	cur = con.cursor()

	enddate = []
	cur.execute('SELECT * from {} where id = (SELECT max(id) FROM {} )'.format(path, path))
	
	date = cur.fetchall()
	
	for row in date:
		enddate= row[1]

	con.close()
	
	return enddate
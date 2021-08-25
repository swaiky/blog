#!/usr/bin/python3
 
import pymysql
 
# 增
def useSqliteInsert(dic):
	conn = pymysql.connect("localhost","root","bear","lldatabase",port=3306,charset='utf8')
	cursor = conn.cursor()
	string = ''
	string2 = ''
	string3 = ''
	arr3 = []
	string33 = ''
	for x in dic:
		if x=='database':
			continue
			pass
		if x=='table':
			continue
			pass
		if string == '':
			string = x + ' ' +'text'
			string2=x
			string3= '\''+ dic[x]+'\''
			string33 = '?'
			pass
		else:
			string = string+', ' + x + ' ' +'text'
			string2 = string2+','+x
			string3 = string3+','+'\''+ pymysql.escape_string(str(dic[x]))+'\''
			string33 = string33 + ',' + '?'
		arr3.append(dic[x])
		pass

	try:
		print('create table if not exists '+dic["table"]+' (id integer NOT NULL PRIMARY KEY auto_increment , '+ string +')')
		cursor.execute('create table if not exists '+dic["table"]+' (id integer NOT NULL PRIMARY KEY auto_increment , '+ string +')')
		string3 = string3.replace("'",'"')
		cursor.execute('insert into '+dic["table"]+' ('+string2+') values ('+string3+')')
	except Exception as e:
		print("---------------error---------------")
		print(e)
		print("---------------error---------------")
		print('insert into '+dic["table"]+' ('+string2+') values ('+string3+')')
		cursor.execute('insert into '+dic["table"]+' ('+string2+') values ('+string3+')')
	cursor.close()
	conn.commit()
	conn.close()

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d
# 删
def useSqliteDelete(data):
	conn = pymysql.connect("localhost","root","bear","lldatabase",port=3306,charset='utf8')
	conn.row_factory = dict_factory 
	cursor = conn.cursor()
	print('===========================')
	# print('DELETE  from ' + data["table"] + ' WHERE id=\'' + data["id"]+'\'')
	try:
		cursor.execute('DELETE  from ' + data["table"] + ' WHERE id=\'' + data["id"]+'\'')
		pass
	except Exception as e:
		print(e)
		raise
	cursor.close()
	conn.commit()
	conn.close()

# 查
def useSqliteSelect(database,table):
	conn = pymysql.connect("localhost","root","bear","lldatabase",port=3306,charset='utf8',cursorclass = pymysql.cursors.DictCursor)
	conn.row_factory = dict_factory 
	cursor = conn.cursor()
	print('SELECT * from '+table)
	cursor.execute('SELECT * from '+table)
	values = cursor.fetchall()
	cursor.close()
	conn.commit()
	conn.close()
	return values
from itertools import chain

# 查
def useSqliteSelectByKey(dic):
	conn = pymysql.connect("localhost","root","bear","lldatabase",port=3306,charset='utf8',cursorclass = pymysql.cursors.DictCursor)
	conn.row_factory = dict_factory 

	# cursor=conn.cursor(pymysql.cursors.DictCursor)
	# cursor=pymysql.cursors.Dictcursor(conn)

	cursor = conn.cursor()
	# print('SELECT * from '+table+' WHERE nickname = '+key)
	# print('SELECT * from '+dic["table"]+' WHERE '+ dic['key'] +' = '+str(dic["value"] )+'  limit '+str(dic["limit"])+' offset '+str(int(dic["offset"])*int(dic["limit"])))
	cursor.execute('SELECT * from '+dic["table"]+' WHERE '+ dic['key'] +' = \''+str(dic["value"] )+'\'')
	print('------------')
	print('SELECT * from '+dic["table"]+' WHERE '+ dic['key'] +' = \''+str(dic["value"] )+'\'')
	# cursor.execute('SELECT * from '+dic["table"]+' WHERE '+ dic['key'] +' = \''+str(dic["value"] )+'\' ORDER BY id desc limit '+str(dic["limit"])+' offset '+str(dic["offset"]))
	# list=get_list('SELECT * from '+dic["table"]+' WHERE '+ dic['key'] +' = \''+str(dic["value"] )+'\'')
	# print('list:',list)
	values = cursor.fetchall()
	# print(values)
	# values2 = list(chain.from_iterable(values))
	# values=values2
	# print('xxxxxxxxxxxxxxxxxxx')
	# print(values)
	cursor.close()
	conn.commit()
	conn.close()
	return values
# 改
def useSqliteUpdate(dic):
	conn = pymysql.connect("localhost","root","bear","lldatabase",port=3306,charset='utf8')
	cursor = conn.cursor()
	string3 = ''
	
	for x in dic:
		if x=='database':
			continue
			pass
		if x=='table':
			continue
			pass
		if x=='id':
			continue
			pass
		if string3 == '':
	
			string3= x +' = ' '\''+ str(dic[x])+'\''
			pass
		else:
		
			string3 = string3+' , '+  x +' = ' '\''+ str(dic[x])+'\''
		pass
	# cursor.execute('create table if not exists '+dic["key"]+' (id integer NOT NULL PRIMARY KEY AUTOINCREMENT , '+ string +')')
	astr = 'UPDATE '+dic["table"]+' SET '+string3+' WHERE id = \''+str(dic["id"])+'\''
	print(astr)
	cursor.execute(astr)
	cursor.close()
	conn.commit()
	conn.close()

# 查询数据库中的所有表名
def useSqliteAllTable(dic):
	conn = pymysql.connect("localhost","root","bear","lldatabase",port=3306,charset='utf8')
	cursor = conn.cursor()
	astr = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
	cursor.execute(astr)
	values = cursor.fetchall()
	cursor.close()
	conn.commit()
	conn.close()
	return values

# 查询表中所有的字段名
def userSqliteTabelDetail(dic):
	conn = pymysql.connect("localhost","root","bear","lldatabase",port=3306,charset='utf8')
	cursor = conn.cursor()
	table = dic["table"]
	cursor.execute('pragma table_info('+table+')')
	col_name=cursor.fetchall()
	col_name=[x[1] for x in col_name]
	values = []
	for x in col_name:
		if x=='id':
			continue
			pass
		values.append(x)
		pass
	# cursor.execute(astr)
	# values = cursor.fetchall()
	# print(values)
	cursor.close()
	conn.commit()
	conn.close()
	return values

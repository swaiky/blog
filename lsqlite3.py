# -*- coding: utf-8 -*-
import sqlite3

# 增
def useSqliteInsert(dic):
	# print("进入插入")
	conn = sqlite3.connect(r'database/'+dic["database"]+'.sqlite3')
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
			string3= '\''+str( dic[x])+'\''
			string33 = '?'
			pass
		else:
			string = string+', ' + x + ' ' +'text'
			string2 = string2+','+x
			string3 = string3+','+'\''+ str(dic[x])+'\''
			string33 = string33 + ',' + '?'
		arr3.append(dic[x])
		pass
	try:
		cursor.execute('create table if not exists '+dic["table"]+' (id integer NOT NULL PRIMARY KEY AUTOINCREMENT , '+ string +')')
		# print('insert into '+dic["table"]+' ('+string2+') values ('+string3+')')
		string3 = string3.replace("'",'"')
		cursor.execute('insert into '+dic["table"]+' ('+string2+') values ('+string33+')',arr3)
	except:
		print("---------------error---------------")
		print('insert into '+dic["table"]+' ('+string2+') values ('+string3+')')
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
	conn = sqlite3.connect(r'database/'+data['database']+'.sqlite3')
	conn.row_factory = dict_factory 
	cursor = conn.cursor()
	print('===========================')
	# print('DELETE  from ' + data["table"] + ' WHERE id=\'' + data["id"]+'\'')
	cursor.execute('DELETE  from ' + data["table"] + ' WHERE id= ?',[data["id"]])
	cursor.close()
	conn.commit()
	conn.close()

# 查
def useSqliteSelect(database,table):
	conn = sqlite3.connect(r'database/'+database+'.sqlite3')
	conn.row_factory = dict_factory 
	cursor = conn.cursor()
	cursor.execute('SELECT * from '+table)
	values = cursor.fetchall()
	cursor.close()
	conn.commit()
	conn.close()
	return values

# 查
def useSqliteSelectByKey(dic):
	conn = sqlite3.connect(r'database/'+dic['database']+'.sqlite3')
	conn.row_factory = dict_factory 
	cursor = conn.cursor()
	# print('SELECT * from '+table+' WHERE nickname = '+key)
	# print('SELECT * from '+dic["table"]+' WHERE '+ dic['key'] +' = '+str(dic["value"] )+'  limit '+str(dic["limit"])+' offset '+str(int(dic["offset"])*int(dic["limit"])))
	cursor.execute('SELECT * from '+dic["table"]+' WHERE '+ dic['key'] +' = \''+str(dic["value"] + '\''))
	values = cursor.fetchall()
	cursor.close()
	conn.commit()
	conn.close()
	return values
# 改
def useSqliteUpdate(dic):
	conn = sqlite3.connect(r'database/'+dic["database"]+'.sqlite3')
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
	conn = sqlite3.connect(r'database/'+dic["database"]+'.sqlite3')
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
	conn = sqlite3.connect(r'database/'+dic["database"]+'.sqlite3')
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



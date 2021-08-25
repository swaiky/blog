# -*- coding: utf-8 -*-


from flask import Flask, url_for, redirect, render_template, request, Response, stream_with_context
import json
import os
import time
import codecs
from flask_cors import *
from pydub import AudioSegment
import lsqlite3
import lmysql
# 音频拼接
app = Flask(__name__)
# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求 
CORS(app, resources=r'/*')

databaseUse = 'sqlite3'
# databaseUse = 'mysql'

# 创建目录
def mkdir(path):
	# 引入模块
	import os

	# 去除首位空格
	path=path.strip()
	# 去除尾部 \ 符号
	path=path.rstrip("\\")

	# 判断路径是否存在
	# 存在	 True
	# 不存在   False
	isExists=os.path.exists(path)

	# 判断结果
	if not isExists:
		# 如果不存在则创建目录
		# 创建目录操作函数
		os.makedirs(path) 

		print(path+' 创建成功')
		return True
	else:
		# 如果目录存在则不创建，并提示目录已存在
		print(path+' 目录已存在')
		return False


# 中文翻译成日文
@app.route("/fanyi",methods=['GET'])
def fanyi():
	#使用方法
	from googletrans import Translator
	# name = request.args.get('name','erro')
	translator = Translator(service_urls=['translate.google.cn'])
	source = request.args.get('name','erro')
	text = translator.translate(source,src='zh-cn',dest='ja').text
	print(text)


	translator = Translator()
	print(translator.translate('星期日').text)

	translator = Translator()
	print(translator.translate('Sunday', dest='zh-CN').text)

	return json.dumps({"data":text})
	pass

# 翻译成英文
@app.route("/fanyichengyingwen",methods=['GET'])
def fanyichengyingwen():
	#使用方法
	from googletrans import Translator
	# name = request.args.get('name','erro')
	translator = Translator(service_urls=['translate.google.cn'])
	source = request.args.get('name','erro')

	return json.dumps({"data":translator.translate(source).text})
	pass

# 翻译成中文
@app.route("/fanyichengzhongwen",methods=['GET'])
def fanyichengzhongwen():
	#使用方法
	from googletrans import Translator
	# name = request.args.get('name','erro')
	translator = Translator(service_urls=['translate.google.cn'])
	source = request.args.get('name','erro')

	return json.dumps({"data":translator.translate(source, dest='zh-CN').text})
	pass


# 根据id修改数据
@app.route("/updatedata",methods=['POST'])
def updatedata():
	data = request.get_data().decode('utf-8')
	data = json.loads(data)
	if databaseUse=='sqlite3':
		lsqlite3.useSqliteUpdate(data)
		return json.dumps({"msg":"保存成功"})
	if databaseUse=='mysql':
		lmysql.useSqliteUpdate(data)
		return json.dumps({"msg":"保存成功"})
	return json.dumps({"msg":"保存成功"})

# 根据id删除数据
@app.route("/deldata",methods=['GET'])
def deldata():
	table = request.args.get('table','erro')
	database = request.args.get('database','erro')
	apath = table
	if databaseUse=='sqlite3':
		lsqlite3.useSqliteDelete({"database":database,'table':table,"id":request.args.get('id','erro')})
		return json.dumps({"msg":"删除成功"})
	if databaseUse=='mysql':
		lmysql.useSqliteDelete({"database":database,'table':table,"id":request.args.get('id','erro')})
		return json.dumps({"msg":"删除成功"})

	return json.dumps({"msg":"删除成功"})

# 上传数据
@app.route("/savedata",methods=['POST'])
def savedata():
	data = request.get_data().decode('utf-8')
	data = json.loads(data)
	data['creatTime']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	if databaseUse=='sqlite3':
		lsqlite3.useSqliteInsert(data)
		return json.dumps({"msg":"保存成功"})
	if databaseUse=='mysql':
		lmysql.useSqliteInsert(data)
		return json.dumps({"msg":"保存成功"})
	return json.dumps({"msg":"保存成功"})

# 获取每一行数据
@app.route("/getdata",methods=['GET'])
def getdata():
	table = request.args.get('table','erro')
	database = request.args.get('database','erro')
	if databaseUse=='sqlite3':
		try:
			return json.dumps({"msg":"获取成功","data":lsqlite3.useSqliteSelect(database,table)})
			pass
		except Exception as e:
			return json.dumps({"msg":"获取成功","data":[]})
	if databaseUse=='mysql':
		try:
			return json.dumps({"msg":"获取成功","data":lmysql.useSqliteSelect(database,table)})
		except Exception as e:
			return json.dumps({"msg":"获取成功","data":[]})
	return json.dumps({"msg":"获取成功","data":[]})
@app.route("/getdatabykey",methods=['POST'])
def getdatabykey():
	data = request.get_data().decode('utf-8')
	# data = json.loads(data)
	data = request.form.to_dict()
	if databaseUse=='sqlite3':
		try:
			return json.dumps({"msg":"获取成功","data":lsqlite3.useSqliteSelectByKey(data)})
			pass
		except Exception as e:
			print('----------')
			print(e)
			return json.dumps({"msg":"获取成功","data":[]})
	if databaseUse=='mysql':
		try:
			return json.dumps({"msg":"获取成功","data":lmysql.useSqliteSelectByKey(data)})
		except Exception as e:
			print(e)
			return json.dumps({"msg":"获取成功","data":[]})
	return json.dumps({"msg":"获取成功","data":[]})
# 获取所有数据库
@app.route("/getalldatabase",methods=['GET'])
def getalldatabase():
	if databaseUse=='sqlite3':
		alist = os.listdir('database')
		blist = []
		for x in alist:
			if 'sqlite3' in x:
				blist.append(x)
				pass
			pass
		return json.dumps({"msg":"获取成功","data":blist})
	return json.dumps({"msg":"获取成功"})

# 获取数据库下所有表
@app.route("/getalltable",methods=['GET'])
def getalltable():
	database = request.args.get('database','erro')
	if databaseUse=='sqlite3':
		return json.dumps({"msg":"获取成功","data":lsqlite3.useSqliteAllTable({"database":database})})
	return json.dumps({"msg":"获取成功"})

# 查询表中所有的字段名
@app.route("/getalltableDetail",methods=['GET'])
def getalltableDetail():
	table = request.args.get('table','erro')
	database = request.args.get('database','erro')
	if databaseUse=='sqlite3':
		return json.dumps({"msg":"获取成功","data":lsqlite3.userSqliteTabelDetail({"table":table,"database":database})})
	return json.dumps({"msg":"获取成功"})



# post请求 上传文件
@app.route("/uploadfile",methods=['POST'])
def uploadfile():
	f = request.files['the_file']
	imgName = (time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))+f.filename
	f.save(r'static/upload/' +imgName)
	return json.dumps({"msg":'上传成功',"path":r'static/upload/' + imgName,"name":f.filename})

# 下载合成成功的视频
@app.route("/download.mp3",methods=['GET'])
def download_mp3():
	# 服务器上文件的位置
	vf = 'static/yinyue/result.mp3'
	# 高级特性 生成器
	def generate(video_file):
		f = open(video_file, 'rb')
		while True:
			chunk = f.read(512*1024)
			if not chunk:
				break
			yield chunk
	return Response(
		stream_with_context(generate(vf)),
		# 控制浏览器怎么识别下载的东西
		# mimetype='video/mp4', # 让浏览器用mp4播放
		mimetype='application/octet-stream', # 让浏览器直接下载
		headers={"Content-Length": os.path.getsize(vf)})



@app.route("/")
def ladmin():
	return render_template('shouye.html')

@app.route("/<name>")
def hello(name):
	return render_template('%s' %name)


if __name__ == '__main__':
	# 绑定的地址0.0.0.0，表示任意ip都能访问
	app.run(host='0.0.0.0', port=8012,debug="True")

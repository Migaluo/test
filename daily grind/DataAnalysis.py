#! /usr/bin/python3

'''任务文件分析工具  v1.0'''
'''update in 20180315'''
import sqlite3,os,struct,datetime,sys

DB_PATH = './db/'
DB_NAME = 'DA.db'

TABLE_DI = 'T_DI_Info'
TABLE_TASK = 'T_Task_Info'
TABLE_TASK_DI = 'T_Task_DI_'
TABLE_TASK_DATA = 'T_Task_Data_'

TK_FILE_PATH = './t/'

#待分析任务号列表  中间用','隔开
FileList = {int(sys.argv[3])}

UNIT = {
        2:'m',
        3:'h',
        4:'d',
        5:'M'
        }

TASK_INFO = {
			'TNo':0,
			'Size':0,
			'Int':0,
			'Int_unit':'',
			'LTime':''
			}

try:
	LOG_NO_RECORD = int(sys.argv[1])    #第一个传入的参数代表是否要打印无效记录
	LOG_ERR_RECORD = int(sys.argv[2])   #第二个传入的参数代表是否要打印无效记录
except:
	print("Para Error!  ex. DataAnalysis.py -IsLogNoRecord -IsLogErrorRecord  (1-Yes  0-No)")     #验证参数有效性
	exit()

#sql语句执行
def _sqlshell(cur,buffer,bLog):
	if sqlite3.complete_statement(buffer):
		try:
			buffer = buffer.strip()   # 去除首尾空格
			if bLog:
				print("sql:%s"%buffer)
			cur.execute(buffer)
			if bLog:
				print("execute!")
		except sqlite3.Error as e:
			print("An error occurred:", e.args[0])
			return False
	else:
		print("complete_statement buffer error!")
		return False
	return True


#检查数据库 （判断数据库是否存在）
def _checkdb():
	if os.path.exists(DB_PATH+DB_NAME):
		return True
	else:
		print("%s is not exists!"%(DB_PATH+DB_NAME))
		return False

#检查表单	（检查表单是否存在）
def _checktable(cur,table_name):
	print("checktable->\"%s\""%table_name)
	if _sqlshell(cur,"select * from %s;"%table_name,False):
		if not cur.fetchall():
			print("Table:\"%s\" Error!"%table_name)
			return False
		else:
			for c in cur.fetchall():
				print(c)
			return True
	else:
		return False

#数字转字符串（%02d）
def _dec2Str(dec):
	if dec > 99:
		dec = 0
		print("dec pass 99 (%s)"%dec)
	return "{:0>2}".format(str(dec))
	

#（删除）创建新的数据表单 此表单存储分析结果
def _CreateDataTable(cur,TNo):
	TaskData = TABLE_TASK_DATA+_dec2Str(TNo)
	TaskDI = TABLE_TASK_DI+_dec2Str(TNo)
	if not _sqlshell(cur,"Drop Table %s;"%TaskData,False):    #删除原有表单
		print("Drop Table %s Error!"%TaskData)
#		return False
	if not _sqlshell(cur,"select * from %s;"%TaskDI,False):
		print("select * from %s Error"%TaskDI)
		return False
	DI = cur.fetchall()
	str_DI = ""
	for d in DI:
		str_DI += ",[%s] varchar(20)"%d
	if not _sqlshell(cur,"create Table %s(Time varchar(20),MP int(3)%s);"%(TaskData,str_DI),False):    #根据任务配置信息建立新的表单
		print("create Table %s %s Error!"%TaskData)
		return False
	return True

#导入任务文件，分析任务属性
def _loadTFileInfo(TNo):
	FileName = TK_FILE_PATH+_dec2Str(TNo)
	if not os.path.exists(FileName):
		print("TaskFile \"%s\"is not exists"%FileName)
		return False
	with open(FileName,'rb') as f:
		print("Load T File %d"%TNo)
		TASK_INFO['TNo']=TNo
		print("Task Max Record Num:%d"%struct.unpack('h',f.read(2)))
		print("Task Last Record:%d"%struct.unpack('h',f.read(2)))
		s = f.read(6)[::-1]
		s = "%02X-%02X-%02X %02X:%02X:%02X"%(s[0],s[1],s[2],s[3],s[4],s[5])
		print("Task Last Record Time:%s"%s)
		TASK_INFO['LTime'] = s
		Size = struct.unpack('h',f.read(2))
		print("Task one record size:%d Byte"%Size[0])
		TASK_INFO['Size']=Size[0]
		print("Task File is Full: %s"%struct.unpack('?',f.read(1))[0])
		unit = UNIT[struct.unpack('b',f.read(1))[0]]
		inter = struct.unpack('b',f.read(1))[0]
		print("Task interval: %d%s"%(inter,unit))
		TASK_INFO['Int'] = inter
		TASK_INFO['Int_unit'] = unit
		s = f.read(6)[::-1]
		s = "%02X-%02X-%02X %02X:%02X:%02X"%(s[0],s[1],s[2],s[3],s[4],s[5])
		print("Task Last Upload Time:%s"%s)
		s = f.read(11) #11个字节的预留信息
	return True

#插入
def _insert(original, new, pos):
	return original[:pos] + new + original[pos:]

#根据时间间隔得到下一时刻
def _timedelta(Int,Unit):
	if Unit == 'h':
		return datetime.timedelta(hours=Int)
	if Unit == 'm':
		return datetime.timedelta(minutes=Int)
	if Unit == 'd':
		return datetime.timedelta(days=Int)
	else:
		return 0

#任务文件分析
def _loadTFileData(cur,TNo):
	try:
		FileName = TK_FILE_PATH+_dec2Str(TNo)
		TaskDI = TABLE_TASK_DI+_dec2Str(TNo)
		TaskData = TABLE_TASK_DATA+_dec2Str(TNo)

		if TASK_INFO['TNo'] != TNo:
			print("TASK_INFO Error!")
			return False
		print("Load Task File:%d"%TNo)
		if not _CreateDataTable(cur,TNo):
			print("CreateDataTable:%d Error!"%TNo)
			return False
		if _sqlshell(cur,"select MP_S,MP_E from %s where TaskNo=%d;"%(TABLE_TASK,TNo),False):
			MP_S,MP_E = cur.fetchone()   #起始测量点  结束测量点
			print(MP_S,MP_E)
		else:
			print("No Info of Task:%d"%TNo)
			return False

		with open(FileName,'rb') as f:
			f.seek(32) #任务文件头信息TFileInfo
			nTime = 0
			LTime = datetime.datetime.strptime('20'+TASK_INFO['LTime'], "%Y-%m-%d %H:%M:%S")		
			while True:
				try:
					sf = f.read(6)[::-1]
					if not sf:
						break  #文件结尾
				except:
					break
				rTime = "%02X-%02X-%02X %02X:%02X:%02X"%(sf[0],sf[1],sf[2],sf[3],sf[4],sf[5])
				dTime = datetime.datetime.strptime('20'+rTime, "%Y-%m-%d %H:%M:%S")
				if nTime:
					while dTime > nTime:   #查找无记录的条目
						str_nTime = nTime.strftime("%Y-%m-%d %H:%M:%S")
						if LOG_NO_RECORD:
							print("No Record -->%s"%str_nTime[2:])
						_sqlshell(cur,"insert into %s(Time) values(\'%s\');"%(TaskData,str_nTime[2:]),False)   #无记录点的时间写入
						nTime = nTime + _timedelta(TASK_INFO['Int'],TASK_INFO['Int_unit'])
						if nTime == LTime:
							print("Last Record!")
							break
					if dTime < nTime:
						print('Time Error!')
						return
				for MP in range(MP_E-MP_S+1):
					ErrorFlag = False
					if _sqlshell(cur,"select * from %s;"%TaskDI,False):
						str_data = ""
						for c in cur.fetchall():
							if _sqlshell(cur,"select size,format,unit from %s where id=\'%s\';"%(TABLE_DI,c[0]),False):
								rSize,rFormat,rUnit = cur.fetchone()
								index = rFormat.find('.')   #格式调整为上行通讯规约格式
								rData = f.read(rSize)[::-1]
								#print(rData)
								s = ""
								for x in rData:
									s+="%02X"%x
									if s == 'FFFF' or s == 'EEEE':
										ErrorFlag = True
								if index != -1:
									s = _insert(s,'.',index)
								if s[0] == '0' and index != 1:
									s = s[1:]
								s += rUnit
								s = ','+'\''+s+'\''
								str_data+=s
							else:
								print("select size,format,unit from %s where id=\'%s\'; Error"%(TABLE_DI,c[0]))
								return False
					else:
						print("select * from %s; Error!"%TaskDI)
						return False
					if ErrorFlag == True and LOG_ERR_RECORD == 1:
						print("Error Record (FF|EE),MP:%d-->%s"%(MP+MP_S,dTime))
					nTime = dTime +  _timedelta(TASK_INFO['Int'],TASK_INFO['Int_unit'])
					_sqlshell(cur,"insert into %s values(\'%s\',%d%s);"%(TaskData,rTime,MP+MP_S,str_data),False)   #记录写入数据库
	except:
		print("loadTFileData Error!")
		return False
	return True

#导入任务冻结文件
def _loadTFile(cur,TNo):
	if not _loadTFileInfo(TNo):
		return False
	if not _loadTFileData(cur,TNo):
		return False
	return True

#关闭数据库
def _closeDB(cur,conn):
		cur.close()
		conn.commit()
		conn.close()


#主函数入口
if __name__ == '__main__':
	table_Flag = True
	if False == _checkdb():
		exit()
	try:
		conn = sqlite3.connect(DB_PATH+DB_NAME)
		cur = conn.cursor()
		
		if not _checktable(cur,TABLE_DI) or not _checktable(cur,TABLE_TASK):
			_closeDB(cur,conn)
			exit()

		for f in FileList:
			if not _checktable(cur,(TABLE_TASK_DI+_dec2Str(f))):
				print("checktable error %d"%f)
				continue
			if not _loadTFile(cur,f):
				print("loadTFile error %d"%f)
				continue

		_closeDB(cur,conn)

	except:
		print("Error!")


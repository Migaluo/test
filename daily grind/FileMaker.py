#! /usr/bin/python3
import os
import shutil
import struct
import sys

#CRC校验函数
def crc16(f):
	a = 0xFFFF
	b = 0xA001
	for byte in f:
		a ^= byte
		for i in range(8):
			last = a % 2
			a >>= 1
			if last == 1:
				a ^= b
	return a


print("### Make Download File by Python3 V1.0 ###")
print("### File+Shell+FactoryInfo ###")


FilePath = os.getcwd()   # 得到当前地址

try:
	HardVersion = sys.argv[1]   # 返回argv第一个参数
	FileName = FilePath+"/"+sys.argv[2]
	ShellFileName = FilePath+"/"+sys.argv[3]
except:
	print("Para Error!  ex. FileMaker.py -HardVersion -FileName")     #验证参数有效性
	exit()

NewFileName = FileName+".d"    #命名新文件名  *.d

if os.path.isfile(FileName) == False:
	print("File \"%s\" is not exists!" %FileName)     #判断源文件是否存在
	print("Exit now")
	exit()

print("Input File <-\"%s\" "%FileName)

if os.path.isfile(ShellFileName) == False:
	print("File \"%s\" is not exists!" %ShellFileName)   #判断脚本文件是否存在
	print("Exit now")
	exit()
print("Add Shell <-\"%s\" "%ShellFileName)
print("HardVersion <-%s"%HardVersion)

FileSize = os.path.getsize(FileName)      #记录源文件大小/脚本首地址

Mod = 16 - (FileSize % 16)                #文件补齐用

print("Download File Making....")

shutil.copyfile(FileName,NewFileName)     #创建新文件
with open(NewFileName,'ab') as f:
	for i in range(Mod):
		f.write(struct.pack('b',0x00))    #在新文件末尾，用0x00补齐，使得脚本首地址对齐到0h

with open(ShellFileName,'r') as sf:
	print("Shell Loading...")
	for line in sf:		
		line = line.strip('\n')		
		with open(NewFileName,'a') as f:
			f.write(line)	                 #将脚本逐行写入文件末尾
		with open(NewFileName,'ab') as f:	 #以二进制格式打开一个文件用于追加,接已有文件之后，不存在则新建文件
			f.write(struct.pack('i',0x00))   #换行用四个字节的0x00取代

with open(NewFileName,'ab') as f:
	f.write(struct.pack('i',(FileSize+Mod)))  #写入脚本首地址

NewFileSize = os.path.getsize(NewFileName)    #得到新文件大小/工厂信息首地址


print("CRC Calculating...10s")
with open(NewFileName,'rb') as f:
	crc = crc16(f.read())                     #对新文件做CRC校验

print("Factory Info Loading...")
with open(NewFileName,'a') as f:
	f.write("creaway")                        #增加creaway

with open(NewFileName,'ab') as f:
	for i in range(13):
		f.write(struct.pack('b',0x00))        #软件版本字段暂时用0x00填写

	f.write(struct.pack('H',int(HardVersion,16)))   #硬件版本
	f.write(struct.pack('i',NewFileSize))     #工厂信息首地址/文件大小
	f.write(struct.pack('H',crc))             #CRC校验
	for i in range(36):
		f.write(struct.pack('b',0x00))        #保留字段

NewFileSize = os.path.getsize(NewFileName)    #获取新文件大小


print("File Maked succeeful!")
print("Output CRC->%02X"%crc)
print("Output File ->%s"%NewFileName)
print("Input File Size:%d Byte" %FileSize)
print("Output File Size:%d Byte" %NewFileSize)




	



			
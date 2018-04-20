#! /usr/bin/python3

import struct 
TERMAL_TEMP = "/sys/devices/virtual/thermal/thermal_zone0/temp"

#插入
def _insert(original, new, pos):
	return original[:pos] + new + original[pos:]

#获取终端温度
def _getTerTemp():
	with open(TERMAL_TEMP,'r') as f:
		temp = f.read()

	s_Temp = str(temp)
	s_Temp = _insert(s_Temp,'.',2)
	temp = float(s_Temp)
	return temp

#print(_getTerTemp())

import time

since_time = time.time() # 最原始监测时间
def monitor():         # 监测函数

    global since_time       # 函数内部使用since_time                 
    day = 1
    while True:
        start_time = time.time()    # 记录开始时间
        while True:
            now_time = time.time()

            if now_time -start_time>= 300:                  # 判断是否超过五分钟

                if now_time - since_time >= 86400:        # 判断是否超过24个小时  
                    day += 1                              
                    since_time += 86400
                with open("record%d" % day , "a") as f:
                    f.write(str(time.strftime("%Y/%m/%d--%H:%M:%S   ")))
                    f.write(str(_getTerTemp()) + "\n")
                    print("record successful!")
                break
if __name__ == '__main__':
    monitor()

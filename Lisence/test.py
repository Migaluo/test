#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
根据某一天来推前几天或者未来几天的时间 比如需要知道从2014-10-25以来的10天的数据 
需要进行时间上的运算，如果按照本质，就是时间戳和时间之间的转换
通过时间转时间戳 获取2014-10-25的时间戳，然后进行时间戳上的运算，
再将运算的结果转成时间字符串
"""

import time,datetime    # 计算给定日期的10天后时间戳
t = datetime.datetime(2014, 10, 25)
timestamp = time.mktime(t.timetuple())
timestamp += 10 * 3600 * 24
t = time.localtime(timestamp)
timeStr = time.strftime('%Y-%m-%d %H:%M:%S', t)
print(timeStr)

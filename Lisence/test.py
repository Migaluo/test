#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time,datetime    # 计算给定日期的10天后时间戳
t = datetime.datetime(2014, 10, 25)
timestamp = time.mktime(t.timetuple())
timestamp += 10 * 3600 * 24
t = time.localtime(timestamp)
timeStr = time.strftime('%Y-%m-%d %H:%M:%S', t)
print(timeStr)

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time           # 计算某天是当年第几天
try:

   date = input('请输入日期：')
   t = time.strptime(date, '%Y-%m-%d')
   print(time.strftime('%j',t))
except:
    print('输入的格式错误，请重新输入!')
    exit()
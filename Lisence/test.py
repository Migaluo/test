#！/user/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import os

pwd = os.path.abspath('.')   # 返回绝对路径(如果改成path = '.',打印相对路径)

print('    size    last modified name')
print('------------------------------------------------')

for f in os.listdir(pwd):
    fsize = os.path.getsize(f)
    mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M')  # 获取文件的修改时间，返回时间戳，
                                                                          # 因此需要用到Python内置的datetime模块来处理

    flag = '/' if os.path.isdir(f) else ''    # 判断是否子目录，同理os.path.isfile(filename)判断是否是文件

    print('%10d %s %s%s' %(fsize,mtime,f,flag))   # 如果想要获取一个子文件的扩展名，则用os.path.splitext(filename)，

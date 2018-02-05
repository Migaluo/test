import os
from datetime import datetime
p = os.path.abspath('.')

for f in os.listdir(p):#返回指定文件夹包含的文件或文件夹名字，以字母排序的列表显示。os.listdir(path)
    fsize = os.path.getsize(f)
    mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime('%y-%m-%d %h:%m')

flag = '/' if os.path.isdir(f) else'' # 判断是否子目录，同理os.path.isfile(filename)判断是否是文件

print('%10d %s %s%s'%(fsize,mtime,f,flag))



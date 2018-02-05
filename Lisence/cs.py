import os
from datetime import datetime
p = os.path.abspath('.')

for f in os.listdir(p):
    fsize = os.path.getsize(f)
    mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime('%y-%m-%d %h:%m')

flag = '/' if os.path.isdir(f) else''

print('%10d %s %s%s'%(fsize,mtime,f,flag))



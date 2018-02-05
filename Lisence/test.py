from io import StringIO

f = StringIO()

f.write('Hello')

print(f.tell())

f.seek(2)    # 0表示从当前位置计算指针的偏移 1，结果5 ello,2结果5 llo

s = f.readline()

print(s)
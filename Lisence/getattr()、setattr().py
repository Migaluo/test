from Day_02 import MyObject

computer = MyObject()
def run(x):
    inp = input('method>')

    if hasattr(computer,inp):            # 判断是否有这个属性
       func = getattr(computer,inp)   # 有就获取，然后赋值给新的变量
       print(func())
    else:
        setattr(computer,inp,lambda x:x+1)      # 没有我们来set一个
        func = getattr(computer,inp)
        print(func(x))

if __name__ == '__main__':
    run(10)


# 首先你有一个command.py文件，内容如下(加减乘除)这里假设它后面还有100个方法
#   是Day_02.py  是import的另一个程序
class MyObject(object):
    def __init__(self):
        self.x = 9
    def add(self):
        return self.x + self.x

    def pow(self):
        return self.x * self.x

    def sub(self):
        return self.x - self.x

    def div(self):
        return self.x / self.x



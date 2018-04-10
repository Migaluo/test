class Book(object):    # 定义一个Book类
    kind = 'math'      # 给类创建属性变量kind,内容是book
    def __init__(self,name): # 双下划线是特殊方法，创建实例时绑定实例的属性name（实例的属性）
        self.name = name     # 有了_init__必须传入与方法匹配的参数（self本身不用传

s = Book('English')    # 是(book类的)实例s的属性

print(s.name)         # 打印实例的属性   E
print(Book.kind)      # 打印math 是book类的属性  m
Book.price = 20       # book类另一个price属性  20
print(Book.price)     # 打印类属性

# 测试对象类型信息
print(hasattr(Book,'name'))    # hasattr判断Book是否有name属性 F(类不具备实例属性)
if(hasattr(s,'price')):
    print(getattr(s,'price'))  # getattr获取实例s的price值   20

  #  math = Book()      # math是book的一个实例
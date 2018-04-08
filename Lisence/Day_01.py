#! /usr/bin/python2
# -*- coding: UTF8 -*-

class Student(object):
    def __init__(self,name,gender):
        self.name = name
        self.__gender = gender

    def get__gender(self):
        return self.__gender

    def set__gender(self,gender):
        if gender.__str__() =='male' or gender.__str__ () =='female':
            self.__gender = gender
        else:
            raise ValueError('性别错误')            # 一个基础类

if __name__ == '__main__':
    # 测试：
   bart = Student('Bart','male')
   if bart.get__gender() != 'male':
       print('测试失败！')
   else:
       bart.set__gender('female')
       if bart.get__gender() != 'female':
           print('测试失败！')
       else:
           try:
               bart.set__gender('男女')
               print('测试失败')
           except ValueError:
                print('测试成功')




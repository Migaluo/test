#!/usr/bin/env Python3
# -*- encoding:UTF-8 -*-
# 练习：为了统计学生人数，给Student类增加一个类属性
# 每创建一个实例，该属性自动增加

class Student(object):
    count = 0                #  类属性
    def __init__(self,name):  # 实例的属性
        self.name = name     #  与上句同时使用
        Student.count = Student.count+1
        print(Student.count)



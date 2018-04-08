#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3   #导入驱动

conn = sqlite3.connect('test.db')   # 连接数据库 不存在则自动创建
cursor = conn.cursor()       # 创建游标
# 创建user表
cursor.execute("CREATE TABLE use (id VARCHAR(10) PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO user(id,name) VALUES (1,'Creaway')")   # 添加一条记录
# 获取插入行数
print(cursor.rowcount)

# 查询
# cursor.execute('select *from user')
# 获取查询结果
# values = cursor.fetchall()
# print(values)  # [('1','Creaway')]


# 关闭游标
cursor.close()
# 提交事务
conn.commit()
# 关闭连接
conn.close()
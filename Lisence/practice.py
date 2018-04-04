from test import Student

Stu_L = []
while True:
    name = input('输入名字：\n>')
    score = int (input('输入成绩：\n>'))
    Stu_L.append(Student(name,score))
    request = input('需要继续吗？(Y/N) \n>')
    if request == 'y' or request =='Y':
        continue

    else:
        print('名字和成绩如下：')
        for i in Stu_L:
             print('姓名：%s 成绩：%d 评价：%s'%(i.name,i.score,i.return_grand()))
        break

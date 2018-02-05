import os   #不知何意
def find_file(name,path = os.path.abspath('.')): #如果改成path = '.',打印相对路径
    for f in os.listdir(path):
        fpath = os.path.join(path,f)
        if os.path.isfile(fpath) and name in os.path.splitext(f)[0]:
            print(path)
            print(f)
        elif os.path.isdir(fpath):
            find_file(name,fpath)

find_file('shan')

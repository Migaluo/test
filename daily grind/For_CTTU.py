#!/usr/bin/python3

import socket,threading,time,datetime,select

lt_socket = []   #socket
lt_port = []     #port
lt_time_wait = [10,60,10,10,10]   #等待时间

addr_local = '127.0.0.1'   #localhost

Max_Socket_Num = 5    #可监听数
Define_Port = 6000    #监听端口  6000开始

#socket 初始化
for i in range(Max_Socket_Num):
    s_Tmp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    lt_socket.append(s_Tmp)
    lt_port.append(Define_Port + i)
    lt_socket[i].bind((addr_local,lt_port[i]))
    print('socket_%s ip:%s,port:%s'%(i,addr_local,lt_port[i]))
    print('socket time wait is %ss'%lt_time_wait[i])


#写文件函数
def writefile(buf,no):
    with open('/cw/o/%s'%(Define_Port+no),'a') as f:        #目录根据实际情况填写
        f.write(time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime()))
        f.write(buf+'\n\n')


#主应用
def tcplink(sock,no):
    sock.listen(1)   #监听
    print('listen port %s'%(Define_Port+no))
    try:
        s, add = sock.accept()   #接受
    except :
        print('accept Error %s'%no)
        s.close()
        return
    print('accept port %s'%(Define_Port+no))
    writefile('accept,Wait %ss' % lt_time_wait[no], no)
    #oldtime = datetime.datetime.now()
    s.setblocking(0)    #非阻塞   默认的recv()是阻塞的   无法做超时判断

    while True:
        try:
            ready = select.select([s], [], [], lt_time_wait[no])    #如果无数据情况超过lt_time_wait秒以后或者有数据
            if ready[0]:
                date = s.recv(256)  #接收数据
            else:
                writefile('No Recv Date in %ss'%lt_time_wait[no], no)   #无数据的情况
                continue
            if not date:   #Client断开连接
                s.close()
                print('socket close %s'%(Define_Port+no))
                writefile('Link cut by client', no)
                s, add = sock.accept()    #重新等待Client
                print('accept port-2 %s' % (Define_Port + no))
                continue
            else:
                #newtime = datetime.datetime.now()
                #second = (newtime-oldtime).seconds
                #if second > 10:
                    #writefile('second is %s' %second, no)
                #oldtime = newtime
                pass
        except :
            print('recv Error %s'%no)   #其他错误
            s.close()
            return
    return


#根据不同的socket 创建线程
for i in range(Max_Socket_Num):
    t = threading.Thread(target=tcplink, args=(lt_socket[i],i))
    t.start()

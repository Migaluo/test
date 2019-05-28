# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import struct, socket, ftplib
import time, os
from binascii import hexlify, unhexlify
import random,paramiko

try:               # 捕捉导入ui模块出错引发的异常
    from Ui_Main import Ui_MainWindow
except ImportError as e:
    print("--1 --", e)
    try:
        from .Ui_Main import Ui_MainWindow
    except ImportError as e:
        print("--2 --", e)

_XFER_FILE = 'FILE' #定义sftp文件和文件夹变量
_XFER_DIR  = 'DIR'
class _Signal(QObject):  #udp收发时 错误消息发送信号
    error_signal = pyqtSignal(int)
Signal = _Signal()

class ClientThread(QThread):
    recvData_signal = pyqtSignal(object) #自定义接收信号

    # 实际终端修改ip 
    def __init__(self,
                 ip_server="127.0.0.1",
                 port_server=2222,
                 ip_slave="127.0.0.1",
                 port_slave=2345,
                 parent=None):
        super().__init__(parent)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((ip_slave, port_slave))
        self.sendAddr = (ip_server, port_server)
        self.ipInfo = {
            "ip_server" : ip_server,
            "ort_server": port_server,
            "ip_slave"  : ip_slave,
            "port_slave": port_slave,
        }

    def run(self):
        while True:
            try:
                recvData, addr = self.server.recvfrom(9999)

                # 接收到返回的数据，此处解析报文 emit 出去、
                
                self.recvData_signal.emit(recvData)
            except ConnectionResetError as e:
                Signal.error_signal.emit(e.__int__())
                continue

    def sendMsg(self, msg, sendToaddr=None, ): # 发消息
        if sendToaddr is None:
            sendToaddr = self.sendAddr
        if isinstance(msg, int):   # 发送转换成字符型
            msg = msg.encode('utf-8')
        if isinstance(msg, bytes): 
            self.server.sendto(msg, sendToaddr)

    def getIPinfo(self):
        return self.ipInfo  # 获得ip和端口的列表

    def closeSocket(self): 
        self.server.shutdown(2)
        self.server.close() # 关闭udp的服务器端连接
        sys.exit(0)

    def closessh(self): 
        self.ssh.close() # 关闭远程的ssh连接
        self.sftp.close()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)       
        self.stateMsg = self.statusBar() # 如果远程没开机 , 发送错误消息
        Signal.error_signal.connect(lambda info: self.stateMsg.showMessage(info, 1500))
        # 实例化 启动线程
        self.socketThread = ClientThread(parent=self) #self.socketThread = ClientThread('192.168.137.253', 2222,'172.30.57.98', 2345,parent=self)
        self.socketThread.recvData_signal.connect(lambda recvData: self.textEdit_query.append(repr(recvData)))
        self.socketThread.start()

        self.transport = paramiko.Transport(('172.30.67.172', 22)) # self.transport = paramiko.Transport(('192.168.137.253', 22))
        self.transport.connect(username='root', password='cw123') 
        self.ssh = paramiko.SSHClient() # 创建SSH对象#将sshclient的对象的transport指定为以上的transport
        self.ssh._transport = self.transport

     #   stdin, stdout, stderr = self.ssh.exec_command('cd /tmp') # 首先进入程序包目录


        self.btnquery.clicked.connect(self.on_query_btn_clicked)
        self.btnUpload.clicked.connect(self.sftp_put_file) #导入文件到远程只能是指定的文件路径
        self.btnDownload.clicked.connect(self.sftp_get_file)  # 只能下载指定目录的指定单一文件/后续用btn选择下载log
        self.startup()  # sftp开启   后续关闭
        self.queryIP_clicked() 
        self.dockerStats_clicked() 
        self.psa_clicked()
       # self.psa1_clicked() # 查看线程状态
        self.reboot_clicked()
        self.time_clicked()
        self.time1_clicked()
        self.ls_clicked()

    def queryIP_clicked(self):
        self.btnIP.clicked.connect(self.queryIP)
    def queryIP(self): 
        stdin, stdout, stderr = self.ssh.exec_command('ifconfig')  # 执行命令
        res,err = stdout.read(),stderr.read() # 获取命令结果
        self.result = res if res else err
        self.textBrowser_cmd.append(self.result.decode())
    
    def dockerStats_clicked(self):
        self.btn_dockerStats.clicked.connect(self.dockerStats)
    def dockerStats(self):
        stdin, stdout, stderr = self.ssh.exec_command('docker ps') 
        res,err = stdout.read(),stderr.read() 
        self.result = res if res else err
        self.textBrowser_cmd.append(self.result.decode())

    def psa_clicked(self):
        self.btnPsa.clicked.connect(self.psa)
    def psa(self):                                      # 加入环境变量
      #  stdin,stdout,stderr = self.ssh.exec_command("source ~/etc/profile;echo $PATH;psa")
        stdin, stdout, stderr = self.ssh.exec_command("echo $PATH")
       # stdin, stdout, stderr = ssh.exec_command('psa')
        res,err = stdout.read(),stderr.read() 
        self.result = res if res else err
        print(self.result.decode())
        self.textBrowser_cmd.append(self.result.decode())
    """
    def psa1_clicked(self):
        self.btnPsa1.clicked.connect(self.psa1)
    def psa1(self):
        stdin, stdout, stderr = self.ssh.exec_command('nsenter -t 947 -n netstat -antp') 
        res,err = stdout.read(),stderr.read() 
        self.result = res if res else err
        self.textBrowser_cmd.append(self.result.decode())
    """
    def reboot_clicked(self):
        self.btnReboot.clicked.connect(self.reboot)
    def reboot(self):
        stdin, stdout, stderr = self.ssh.exec_command('reboot') 
        res,err = stdout.read(),stderr.read() 
        self.result = res if res else err
        self.textBrowser_cmd.append(self.result.decode())

    def time_clicked(self):  #终端对时
        self.btnTime.clicked.connect(self.adjustTime)
    def adjustTime(self):#stdin, stdout, stderr = self.ssh.exec_command('ntpdate 0.rhel.pool.ntp.org')
        stdin, stdout, stderr = self.ssh.exec_command('ntpdate asia.pool.ntp.org') 
        res,err = stdout.read(),stderr.read() 
        self.result = res if res else err
        self.textBrowser_cmd.append(self.result.decode())
    
    def time1_clicked(self):
        self.btnTime1.clicked.connect(self.adjustTime1)
    def adjustTime1(self):
        stdin, stdout, stderr = self.ssh.exec_command('hwclock')  # -w
        res,err = stdout.read(),stderr.read() 
        self.result = res if res else err
        self.textBrowser_cmd.append(self.result.decode())

    def ls_clicked(self):
        self.btnLs.clicked.connect(self.ls)
    def ls(self):
        stdin, stdout, stderr = self.ssh.exec_command('ls -l') 
        res,err = stdout.read(),stderr.read() 
        self.result = res if res else err
        self.textEdit_file.append(self.result.decode())

    def setUp(self):
        pass
       #stdin, stdout, stderr = self.ssh.exec_command('./deploy_sk.sh') #添加环境变量的文件

    

    def sftp_put_file(self):  # 本地文件传到远端
        source = r'C:/Users/luoji/PycharmProjects/creaway_3206_0523'
        target = r'/tmp/creaway_3206_0523' 
        replace = False   
        self.upload(source, target, replace)

    def solve_receData(self,data): # 处理接收到的数据显示在空白处

        """线程run 里面emit出来连接到此、"""

        print("远程终端返回的数据 ：", data)
        self.textEdit_query.append(repr(data)) #repr返回对象的string 格式 

    def open(self):  # open_file显示内容  不是单独建立的副线程
        filename, _ = QFileDialog.getOpenFileName(self)
        text = open(filename,'r', encoding='utf-8').read()
        self.textEdit_file.append(text)

    def get_send_msg(self): #从勾选框和下拉列表获取文字 组成发送消息

        listWidget = self.listWidget
        for row in range(listWidget.count()): # count为0-19
            item = listWidget.item(row) # 每个checkbox发不同命令 实际报文改变逻辑地址不同
            if self.listWidget.item(0).checkState() == Qt.Checked:        
                send_msg = "6817130701C10368010A00010000000000000000895B16"
            elif self.listWidget.item(1).checkState() == Qt.Checked:
                send_msg = "6817130701010468010A00010000000000000001899D16"
            elif self.listWidget.item(2).checkState() == Qt.Checked:
                send_msg = "6817130701410468010A0001000000000000000289DE16"
            elif self.listWidget.item(3).checkState() == Qt.Checked:
                send_msg = "6817130701810468010A00010000000000000006892216"                
        return send_msg
        print(item.text())

    @pyqtSlot()
    def on_query_btn_clicked(self): #查询按钮

        send_msg = self.get_send_msg()  # type:str
        self.socketThread.sendMsg(send_msg.encode('utf-8'))


    def closeEvent(self,e):
        self.socketThread.closeSocket() # 关闭事件包含关闭socket线程
       #self.socketThread.terminate()  # 关闭远端线程
        self.socketThread.closessh()

    def startup(self): # sftp开始
        try:
            transport = paramiko.Transport('172.30.67.172', 22)
            transport.connect(username='root', password='cw123')
            self.sftp = paramiko.SFTPClient.from_transport(transport)
            self.textEdit_file.append('已连接172.30.67.172...')
        except Exception as e:
            self.textEdit_file.append('error connection')
            print (u'连接失败：'+str(e))
 
    def upload(self, source, target, replace): # 处理上传
        source = source.replace('\\', '/')   # 来源路径   
        target = target.replace('\\', '/')  # 目标路径
        if not os.path.exists(source): # print (u'来源资源不存在，请检查：' + source)
            return   
        self.__makePath(target)    # 格式化目标路径
        filetype, filename = self.__filetype(source)
     
        if filetype == _XFER_DIR:    # 判断文件类型: 文件/目录
            self.uploadDir(source, target, replace)
        elif filetype == _XFER_FILE:
            self.uploadFile(source, filename, replace)


    # 传送目录
    def uploadDir(self, source, target, replace):
        if not os.path.isdir(source):        # 判断目录存在
            return      #print (u'这个函数是用来传送本地目录的')      
        for file in os.listdir(source):  # 遍历目录内容，上传资源
            filepath = os.path.join(source, file)      # 资源路径
            if os.path.isfile(filepath):  # 判断要上传的文件类型：文件/文件夹
                self.uploadFile(filepath, file, replace) 
            elif os.path.isdir(filepath):
                try:
                    self.sftp.chdir(file) 
                except:
                    self.sftp.mkdir(file)
                    self.sftp.chdir(file) 
                self.uploadDir(filepath, file, replace)
        self.sftp.chdir('..')          ### 重置数据 # 返回上一层目录

    def uploadFile(self, filepath, filename, replace):     # 传送文件
        if not os.path.isfile(filepath): # print (u'这个函数是用来传送单个文件的')
            return
        if not os.path.exists(filepath):  #print (u'err:本地文件不存在，检查一下'+filepath)
            return
        try:
            self.sftp.put(filepath, filename)
            print (u'[+] 上传成功:' + filepath + ' -> ' + self.sftp.getcwd() + '/' + filename)
            self.textEdit_file.append(filename)
        except Exception as e:
            print (u'[+] 上传失败:' + filepath + ' because ' + str(e))
   
    def __filetype(self, source):  # 获得文件媒体数据({文件/目录, 文件名称})
        if os.path.isfile(source):
            index = source.rfind('/')
            return _XFER_FILE, source[index+1:]
        elif os.path.isdir(source):  
            return _XFER_DIR, '' 
    def __makePath(self, target):   # 目标路径不存在则依次创建路径目录       
        self.sftp.chdir('/')  # 切换根目录
        data = target.split('/') # 分割目标目录为目录单元集合
        for item in data:         # 进入目标目录, 目录不存在则创建
            try:
                self.sftp.chdir(item) 
                print (u'要上传的目录已经存在，选择性进入合并：' + item)
            except:
                self.sftp.mkdir(item)
                self.sftp.chdir(item) 
                print (u'要上传的目录不存在，创建目录：' + item) # 都可以显示到textEdit_file
   

    def sftp_get_file(self):
        local='C:/Users/luoji/PycharmProjects/logcom' #单一文件情况:目录最后名称就是文件的名字
        remote= '/cw/log/logcom'
        sf = paramiko.Transport('172.30.67.172',22)
        sf.connect(username = 'root',password = 'cw123')
        sftp = paramiko.SFTPClient.from_transport(sf)
        try:
            if os.path.isdir(local):     #判断本地参数是目录还是文件
                for f in sftp.listdir(remote):    #遍历远程目录
                    sftp.get(os.path.join(remote+f),os.path.join(local+f))#下载目录中文件
            else:
                sftp.get(remote,local)   
                self.textEdit_file.append('get logcom sucessful!')
        except Exception as e:    #下载单一的指定文件到指定目录
            sf.close()
 
    
if __name__ == "__main__":
    
    paramiko.util.log_to_file('paramiko.log')  # 记录ssh日志文件
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion")) # 界面风格设置
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

# coding=utf-8
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import struct
import socket
import time
import tool_ui
#from binascii import hexlify, unhexlify

class Main(QMainWindow):
   # def __init__(self):
    def __init__(self):
        super(Main, self).__init__()  
        self.ui = tool_ui.Ui_MainWindow()  
        self.ui.setupUi(self)
        self.ui.textBrowser_query=QTextBrowser()
        self.ui.textEdit_send = QTextEdit()
        self.ui.btnopen.clicked.connect(self.btn_open) 
        self.ui.btnsend.clicked.connect(self.udp_send) # UDP客户端发送
        self.address = ('172.30.57.98', 12345)
        self.client_start()
       # self.udp_recv()

    def client_start(self): # 启动客户端   
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def udp_send(self): # 发送消息至服务器

        send_msg = (str(self.ui.textEdit_send.toPlainText())).encode('utf-8') 
        self.udp_socket.sendto(send_msg, self.address)
    
    def udp_recv(self): # 接收数据  
        while True:
            recv_data=udp_socket.recvfrom(1024)#1024表示本次接收的最大字节

            #recv_data存储的是一个元组（发送方ip，Port）

            recv_msg=recv_data[0]

            send_addr=recv_data[1]

            #4、显示接收到的数据

            print("%s:%s"% (str(send_addr),recv_msg.decode("gbk")))
            udp_socket.close()      
       

    def udp_close(self): # 关闭连接
        try:
            self.udp_socket.close()
        except Exception as ret:
            pass     

    def btn_open(self): # 打开部署脚本  # 另一def函数,并且显示在textbrowser
        open_file, file_type = QFileDialog.getOpenFileName(self,'选择文件','')
        self.ui.textEdit_send.setText(open_file)

    class Thread(QThread):
        def run(self):
            pass
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UI = Main()
    UI.show()
    sys.exit(app.exec_())


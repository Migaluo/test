from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtNetwork import *
from PyQt5.QtNetwork import QHostAddress, QTcpServer, QTcpSocket
import PreviewApp
import sys, os
import qdarkstyle
#import SSHsore

CONTAINER, STATE = range(2)
class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()  # 初始化,super集成父类的属性
        self.ui = PreviewApp.Ui_MainWindow()  # 实例化
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('db/logo.jpg')) 
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('db/App.db')
        self.db.open()          
        
        self.tableView = self.ui.tableView  # 获取TableView对象
        self.tableView1 = self.ui.tableView1 

        self.model = QSqlTableModel(self) # 设置数据库模型
        self.model.setTable("Preview") # 选择db的其中一个表 
        self.tableView.setModel(self.model)  # 设置TableView的模型
        self.tableView.setEditTriggers(QTableView.NoEditTriggers) # 设置表1内容不可编辑
        self.model.select()
        # model1为页面2对象 
        self.model1 = QSqlTableModel(self) 
        self.model1.setTable("Container") 
        self.tableView1.setModel(self.model1) 
        self.model1.select()

        self.ui.btn1.clicked.connect(self.addRow)
        self.ui.btn2.clicked.connect(self.delRow)
        self.ui.btn3.clicked.connect(self.CPU)
        self.ui.btn4.clicked.connect(self.Memory)
        self.ui.btn5.clicked.connect(self.CPU_temp)
        self.ip_list = []
        self.tcpserver = TcpServer(self)
        self.tcpserver.listen(QHostAddress("0,0,0,0,"), Port)  # 绑定监听端口
        self.tcpserver.signRecv.connect(self.Recv) 
   #     self.tcpserver.signGetAddress.connect(self.updateCombox)
        self.updateCombox()

    def updateCombox(self):
        if self.db.open():
            print("open") # 打开了数据库
            query1 = QSqlQuery()
            query1.exec_("SELECT adress FROM IP") #打开查询数据库表
        for i in range(query1.size()):
            print(query1.value(0))
            self.ui.comboBox1.addItem(query1.value(0))  # 添加下拉列表框事件
            query1.next()

           
    def Recv(self, msg):
        reply = QMessageBox.information(self,
                                        "标题",
                                        msg,
                                        QMessageBox.Yes | QMessageBox.No)

    def Send(self, msg):  # 调用接口函数,向客户端发送消息
        print('发送信号发出')
        for id in self.tcpserver.socketList:
            self.tcpserver.signSend.emit(msg, id)

    def addRow(self):  # 添加一行
        row = self.model1.rowCount()
        self.model1.insertRow(row)
        index = self.model1.index(row, CONTAINER)
        self.tableView1.setCurrentIndex(index)
        self.tableView1.edit(index)

    def delRow(self):
        index = self.tableView1.currentIndex()
        if not index.isValid():
            return
        record = self.model1.record(index.row())
        container = record.value(CONTAINER)
        state = record.value(STATE)
        if (QMessageBox.question(self, "Container Data",  # 删容器时弹框
                                 ("Delete this record?"
                                         .format(state, container)),
                                 QMessageBox.Yes | QMessageBox.No) ==
                QMessageBox.No):
            return
        self.model1.removeRow(index.row())
        self.model1.submitAll()
        self.model1.select()

    def CPU(self):  # CPU占有率曲线
        self.ui.label2.setPixmap(QPixmap("db/CPU_percent.png"))

    def Memory(self):  # 内存曲线
        self.ui.label2.setPixmap(QPixmap("db/memory.jpg"))

    def CPU_temp(self):  # CPU温度
        self.ui.label2.setPixmap(QPixmap("db/CPU.jpg"))

Port = 6666
SIZEOF_UINT16 = 2
class TcpSocket(QTcpSocket):  # client收发功能
    signRecv = pyqtSignal(str)
    def __init__(self, socketId, parent=None):
        super(TcpSocket, self).__init__(parent)
        self.socketId = socketId  # 客户端每接入一个对应socketId
        self.readyRead.connect(self.Recv)  # 连接信号readyRead槽函数

    def Recv(self):  # 槽接收  
        print('receiving Message')
        while self.state() == QAbstractSocket.ConnectedState:  # 判断socket连接状态
            nextBlockSize = 0
            stream = QDataStream(self)  # QDataStream接收数据
            print('QDataStream is created')
            if self.bytesAvailable() >= SIZEOF_UINT16:  # 所有字节读完跳出循环
                nextBlockSize = stream.readUInt16()
            else:
                break
            if self.bytesAvailable() < nextBlockSize:
                break
            msg = ''
            msg = stream.readQString()
            try:
                clientAddress = self.peerAddress().toString()
                clientPort = str(self.peerPort())
            except :
                print("Exception")

            msg = '来自%s 端口为：%s的信息： %s'%(clientAddress, clientPort, msg)
        
            self.signRecv.emit(msg) 

    def Send(self, msg, id):  
        if id == int(self.socketId):
            reply = QByteArray()
            stream = QDataStream(reply, QIODevice.WriteOnly)
            stream.writeUInt16(0)
            stream.writeQString(msg)
            stream.device().seek(0)
            stream.writeUInt16(reply.size() - SIZEOF_UINT16)
            self.write(reply)

class Thread(QThread): 
    signRecv = pyqtSignal(str)
    signSend = pyqtSignal(str, int)
    signGetAddress = pyqtSignal(str)

    def __init__(self, socketId, parent):
        super(Thread, self).__init__(parent)  # 父线程
        self.socketId = socketId

    def run(self):  # run实现数据收发
        socket = TcpSocket(self.socketId)
        if not socket.setSocketDescriptor(self.socketId):  # 获取连接
            return
        socket.signRecv.connect(self.Recv)
        self.signSend.connect(socket.Send)

        clientAddress = socket.peerAddress().toString()
        self.signGetAddress.emit(clientAddress)

        self.exec_()  # 循环

    def Send(self, msg, id):
        if msg == '':  # action
            return
        self.signSend.emit(msg, id)
    def Recv(self, msg):  
        self.signRecv.emit(msg)

class TcpServer(QTcpServer):
    signRecv = pyqtSignal(str)  # 自定义信号
    signSend = pyqtSignal(str, int)
    socketList = []                    # List存放加入的socketId
    signGetAddress = pyqtSignal(str)  #自定义信号

    def __init__(self, parent=None):
        super(TcpServer, self).__init__(parent)

    def incomingConnection(self, socketId):
        if socketId not in self.socketList:  # 判断列表是否存在加入的客户端
            self.socketList.append(socketId) 
            thread = Thread(socketId, self)  # 创建线程
            thread.signRecv.connect(self.Recv)

            thread.signGetAddress.connect(self.signGetAddress)

            self.signSend.connect(thread.signSend)  # 后send改成signSend
            thread.finished.connect(thread.deleteLater)  # 删除线程
            thread.start()

    def Recv(self, msg):
        self.signRecv.emit(msg)
        for id in self.server.socketList:
            self.server.signSend.emit(action, msg, id)

    def showConnection(self):
        print(self.server.socketList)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    UI = Main()
    UI.show()
    sys.exit(app.exec_())
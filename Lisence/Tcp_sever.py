import socket   # tcp服务端


host = '127.1.0.0'
port = 4444


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()  # 生成新的连接


while True:
    data = conn.recv(1)
    print(data)
conn.close()
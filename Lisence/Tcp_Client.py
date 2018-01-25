import socket   # tcp协议客户端

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host='172.30.32.0'
port= 4444

sock.connect((host,port))

print (sock.recv(1024))
sock.close()



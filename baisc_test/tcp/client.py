import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',8888))
print('建立连接')
string = "hello"
s.send(string.encode())
data = s.recv(1024)
print("从服务端接受的消息：{0}".format(data.decode()))
s.close()
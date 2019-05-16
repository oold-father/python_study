import socket

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
addr = ('127.0.0.1',8888)

string = "hello"
s.sendto(string.encode(),addr)
data, _ = s.recvfrom(1024)
print("从服务端接受的消息：{0}".format(data.decode()))
s.close()
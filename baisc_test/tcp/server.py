import socket

#创建socket，制定IP地址类型和通信类型
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#绑定本机
s.bind(('',8888))

#监听端口
s.listen()
print('服务器端启动')

#等待访问
conn,addr = s.accept()

#客户端连接成功
print(addr)

#接受客户端数据
data = conn.recv(1024)
print("从客户端接受的消息：{0}".format(data.decode()))

#发送数据到客户端
string = '你好'
conn.send(string.encode())

#释放资源conn
conn.close()
s.close()
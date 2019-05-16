import socket

#创建socket，制定IP地址类型和通信类型
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#绑定本机
s.bind(('',8888))
print('服务器端启动')


#接受客户端数据
data,caddr= s.recvfrom(1024)
print("从客户端接受的消息：{0}".format(data.decode()))

#发送数据到客户端
string = '你好'
s.sendto(string.encode(),caddr)

s.close()
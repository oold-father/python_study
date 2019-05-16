import socket

HOST = '127.0.0.1'
PORT = 7777
addr = (HOST,PORT)
file_name = '1.png'
BUF_SIZE = 1024
with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
    with open(file_name,'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if str(data) != "b''":
                s.sendto(data,addr)
            else:
                s.sendto('end'.encode(),addr)
                break
    print('客户端上传完成')

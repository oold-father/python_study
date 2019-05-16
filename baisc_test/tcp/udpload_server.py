import socket

HOST = ''
PORT = 7777
BUF_SIZE = 1024
file_name = '1_udp.png'
with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
    s.bind((HOST,PORT))
    print("服务器启动............")
    with open(file_name,'wb') as f:
        buffer = []
        while True:
            data,addr = s.recvfrom(BUF_SIZE)
            
            if str(data) != "b'end'":
                buffer.append(data)
            else:
                break
        b = bytes().join(buffer)
        f.write(b)
    print('服务器接受完成')

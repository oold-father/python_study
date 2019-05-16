import socket

HOST = ''
PORT = 7777
file_name = 'hello_save.txt'
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:

    s.bind((HOST,PORT))
    s.listen(10)
    print("服务器启动............")

    while True:
        with s.accept()[0] as conn:
            buffer = []
            while True :
                data = conn.recv(1024)
                if data:
                    buffer.append(data)
                else:
                    break
            b = bytes().join(buffer)

            with open(file_name,'wb') as f:
                f.write(b)

            print('服务器接受完成')
            break

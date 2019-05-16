
from threading import Thread,Lock
import time

balance = 200

def draw():
    print("----------取钱开始----------")
    global balance
    mutex.acquire()
    temp = balance

    temp -= 100
    print("余额：",temp)
    time.sleep(2)
    balance = temp
    print("----------取钱结束----------")
    mutex.release()

def deposit():
    print("----------存钱开始----------")
    global balance
    mutex.acquire()
    temp = balance
    temp += 100
    print("余额：",temp)
    time.sleep(2)
    balance = temp
    print("----------存钱结束----------")
    mutex.release()

def main():
    print("主进程开始")
    print("当前存款：",balance)
    mutex = Lock()
    p1 = Thread(target=draw)
    p2 = Thread(target=deposit)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(balance)
    print("主进程结束")

if __name__ == "__main__":
    
    #main()
    print("主进程开始")
    print("当前存款：",balance)
    mutex = Lock()
    p1 = Thread(target=draw)
    p2 = Thread(target=deposit)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(balance)
    print("主进程结束")
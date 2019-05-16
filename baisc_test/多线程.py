#%%
from threading import Thread,Lock
import time

def test(i):
    print("-----------子线程"+str(i)+"开始----------")
    time.sleep(5)
    print("-----------子线程"+str(i)+"结束----------")

"""
if __name__ == "__main__":
    print("----------主进程开始----------")
    thread1 = Thread(target=test,args=(1,))
    thread2 = Thread(target=test,args=(2,))
    start = time.time()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    stop = time.time()
    print("----------主进程结束----------")
    print("cost time:",stop-start)
"""
#%%
balance = 200

#%%
def draw(mutex):
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

#%%
def deposit(mutex):
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

#%%
def main():
    print("主进程开始")
    print("当前存款：",balance)
    mutex = Lock()
    p1 = Thread(target=draw,args=(mutex,))
    p2 = Thread(target=deposit,args=(mutex,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(balance)
    print("主进程结束")

#%%
if __name__ == "__main__":
    
    main()
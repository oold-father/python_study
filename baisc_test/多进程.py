from multiprocessing import Process,Pool,Queue
import time
import os



def test(interval):
    print("我是子进程:{:d},执行任务:{:d}".format(os.getpid(),interval))
    #print("我是子进程:",name)
    #for i in range(interval):
    #    print(name,":",i)
    time.sleep(5)
    print("子进程结束",os.getpid())

"""
def main():
    print("我是主进程:",os.getpid())
    p = Pool(processes=3)
    #p1 = Process(target = test, args = (10,"test1"),name = "test1")
    #p2 = Process(target = test, args = (5,"test2"),name = "test2")
    #p1.start()
    #p2.start()

    #print("p.is_alive=",p.is_alive())
    #print("p.name=",p.name)
    #print("p.pid=",p.pid)
    for i in range(5):
        p.apply_async(func = test,args = {i,})

    print("等待子进程")
    p.close()
    p.join()
    #print("p.is_alive=",p.is_alive())

    print("主进程结束")

"""


def draw(q):
    print("----------取钱开始----------")
    if not q.empty():
        balance = q.get()
        balance -= 100
        q.put(balance)
        print("余额：",balance)
    print("----------取钱结束----------")

def deposit(q):
    print("----------取钱开始----------")
    if not q.empty():
        balance = q.get()
        balance += 100
        q.put(balance)
        print("余额：",balance)
    print("----------取钱结束----------")


def main():
    print("主进程开始")
    balance = 200
    print("当前存款：",balance)
    q = Queue(2)
    q.put(balance)
    p1 = Process(target=draw,args=(q,))
    p2 = Process(target=deposit,args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("主进程结束")


if __name__ == "__main__":
    main()
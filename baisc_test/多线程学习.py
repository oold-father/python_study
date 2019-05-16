
#%%
import  threading
import  time

# 子线程调用方法
def run(n):
    print("Run Start",n)
    time.sleep(1)
    print("Run done")

#创建子线程实例对象 
t1 = threading.Thread(target=run, args=("TZ",))

#启动线程,执行子线程任务
t1.start()


#%%
#创建自定义线程类
class MYThread(threading.Thread):
    def __init__(self,n):
        super(MYThread,self).__init__()
        self.n = n

    def run(self):
        print("runnint task : ",self.n)
        time.sleep(2)

#实例化类
t1 = MYThread("t1")
t2 = MYThread("t2")

#启动线程
t1.start()
#t1.join() #等待t1结束 进行t2  变成串行了
t2.start()


#%%
import  threading,time

#执行函数
def run(n):
    semaphore.acquire()
    time.sleep(1)
    print("run the thread : %s\n" %n)
    semaphore.release()

num = 0
#允许最多5个线程同时运行
semaphore = threading.BoundedSemaphore(5)

#循环创建20条线程
for i in range(20):
    t = threading.Thread(target=run,args=(i,))
    t.start()

while threading.active_count() != 1:
        pass
else:
    print('------all threads done---')


#%%
import  threading,time
import  queue
q = queue.Queue(maxsize=10)
#生产者模型
def Producer(name):
    count = 1
    while True:
        q.put("馒头%s" % count)
        print("%s生产了馒头 :%s" %(name,count))
        count += 1
        time.sleep(0.5)

#消费者模型
def Consumer(name):
    #while q.qsize() > 0:
    while True:
        print("%s 取到 %s 并且吃了它" %(name,q.get()))
        time.sleep(1)


p = threading.Thread(target=Producer,args=("TZ",))
C = threading.Thread(target=Consumer, args=("BAIBAI",))
C1 = threading.Thread(target=Consumer, args=("ZK",))

p.start()
C.start()
C1.start()


#%%
#!/usr/bin/python
#coding: utf-8
 
'''
队列的 task_done 方法
队列中的数据的使用者用来指示对于项目的处理已经结束。
如果使用此方法，那么从队列中删除的每一项都应该调用一次。
队列中的 join 方法
阻塞直到队列中的所有项目均被删除和处理为止。
一旦为队列中的每一项都调用了一次 task_done 方法，此方法将直接返回
'''
 
import queue
import threading
 
class WorkerQueue(threading.Thread):
 
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        # 创建队列
        self.input_queue = queue.Queue()
 
    def send(self, item):
        self.input_queue.put(item)
 
    def close(self):
        self.input_queue.put(None)
        # 阻塞知道队列中的所有项目均被删除和处理为止
        self.input_queue.join()
 
    def run(self):
        while True:
            item = self.input_queue.get()
            if item is None:
                break
 
            # 输出结果
            print (item)
            self.input_queue.task_done()
        
        # 完成，指示受到和返回了标志
        self.input_queue.task_done()
        return
 
w = WorkerQueue()
w.start()
w.send("Hello, ")
w.send("World")
w.close()


#%%
#!/usr/bin/python
#coding: utf-8
 
import queue
import threading
import time
 
# 队列为空的时候的标记
flag = 0
 
class Mythread(threading.Thread):
 
    def __init__(self, thread, que):
        threading.Thread.__init__(self)
        self.thread = thread
        self.que = que
 
    def run(self):
        print ("Starting " + self.thread)
        func(self.thread, self.que)
        print ("Exiting " + self.thread)
 
def func(name, que):
    # 如果说flag为0，则证明此时队列中还有数据
    while not flag:
        lock.acquire()
        try:
            # 从队列中删除一项，然后返回的是该项目的值
            # 设置删除等待的超时时间，防止产生阻塞
            data = que.get(timeout = 0)
            print("%s processing %s" % (name, data))
        except Exception as e: # 对抛出的异常不进行处理
            continue
        finally:
            lock.release()
            time.sleep(1)
 
threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
lock = threading.Lock()
# 创建一个队列，设置队列的大小
workQueue = queue.Queue(10)
threads = []
 
for _thread in threadList:
    thread = Mythread(_thread, workQueue)
    thread.start()
    threads.append(thread)
 
# 填充队列
# 填充队列的时候加锁，防止数据还没有插入完全就有该程序的其它地方运行，产生错误
lock.acquire()
for name in nameList:
    # 队列中输入数据
    workQueue.put(name)
lock.release()
 
# 如果队列不为空，则停留在此处，等待队列为空
while not workQueue.empty():
    pass
 
# 要退出了
flag = 1
 
# 等待所有的线程都运行完
for t in threads:
    t.join()
 
print("Exiting Main Thread")


#%%
import urllib.request
import urllib.error
import re
class BDTB:
    def __init__(self,baseUrl,seeLZ):
        self.baseUrl=baseUrl
        self.seeLZ='?see_lz='+str(seeLZ)
    def getPage(self,pageNum):
        try:
            url=self.baseUrl+self.seeLZ+'&pn'+str(pageNum)
            request=urllib.request.Request(url)
            reponse=urllib.request.urlopen(request)
            print(reponse.read())
            return reponse
        excepturllib.error.URLError,e:
            if hassttr(e,"reason"):
                print(u"连接百度贴吧失败，错误原因",e.reason)
        return None


#%%
import threading
import time


class Mythread(threading.Thread):
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print("开启线程:"+self.name)
        #获取锁用于线程同步
        threadLock.acquire()
        print(self.name + "加锁")
        print_time(self.name,self.counter,3)
        #释放锁，开启下一个线程
        threadLock.release()
        print(self.name + "解锁")



def print_time(threadName,delay,counter):
    while counter :
        time.sleep(delay)
        print("%s -- %s -- %s" %(threadName,delay,time.ctime(time.time())))
        counter -= 1

threadLock = threading.Lock()
threads = []

#创建新线程
thread1 = Mythread(1,"Thread-1",1)
thread2 = Mythread(2,"Thread-2",2)

#开启新线程
thread1.start()
thread2.start()

#添加新线程到线程列表
threads.append(thread1)
threads.append(thread2)

#等待所有线程完成
for t in threads:
    t.join()
print("退出主线程")


#%%
import threading
import time

def listen():
    print('begin to  listen')
    time.sleep(5)
    print('end listening')

def play():
    print('begin to play')
    time.sleep(4)
    print('end playing')

t1=threading.Thread(target=listen)
t2=threading.Thread(target=play)
start_time=time.time()

#法1 并发
t1.start()
t2.start()
t1.join()
t2.join()
#2顺序
#t1.start()
#t1.join()
#t2.start()
#t2.join()

end_time=time.time()
duration=end_time-start_time
print('duration:',duration)#并发5.001286268234253#顺序9.001514673233032


#%%
import threading,time

lst=[1,2,3,4,5]
def f():
    while lst:
        a=lst[-1]
        print(a)
        time.sleep(2)
        lst.remove(a)
t1=threading.Thread(target=f)
t2=threading.Thread(target=f)
t1.start()
t2.start()
t1.join()
t2.join()


#%%
import threading,time,queue
#注意queue是一个单独的模块
q=queue.Queue(2)
q.put('a')
q.put('b')#默认block为True，表示如果队列已经满了就卡住，等待直到有人get
#q.put('c',block=False)#把block设为False。如果队列满了会报异常    raise Full
queue.Full
print('已经放了a,b,队列长度为:',q.qsize())
time.sleep(2)
foo1=q.get()
print(foo1)#queue是先进先出
foo2=q.get_nowait()
print(foo2)
print(q.empty())
#foo3=q.get(block=False)#同理，默认为True表示没有数据就阻塞直到有人put，设为False表示不阻塞遇到为空发生raise Empty


#%%



#%%
# coding=utf-8
import codecs
from selenium import webdriver

'''
https://www.qidian.com/rank/fin?dateType=3&page=1
这是一个很典型的restful风格的URL，我们看他的URI部分，dateType表示的是哪个榜单，page代表的是第几页
这是我们要爬取的目标，是起点小说的完本小说的列表
我们的目标是获取小说的名字、作者、类型、小说的写作状况、小说的简介、最近更新的章节名称、最后的更新时间
'''

#禁止浏览器的图片和js
chromeOpt = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
        'javascript':2,
    }
}

file = codecs.open('qidian.txt','w','utf-8')
file.write("标题|作者|类型|状态|简介|最后更新章节|最后更新时间\n")

chromeOpt.add_experimental_option('prefs',prefs)
chrome = webdriver.Chrome(chrome_options=chromeOpt)
for i in range(1,26):
    chrome.get("https://www.qidian.com/rank/fin?dateType=3&page="+str(i))
    #标题
    titles = chrome.find_elements_by_xpath(r'//*[@id="rank-view-list"]/div/ul/li/div[2]/h4/a')
    #作者
    authors = chrome.find_elements_by_xpath(r'//*[@id="rank-view-list"]/div/ul/li/div[2]/p[1]/a[1]')
    #类型
    types = chrome.find_elements_by_xpath(r'//*[@id="rank-view-list"]/div/ul/li/div[2]/p[1]/a[2]')
    #小说的写作状况
    status = chrome.find_elements_by_xpath(r'//*[@id="rank-view-list"]/div/ul/li/div[2]/p[1]/span')
    #简介
    descriptions = chrome.find_elements_by_xpath(r'//*[@id="rank-view-list"]/div/ul/li/div[2]/p[2]')
    #最后更新，有固定的开头  最后更新，需要去掉
    lastUpdates = chrome.find_elements_by_xpath(r'//*[@id="rank-view-list"]/div/ul/li/div[2]/p[3]/a')
    #最后的更新时间
    lastTimes = chrome.find_elements_by_xpath(r'//*[@id="rank-view-list"]/div/ul/li/div[2]/p[3]/span')
    #开始解析内容
    print(titles)
    for i in range(len(titles)):
        file.write(titles[i].text+"|"+authors[i].text+"|"+types[i].text+"|"+status[i].text+"|"+descriptions[i].text+"|"+lastUpdates[i].text+"|"+lastTimes[i].text+"\n")

#关闭窗口
chrome.close()
#关闭文件
file.close()


#%%
# coding=utf-8
import codecs
from selenium import webdriver
import pandas as pd
'''
http://news.scujcc.cn/channels/3.html
3表示新闻第一页
后续使用的是3_2

'''
chromeOpt = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
        'javascript':2,
    }
}

file = codecs.open('jincheng.txt','w','utf-8')
file.write("标题>>时间>>内容\n")
chromeOpt.add_experimental_option('prefs',prefs)
chrome = webdriver.Chrome(chrome_options=chromeOpt)
for i in range(1,11):
    if i==1:
        chrome.get("http://news.scujcc.cn/channels/3.html")
    else:
        chrome.get("http://news.scujcc.cn/channels/3_"+str(i)+".html")
    
    title = chrome.find_elements_by_xpath(r'//*[@id="main"]/div[2]/div[2]/div[1]/ul/li/h1/a')
    time = chrome.find_elements_by_xpath(r'//*[@id="main"]/div[2]/div[2]/div[1]/ul/li/div/span[2]')
    
    link_list=[link.get_attribute('href') for link in title]
    message_title=[]
    message_time=[]
    for i in range(len(title)):
        message_title.append(title[i].text)
        message_time.append(time[i].text)
        
    message_content=[]
    for link in link_list:
        chrome.get(link)
        message_main_content=chrome.find_elements_by_xpath(r'//*[@id="main"]/div/div[2]/div/div[3]/p')
        message_body=[]
        for i in range(len(message_main_content)):
            message_body.append(message_main_content[i].text)
            str_1 = "".join(message_body)
        message_content.append(str_1.replace("\n",""))
    
    for i in range(len(message_title)):
        file.write(message_title[i]+">>"+message_time[i]+">>"+message_content[i]+"\n")


#关闭窗口
chrome.close()
#关闭文件
file.close()


#%%



#%%
import codecs
file = codecs.open('jincheng.txt','r','utf-8')
title=[]
time=[]
concent=[]
for i in file:
    list_line=i.split('>>')
    title.append(list_line[0])
    time.append(list_line[1])
    concent.append(list_line[2])

dataframe = pd.DataFrame({'title':title,'time':time,'concent':concent})
dataframe.to_csv("jincheng.csv",index=False,sep=',')
file.close()


#%%
import pandas as pd
data = pd.read_csv("jincheng_utf8.csv")
data.shape


#%%




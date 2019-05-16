import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import os,warnings,time
from threading import Thread

warnings.filterwarnings("ignore")

def get_screen_image():
    os.system(r'.\adb shell screencap -p /sdcard/sc.png')
    os.system(r'.\adb pull /sdcard/sc.png')
    img = cv2.cvtColor(cv2.imread('sc.png'),cv2.COLOR_BGR2RGB)
    return img

def jumpto(point1,point2):
        x1,y1 = point1
        x2,y2 = point2
        #计算起点和终点像素距离
        distansce = ((x1-x2)**2+(y1-y2)**2)**0.5
        #执行触摸手机命令，时间由距离乘以1.3
        os.system(r'.\adb shell input swipe 350 1250 350 1250 {0}'.format(int(distansce*1.35)))
        print("跳")

def update():
    
    time.sleep(1)
    print('更新')
    figure      = plt.figure()
    axes_image  = plt.imshow(get_screen_image())
    
    axes_image.set_array(get_screen_image())
    figure.canvas.draw()
        
def onClick(event):
    if None != event.xdata and None != event.ydata:
        x = event.xdata
        y = event.ydata
        print(x,y)
        if x > 60 and y > 60:
            coor.append([x,y])
            if 1 == len(coor):
                print("选择起点")
            else:
                print("选择终点")
            global ax
            ax = figure.add_subplot(1,1,1)
            ax.plot(x,y,'ro')
            figure.canvas.draw()

            if 2== len(coor):
                jumpto(coor.pop(),coor.pop())
                ax.lines.clear()
                thread = Thread(target= update)
                thread.start()

def resel_btn_click(event):
    print('重选')
    global ax
    if None != ax:
        coor.clear()
        ax.lines.clear()
        figure.canvas.draw()    
    
def auto_btn_click():
    a = 0 

if __name__ == '__main__':
    
    coor        = []
    ax          = None
    figure      = plt.figure()

    #截取手机屏幕图片并显示
    axes_image  = plt.imshow(get_screen_image())

    #单击事件
    figure.canvas.mpl_connect("button_press_event",onClick)
    #重选按钮
    reselect_button_position    = plt.axes([0.79,0.8,0.1,0.08])
    img_resel                   = cv2.cvtColor(cv2.imread(r'./img/bt_reselect.png'),cv2.COLOR_BGR2RGB)
    reselect_button             = Button(reselect_button_position,label="",image=img_resel)
    
    reselect_button.on_clicked(resel_btn_click)

    #自动按钮
    auto_button_position        = plt.axes([0.79,0.65,0.1,0.08])
    img_auto                    = cv2.cvtColor(cv2.imread(r'./img/bt_auto.png'),cv2.COLOR_BGR2RGB)
    auto_button                 = Button(auto_button_position,label="",image=img_auto)
    
    auto_button.on_clicked(auto_btn_click)

    #thread = Thread(target= update)
    #thread.start()
    plt.show()
    
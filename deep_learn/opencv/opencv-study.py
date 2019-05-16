import cv2
import numpy as np
import pandas as pd

#width=400
#height=400
#img = np.zeros((width,height),dtype=np.uint8)

#再利用cv2.cvtColor()函数将图像转换成BGR（Blue-Green-Red）格式。
#img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

#RGB与BGR所表示的色彩空间相同，只是字节顺序相反。当将RGB或者BGR转换成GRAY灰度图时使用如下公式：
#Gray = R*0.299 + G*0.587 + B*0.114

"""
img = np.zeros((3,3),dtype=np.uint8)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
img[:, :, 0] = 255
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
"""
#OpenCV的imread()和imwrite()支持各种静态图像文件格式，如JPG、PNG等
#img = cv2.imread(‘test.jpg’)
#img = cv2.imread(‘test.jpg’, IMREAD_GRAYSCALE)

#OpenCV的imread()和imwrite()支持各种静态图像文件格式，如JPG、PNG等
#cv2.imwrite(‘outimg.jpg’, img)
"""
cv2.imshow("main", img)
cv2.waitKey()
cv2.destroyAllWindows()
"""
#OpenCV提供VideoCapture类和VideoWriter类来支持各种格式的视频文件。
"""
videocapture = cv2.VideoCapture('test.mp4')
fps = videocapture.get(cv2.CAP_PROP_FPS)
width = int(videocapture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(videocapture.get(cv2.CAP_PROP_FRAME_HEIGHT))

success, frame = videocapture.read()

while success and cv2.waitKey(5)==-1:
    cv2.imshow('main', frame)
    success, frame = videocapture.read()
    
cv2.destroyWindow('main')
"""
#写视频
"""
videowriter = cv2.VideoWriter('outfile.avi',cv2.VideoWriter_fourcc('I','4','2','0'),fps,(width,height))

success, frame = videocapture.read()
while success:
    videowriter.write(frame)
    success, frame = videocapture.read()

"""
"""
videocapture = cv2.VideoCapture(0)

success, frame = videocapture.read()
while success and cv2.waitKey(5)==-1:
    cv2.imshow('main', frame)
    success, frame = videocapture.read()

cv2.destroyWindow('main')
videocapture.release()
"""
"""

face_cascade = cv2.CascadeClassifier(r'C:\deap-learn\haarcascades\haarcascade_frontalface_alt.xml')
img = cv2.imread(r'C:\deap-learn\trump2.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray,1.3,3)
for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

cv2.imshow("main", img)
cv2.waitKey()
cv2.destroyAllWindows()
"""


#视频捕获照片
def get_pic():
    
    videocapture = cv2.VideoCapture(0)
    success, frame = videocapture.read()
    i = 0
    while success and cv2.waitKey(300)==-1:
        face_cascade = cv2.CascadeClassifier(r'C:\deap-learn\haarcascades\haarcascade_frontalface_alt.xml')
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,3)
        for (x,y,w,h) in faces:
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            img = cv2.resize(gray[y:y+h,x:x+w],(200,200))
            cv2.imwrite('yinxin_{0}.png'.format(i), img)
            if 20 == i:
                break
            else:
                i+=1
            
        cv2.imshow('main', frame)
        success, frame = videocapture.read()
    cv2.destroyWindow('main')
    videocapture.release()

#get_pic()


def face_recognition():
    names = ['yinxin','luyangzhi','cz']

    x=[]
    y=[]
    df = pd.read_csv('faces.csv')
    data = df.values
    for path,value in data:
        img = cv2.imread('./data/'+path,cv2.IMREAD_GRAYSCALE)
        x.append(img)
        y.append(value)

    #model = cv2.face.EigenFaceReconizer_create()
    #model = cv2.face.FisherFaceReconizer_create()
    model = cv2.face.LBPHFaceRecognizer_create()
    y = np.asarray(y,dtype = np.int32)
    #print(len(x),len(y))
    model.train(x,y)

    videocapture = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(r'C:\deap-learn\haarcascades\haarcascade_frontalface_alt.xml')
    
    success, frame = videocapture.read()
    cv2.namedWindow('FaceRecog')
    while success and cv2.waitKey(1)==-1:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

            #提取检测到的人脸匹配
            roi = cv2.resize(gray[y:y+h,x:x+w],(200,200))
            #params第一个参数是识别结果，第二个参数是置信度评分
            params = model.predict(roi)

            print('label:',params)

            #标注识别结果
            cv2.putText(frame,names[params[0]],(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)


        cv2.imshow('FaceRecog',frame)
        success, frame = videocapture.read()
    cv2.destroyWindow('FaceRecog')
    videocapture.release()

face_recognition()


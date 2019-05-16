import cv2
import numpy as np
import pandas as pd
from multiprocessing import Process,Pool
import time
import os

def face_recognition(xml_adress):
    print("摄像头检测开始")

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
    face_cascade = cv2.CascadeClassifier(xml_adress)
    
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

def pic_r(xml_adress):
    print("图片检测开始")
    face_cascade = cv2.CascadeClassifier(xml_adress)
    img = cv2.imread(r'D:\deap-learn\trump2.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,3)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

    cv2.imshow("main", img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def main():
    p = Pool(processes=2)
    list=[face_recognition,pic_r]
    for i in range(2):
        p.apply_async(func = list[i], args = {r'D:\deap-learn\haarcascades\haarcascade_frontalface_alt.xml',})
    p.close()
    p.join()
    
if __name__ == "__main__":
    main()
    #face_recognition(r'D:\deap-learn\haarcascades\haarcascade_frontalface_alt.xml')
    #pic_r(r'D:\deap-learn\haarcascades\haarcascade_frontalface_alt.xml')
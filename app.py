import streamlit as st
import cv2
import numpy as np
import threading
import time
import PoseModule as pm
from pygame import mixer
import gtts  
from playsound import playsound


detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
delay=4
count_limit=0


st.title("Ai GYM Trainer")

music = st.file_uploader("Add Music to your Excercise")
try :
    mixer.music.load(music)
except Exception:
    st.write("Music Status : Not added")






stframe= st.empty()

option = st.selectbox(
     'Choose Exercise Type',
     ('reps', 'push ups', 'Squat'))
if option=="reps":
    camera = cv2.VideoCapture(1)
elif option=="push ups":
    camera = cv2.VideoCapture(1)
elif option =="Squat":
   camera = cv2.VideoCapture("sample_video/squat.mp4")
    

count_limit= st.text_input("You Can add limit to your "+option+" count (optional)")


run = st.checkbox('Start Exercise')


mixer.init()
if run:
    playsound("audio/welcome.mp3")
    count=0;
    if music:
        mixer.music.play()
else:
    mixer.music.stop()
    
   

while run:
    _, img = camera.read()
    img = cv2.resize(img,dsize=(1200,720))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
  
  
    if len(lmList) != 0:
        if option =="reps":
            # Right Arm
            angle = detector.findAngle(img, 12, 14, 16)
            
            # # Left Arm
            angle = detector.findAngle(img, 11, 13, 15)
            value1,value2=detector.windowPos(img,12);
            if int(value1)<140:
                playsound("audio/left.mp3")
            if int(value1)>910:
                playsound("audio/right.mp3")
            per = np.interp(angle, (210, 310), (0, 100))
            bar = np.interp(angle, (220, 310), (650, 100))
        elif option =="push ups":
            # Right Arm
            angle = detector.findAngle(img, 12, 14, 16)
            # # Left Arm
            angle = detector.findAngle(img, 11, 13, 15)

            # print(angle, per)
            # legs
            angle = detector.findAngle(img, 24, 26, 28)
            angle = detector.findAngle(img, 23, 25, 27)

            # # Left Arm
            angle = detector.findAngle(img, 11, 13, 15)
            per = np.interp(angle, (60, 130), (0, 100))
            bar = np.interp(angle, (60, 130), (650, 100))
        # print(angle, per)
        elif option == "Squat":
            angle = detector.findAngle(img, 12, 24, 28)
            per = np.interp(angle, (100, 170), (0, 100))
            bar = np.interp(angle, (100, 170), (650, 100))
        
        # Check for the dumbbell curls
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        print(count)
        if count!=0:
            if int(float(int(count)))>=int(float(int(count_limit))):
                cv2.putText(img, 'COUNT COMPLETED !', (200, 300), cv2.FONT_HERSHEY_PLAIN, 4,
                            color, 4)
                playsound('audio/countcom.mp3')
            
        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                            color, 4)

        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                            (255, 0, 0), 25)
    else:
        playsound("audio/wrongcam.mp3")

    cTime = time.time()
    print("cur time "+str(int(cTime)));
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, "fps:"+str(int(fps)), (70, 55), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)
      
    stframe.image(img);
else:  
   st.write('')


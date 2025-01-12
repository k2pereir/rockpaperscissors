import tensorflow as tf 
from tensorflow import keras 
model = keras.models.load_model('rpsmodel.h5')
import cv2 as cv 
import mediapipe as mp 
import numpy as np 

cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

while True:         
    ret, frame = cam.read()
    if not ret: 
        print("Camera failed")
        break    
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    myhands = hands.process(rgb_frame)  
    
    if myhands.multi_hand_landmarks: 
        for hand_landmarks in myhands.multi_hand_landmarks:
            row = list()
            for landmark in hand_landmarks.landmark:
                row.extend([landmark.x, landmark.y, landmark.z])
            row = np.array(row)
            row = row / np.max(np.abs(row), axis=0)
            prediction = model.predict(np.expand_dims(row, axis=0))
            predict = np.argmax(prediction)
            print(['rock', 'paper', 'scissors'][predict])
                
    cv.imshow("Hand", frame)
        
    if cv.waitKey(1) == ord('q'):
        break  

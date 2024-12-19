import cv2 as cv 
import mediapipe as mp 
import csv 

#initialize camera 
cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

#initialize hands 
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

#collect + save data to csv file
#the issue though, is that as soon as hands are detected the user is prompted to enter the label
#this is problematic cause half the time i'm not ready 
with open('hands_data.csv', 'w', newline='') as f: 
    write = csv.writer(f)
    write.writerow(
        ['x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'x3', 'y3', 'z3', 'x4', 'y4', 'z4', 
        'x5', 'y5', 'z5', 'x6', 'y6', 'z6', 'x7', 'y7', 'z7', 'x8', 'y8', 'z8',
        'x9', 'y9', 'z9', 'x10', 'y10', 'z10', 'x11', 'y11', 'z11', 'x12', 'y12', 'z12',
        'x13', 'y13', 'z13', 'x14', 'y14', 'z14', 'x15', 'y15', 'z15', 'x16', 'y16', 'z16',
        'x17', 'y17', 'z17', 'x18', 'y18', 'z18', 'x19', 'y19', 'z19', 'x20', 'y20', 'z20',
        'x21', 'y21', 'z21', 'label']
    )

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
                label = input("Rock, paper, scissors: ")
                row.append(label)
                write.writerow(row)
        
        cv.imshow("Hand", frame)
        if cv.waitKey(1) == ord('q'):
            break

cam.release()
cv.destroyAllWindows()
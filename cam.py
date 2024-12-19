import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.python.solutions import hands as mp_hands
import mediapipe.python.solutions.drawing_utils as mp_draw
import mediapipe.python.solutions.drawing_styles as drawing_styles
from mediapipe.tasks.python import vision 

#initialize camera 
cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

#initialize hands
hands = mp_hands.Hands(
    static_image_mode = False, 
    max_num_hands = 2,
    min_detection_confidence = 0.7,
)

#check if camera is opened
if not cam.isOpened():
    print("Cannot open camera")
    exit()

#capture video 
while True: 
    ret, frame = cam.read()
    if not ret: 
        print("Camera failed")
        break

    #rgb to process hands
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    myhands = hands.process(rgb_frame)

    #draw landmarks 
    if myhands.multi_hand_landmarks: 
        for hand_landmarks in myhands.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame, 
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                drawing_styles.get_default_hand_landmarks_style(),
                drawing_styles.get_default_hand_connections_style(),
            )
    
    cv.imshow("Hand", frame)

    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
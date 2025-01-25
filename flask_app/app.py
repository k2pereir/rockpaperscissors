from flask import Flask, render_template, request, Response, jsonify
from game import vid_processing
import cv2 as cv 
import mediapipe as mp 
import random

app = Flask(__name__)

cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def video_feed(): 
    while True:
        ret, frame = cam.read()
        if not ret: 
            print("Camera failed")
            break    
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        myhands = hands.process(rgb_frame)

        _, buffer = cv.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n') 

@app.route('/')
def home(): 
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')    

@app.route('/video')
def video(): 
    return Response(video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/process_video')
def process(): 
    ret, frame = cam.read()
    if not ret: 
        print("Camera failed")
        return None
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    myhands = hands.process(rgb_frame)  
    user = vid_processing(myhands)
    return jsonify({"result": user})

@app.route("/find_winner")
def find_winner(): 
    print("I'm in here!!!!!!!!!!")
    user = request.args.get("user")
    comp = random.choice(["rock", "paper", "scissors"])

    if not user: 
        return jsonify({"result": "Please make a choice!"})

    winnings = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    if user == comp: 
        result = "It's a tie!"
    elif winnings[user] == comp: 
        result = "You have won!!"
    else: 
        result = "You have lost :("
    return jsonify({"result": result})

@app.route('/cleanup')
def cleanup(): 
    cam.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    app.run(debug=True)
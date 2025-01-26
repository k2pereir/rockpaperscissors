# Rock, Paper, Scissors! 

Here's how it was made: 

Cam.py 
* was used to test out the mediapipe hand landmarking 
* opens the camera and draws landmarks onto hands 

collectdata.py
* opens up the camera and writes handlandmarks onto a csv file 
* manually typed whether each gesture was rock, paper, or scissors 

augment.py 
* was used to apply data augmentation techniques to the manually collected data 
* combinations of shifts, rotations, flips, and gaussian noise 

data 
* the data folder contains the original manually collected data 
* it also contains the extended csv files, each file was brought to close to 6000 lines

train.py
* was used to train a model off the data in the extended csv files 
* take a look through it to see how the training was done!

game.py 
* uses the trained model to recognize gestures in real-time

flask_app 
* contains the components for a web app of the game
import numpy as np
import math

infile = open('paper.csv', 'r') 
outfile = open('paper_extended.csv', 'w')
line = infile.readline()
data = []

#write original data 
while line!='': 
    outfile.write(line)
    line.removesuffix('\n')
    temp = line.split(',')
    temp = [float(x) for x in temp]
    data.append(temp)
    line = infile.readline()
infile.close()
outfile.close()

#add a small random shift to original data 
def add_random_shift(data, filename): 
    outfile = open(filename, 'a')
    for i in range(len(data)):
        landmarks = np.array(data[i])
        shifts = np.random.uniform(-0.1, 0.1, landmarks.shape)
        landmarks = landmarks + shifts
        outfile.write(','.join([str(x) for x in landmarks]) + '\n')
        outfile.flush()
    outfile.close()

#add small rotations to original data 
def add_random_rotation(data, filename):
    #rotate the landmarks by a given angle around a given axis
    def rotate(landmarks, angle, axis): 
        landmarks = np.array(landmarks).reshape(21, 3)
        angle = math.radians(angle)
        
        if axis == 'x': 
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, np.cos(angle), -np.sin(angle)],
                [0, np.sin(angle), np.cos(angle)]
            ])
        elif axis == 'y': 
            rotation_matrix = np.array([
                [np.cos(angle), 0, -np.sin(angle)],
                [0, 1, 0],
                [np.sin(angle), 0, np.cos(angle)]
            ])
        elif axis == 'z': 
            rotation_matrix = np.array([
                [np.cos(angle), -np.sin(angle), 0], 
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1]
            ])

        #apply linear transformation      
        rotated = np.dot(landmarks, rotation_matrix.T)
        return rotated.flatten()

    outfile = open(filename, 'a')
    for i in range(len(data)):
        landmarks = np.array(data[i])
        angle = np.random.uniform(-20, 20)
        axis = np.random.choice(['x', 'y', 'z'])
        landmarks = rotate(landmarks, angle, axis)
        outfile.write(','.join([str(x) for x in landmarks]) + '\n')
        outfile.flush()
    outfile.close()

#flip original landmarks
def flip_landmarks(data, filename):
    outfile = open(filename, 'a')
    for i in range(len(data)):
        landmarks = np.array(data[i]).reshape(21, 3)
        landmarks[:, 0] = -landmarks[:, 0]
        landmarks = landmarks.flatten()
        outfile.write(','.join([str(x) for x in landmarks]) + '\n')
        outfile.flush()
    outfile.close() 

#add gaussian noise
def add_noise(data, filename): 
    outfile = open(filename, 'a')
    for i in range(len(data)): 
        landmarks = np.array(data[i])
        noise = np.random.normal(0, 0.05, landmarks.shape)
        landmarks = landmarks + noise
        outfile.write(','.join([str(x) for x in landmarks]) + '\n')
        outfile.flush()
    outfile.close()


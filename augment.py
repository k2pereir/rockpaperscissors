import numpy as np
import math
import random 

infile = open('./data/scissors.csv', 'r') 
outfile = open('./data/scissors_extended.csv', 'w')
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
def shift(data, filename): 
    new_data = []
    outfile = open(filename, 'a')
    for i in range(len(data)):
        landmarks = np.array(data[i])
        shifts = np.random.uniform(-0.1, 0.1, landmarks.shape)
        landmarks = landmarks + shifts
        new_data.append(landmarks)
        outfile.write(','.join([str(x) for x in landmarks]) + '\n')
        outfile.flush()
    outfile.close()
    return new_data

#add small rotations to original data 
def rotate(data, filename):
    new_data = []
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
        new_data.append(landmarks)
        outfile.write(','.join([str(x) for x in landmarks]) + '\n')
        outfile.flush()
    outfile.close()
    return new_data

#flip original landmarks
def flip(data, filename):
    new_data = []
    outfile = open(filename, 'a')
    for i in range(len(data)):
        landmarks = np.array(data[i]).reshape(21, 3)
        landmarks[:, 0] = -landmarks[:, 0]
        landmarks = landmarks.flatten()
        new_data.append(landmarks)
        outfile.write(','.join([str(x) for x in landmarks]) + '\n')
        outfile.flush()
    outfile.close() 
    return(new_data)

#add gaussian noise
def noise(data, filename): 
    new_data = []
    outfile = open(filename, 'a')
    for i in range(len(data)): 
        landmarks = np.array(data[i])
        noise = np.random.normal(0, 0.05, landmarks.shape)
        landmarks = landmarks + noise
        new_data.append(landmarks)
        outfile.write(','.join([str(x) for x in landmarks]) + '\n')
        outfile.flush()
    outfile.close()
    return new_data 

def multiple_augmentations(data, filename): 
    new_data = shift(data, filename)
    outfile = open(filename, 'a')
    augmentations = [shift, rotate, flip, noise]
    num_augmentations = random.randint(1, 5)
    for i in range(num_augmentations): 
        choice = random.choice(augmentations)
        new_data = choice(new_data, filename)
    for i in range(len(new_data)):
        outfile.write(','.join([str(x) for x in new_data[i]]) + '\n')
        outfile.flush()
    outfile.close()

for i in range(100):
    multiple_augmentations(data, './data/scissors_extended.csv')
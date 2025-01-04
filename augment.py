import numpy as np

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

add_random_shift(data, 'paper_extended.csv')
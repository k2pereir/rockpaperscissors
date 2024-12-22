#sorry this is so messy i have no excuses

infile = open('collected.csv', 'r')
line = infile.readline()
outfile = open('organized.csv', 'w')
while line != '':
    line = infile.readline()
    line = line.strip()
    parts = line.split(',')
    if parts[len(parts)-1] == "rock":
        outfile.write(line + '\n')
infile.close()
infile = open('collected.csv', 'r')
line = infile.readline()
while line != '':
    line = infile.readline()
    line = line.strip()
    parts = line.split(',')
    if parts[len(parts) -1] == "paper":
        outfile.write(line + '\n')
infile.close()
infile = open('collected.csv', 'r')
line = infile.readline()
while line != '':
    line = infile.readline()
    line = line.strip()
    parts = line.split(',')
    if parts[len(parts)-1] == "scissors":
        outfile.write(line + '\n')
infile.close()
outfile.close()
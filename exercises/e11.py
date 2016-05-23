from sys import argv
from os.path import exists

script, fromFile, toFile = argv
inFile = open(fromFile)
inData = inFile.read()

outFile = open(toFile, 'w')
line1 = input('line 1 >')
outFile.write(line1)
outFile.write('\n')
outFile.close()

print('The input file is %d bytes long' % len(inData))
print('If the output file exists? %r' % exists(toFile))
write_now = input('write? > ')

if (write_now == 'y'):
	outFile = open(toFile,'w')
	outFile.write(inData)
	outFile.close()

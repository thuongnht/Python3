from sys import argv

script, filename = argv
text = open(filename, 'w')

line1 = input('line 1 >')
line2 = input('line 2 >')
text.write(line1)
text.write('\n')
text.write(line2)
text.write('\n')
text.close()

truncate = input('would you like to erase it >')
if (truncate == 'y'):
	text = open(filename,'w')
	text.truncate()
	text.close()

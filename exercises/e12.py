from sys import argv
from os.path import exists

script, fromFile = argv

def printAll(f):
	print(f.read())

def rewind(f):
	f.seek(0)
	
def printLine(l, f):
	print('Line %r' %l, f.readline())
	
current = open(fromFile)
while (True):	
	what = input('like \(all=a, rewind=r, line=l\) >')
	if (what == 'e'):
		break
	elif (what == 'a'):
		printAll(current)
	elif (what == 'r'):
		rewind(current)
	elif (what == 'l'):
		printLine(1, current)
	else:
		continue
current.close()
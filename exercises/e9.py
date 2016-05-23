from sys import argv

script, filename = argv
text = open(filename)

print('Your script %r reading the file %r' % (script, filename) )
print(text.read())
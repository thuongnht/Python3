x = "There are %d types of people." %10
binary = 'binary'
do_not = "don't"
y = "Those who know %s and those who %r" %(binary, do_not)

print('I said: %r' %x)
print('I also said: "%s"' %y)

hilarious = False
joke = "Isn't that joke no fun? %r" 

print(joke % hilarious)
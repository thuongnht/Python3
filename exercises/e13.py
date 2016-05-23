def break_words(s):
	return s.split(' ')

def print_first(w):
	print(w.pop(0))
	
def print_last(w):
	print(w.pop(-1))
	
def print_first_and_last(s):
	w = break_words(s)
	print_first(w)
	print_last(w)
	
def sort_words(w):
	return sorted(w)
	
def sort_sentence(s):
	w = break_words(s)
	return sort_words(w)
	
def print_first_and_last_sorted(s):
	w = sort_sentence(s)
	print_first(w)
	print_last(w)
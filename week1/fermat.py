def check_fermat(a, b, c, n):
	if n > 2 and (a**n + b**n == c**n):
		print "Holy snokes, Fermat was wrong!"
	else:
		print "No, that doesn't work."

def check_me_out_fermat():
	a = (int)input("What is a?")
	b = (int)input("What is b?")
	c = (int)input("What is c?")
	n = (int)input("What is n?")
	check_fermat(a,b,c,n)

check_me_out_fermat()

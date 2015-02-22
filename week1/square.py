def make_beam():
	print '+ - - - -',

def make_post():
	print '|        ',

def make_beams():
	make_beam()
	make_beam()
	print '+'

def make_posts():
	make_post()
	make_post()
	print '|'

def make_row():
	make_beams()
	for i in range(4):
		make_posts()

def make_whole_shebang():
	make_row()
	make_row()
	make_beams()

def make_whole_shebang2():
	print '+ - - - - + - - - - +\n|         |         |\n|         |         |\n|         |         |\n|         |         |\n+ - - - - + - - - - +\n|         |         |\n|         |         |\n|         |         |\n|         |         |\n+ - - - - + - - - - +'

make_whole_shebang()

make_whole_shebang2()
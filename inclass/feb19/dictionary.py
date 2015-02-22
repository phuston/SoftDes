import re
import random

f = open('/usr/share/dict/words','r')

words = [word.rstrip('\n') for word in f]

print words

sentence = ""

for i in range(20):
	sentence += (random.choice(words) + " ")

print sentence

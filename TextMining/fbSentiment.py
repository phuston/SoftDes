# fb_license = CAAEuAis8fUgBAH31cSTZCiUpBQpuqyqIZC7V2dSNnfjZANXoRv6aVCoUdBO8kcg4Bo5MUAZCZBdfmZCZAW2mB1v3ye5BQbZAXjaxQ94kL1PqaQhZBZBu42aGBoE1Vbvd6qgFe7kpVP2234lazFnuUktsGYcmbfMdj25KsZA4jZAZAHobqpKCZBZCq2EGEjT

from pattern.web import *
from pattern.en import *
from datetime import datetime
import re
import matplotlib.pyplot as plt
import numpy as np

def is_useful_post(post_text):
	'''Given the input post text, determines
	whether or not the post is substantial, 
	not just sharing a link or updating photos
	
	Input: Raw text of post
	Output: Boolean of whether post is 'useful'
	'''

	cov_photo = re.match(r'.*?updated.*?cover photo', post_text)
	life_event = re.match(r'.*?added a life event.*?', post_text)
	share_photo = re.match(r'.*?shared.*?photo.*?', post_text)
	share_video = re.match(r'.*?shared.*?video.*?', post_text)
	share_link = re.match(r'.*?shared.*?link.*?', post_text)
	comment = re.match(r'.*?commented on.*?', post_text)
	link = re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', post_text)

	if cov_photo or life_event or share_photo or share_video or share_link or link:
		return False

	else:
		return True

def create_post_dictionary(fb):
	'''Creates a dictionary of friends --> Includes 
	profile information, total number of text posts,
	and average sentiment over all posts 

	Input: fb - pattern.web facebook session
	Output: friend post dictionary
	'''
	me = fb.profile()
	friend_dict = {}

	my_friends = fb.search(me[0], type=FRIENDS, count=300)
	for friend in my_friends:
		friend_prof = fb.profile(id=friend.id)
		print friend_prof
		user_element = create_user_element(friend, fb)
		if user_element:
			friend_dict[friend_prof] = user_element
	return friend_dict


def create_user_element(friend, fb):
	'''Creates tuple of a user's total number of posts,
	average sentimentality, and subjectivity.

	Inputs: pattern.web friend object, pattern.web fb session
	Output: tuple of friend information to be added to
	dictionary created by 'create_post_dictionary' '''


	tot_post = 0.0
	sent = 0.0
	subj = 0.0
	friend_news = fb.search(friend.id, type=NEWS, count=1000)
	for news in friend_news:
		# dt = datetime.strptime(news.date, "%Y-%m-%dT%H:%M:%S+0000")
		if is_useful_post(news.text):
			# print news.text
			tot_post += 1
			post_anal = sentiment(news.text)
			sent += post_anal[0]
			subj += post_anal[1]
	if tot_post > 0:
		return (tot_post,sent/tot_post,subj/tot_post)
	else: return None



if __name__ == "__main__":
	facebook = Facebook(license='CAAEuAis8fUgBAH31cSTZCiUpBQpuqyqIZC7V2dSNnfjZANXoRv6aVCoUdBO8kcg4Bo5MUAZCZBdfmZCZAW2mB1v3ye5BQbZAXjaxQ94kL1PqaQhZBZBu42aGBoE1Vbvd6qgFe7kpVP2234lazFnuUktsGYcmbfMdj25KsZA4jZAZAHobqpKCZBZCq2EGEjT', throttle = 0.5)
	
	create_post_dictionary(facebook)
	my_dict = create_post_dictionary(facebook)

	male_sent = []
	fem_sent = []

	male_sub = []
	fem_sub = []

	for friend, friend_info in my_dict.iteritems():
		if str(friend[3])=='m':
			male_sent.append(my_dict[friend][1])
			male_sub.append(my_dict[friend][2])
		elif str(friend[3])=='f':
			fem_sent.append(my_dict[friend][1])
			fem_sub.append(my_dict[friend][2])


	print "Average male sentimentality: " + str(np.mean(male_sent))
	print "Average female sentimentality: " + str(np.mean(fem_sent))
	print "Average male subjectivity: " + str(np.mean(male_sub))
	print "Average female subjectivity: " + str(np.mean(fem_sub))
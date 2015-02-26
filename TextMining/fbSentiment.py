# fb_license = CAAEuAis8fUgBAH31cSTZCiUpBQpuqyqIZC7V2dSNnfjZANXoRv6aVCoUdBO8kcg4Bo5MUAZCZBdfmZCZAW2mB1v3ye5BQbZAXjaxQ94kL1PqaQhZBZBu42aGBoE1Vbvd6qgFe7kpVP2234lazFnuUktsGYcmbfMdj25KsZA4jZAZAHobqpKCZBZCq2EGEjT

from pattern.web import *
from pattern.en import *
from datetime import datetime
import re
import matplotlib.pyplot as plt
import numpy as np
import os
import MySQLdb

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

	# If the re.match returns a non-null result, return True to indicate the usefulness of the post
	if cov_photo or life_event or share_photo or share_video or share_link or link:
		return False
	else:
		return True

def create_post_date_dictionary(fb, cursor):
	'''Creates a dictionary of friends --> Includes 
	profile information, total number of text posts,
	and average sentiment over all posts 

	Input: fb - pattern.web facebook session
	Output: friend post dictionary
	'''

	me = fb.profile()
	post_list = []

	my_friends = fb.search(me[0], type=FRIENDS, count=700)
	for i,friend in enumerate(my_friends):

		# Indicator for progress in calling pattern API
		os.system('clear')
		print str((i/float(len(my_friends)))*100) + ' percent complete.'

		# Search for friend's posts
		friend_news = fb.search(friend.id, type=NEWS, count=1000)
		for news in friend_news:
			if is_useful_post(news.text):

				# Gets the day of the year and the positivity of the post
				news_date = datetime.strptime(news.date, "%Y-%m-%dT%H:%M:%S+0000").timetuple().tm_yday
				post_sent = sentiment(news.text)[0]

				# Access database connection, add row for facebook post day year and sentiment
				cursor.execute('INSERT INTO fb_posts(day_yr, sentiment) VALUES(%d, %f)' %(news_date, post_sent))

	return True



def create_friend_post_dictionary(fb):
	'''Creates a dictionary of friends --> Includes 
	profile information, total number of text posts,
	and average sentiment over all posts 

	Input: fb - pattern.web facebook session
	Output: friend post dictionary
	'''

	me = fb.profile()
	friend_dict = {}

	# Search through all friends
	my_friends = fb.search(me[0], type=FRIENDS, count=700)
	for friend in my_friends:

		# Access friend's profile to gain access to user information
		friend_prof = fb.profile(id=friend.id)
		user_element = create_user_element(friend, fb)

		# Adds friend's element to dictionary if friend has more than 0 posts
		if user_element:
			friend_dict[friend_prof] = user_element

	return friend_dict


def create_user_element(friend, fb):
	'''Creates tuple of a user's total number of posts,
	average sentimentality, and subjectivity.

	Inputs: pattern.web friend object, pattern.web fb session
	Output: tuple of friend information to be added to
	dictionary created by 'create_friend_post_dictionary' '''

	tot_post = 0.0
	sent = 0.0
	subj = 0.0

	# Get friend's posts
	friend_news = fb.search(friend.id, type=NEWS, count=1000)
	for news in friend_news:

		# If useful post, get sentimentality and subjectivity
		if is_useful_post(news.text):

			tot_post += 1
			post_anal = sentiment(news.text)
			sent += post_anal[0]
			subj += post_anal[1]


	# If user has more than 0 posts, return average positivity and subjectivity
	if tot_post > 0:
		return (tot_post,sent/tot_post,subj/tot_post)

	else: return None



if __name__ == "__main__":	
	# Connects to MySQL database locally
	print 'Accessing MySQL database...'
	db = MySQLdb.connect(host="localhost", user="phuston", passwd="1nval1dpass", db="fbsentiment")
	cursor = db.cursor()

	#Selects all rows from database table
	cursor.execute("SELECT * FROM fb_posts")

	# Gets the number of rows in the resultset
	numrows = int(cursor.rowcount)

	# If database table is not populated, create it using the 'create_post_date_dictionary' method
	if numrows == 0:
		facebook = Facebook(license='CAAEuAis8fUgBAH31cSTZCiUpBQpuqyqIZC7V2dSNnfjZANXoRv6aVCoUdBO8kcg4Bo5MUAZCZBdfmZCZAW2mB1v3ye5BQbZAXjaxQ94kL1PqaQhZBZBu42aGBoE1Vbvd6qgFe7kpVP2234lazFnuUktsGYcmbfMdj25KsZA4jZAZAHobqpKCZBZCq2EGEjT', throttle = 0.5)
		create_post_date_dictionary(facebook, cursor)


	day_dict = {}
	# Gets and display one row at a time
	for x in range(0,numrows):
		row = cursor.fetchone()
		day = str(row[0])
		sent = row[1]
		day_dict[day] = day_dict.get(day, []) + [sent]

	db.commit()
	# disconnect from server
	db.close()

	# Just a little bit of error checking, yo; it's good for the soul
	if "None" in day_dict:
		del day_dict["None"]

	# Takes sentiment lists for each day, finds mean sentiment
	for day, sentiments in day_dict.iteritems():
		try: 
			day_dict[day] = float(sum(sentiments))/len(sentiments) if len(sentiments) > 0 else float('nan')
		except:
			day_dict[day] = 0.0

	days = [int(day) for day in day_dict.keys()]
	values = day_dict.values()

	plt.plot(days, values, marker = '*', linestyle='None')
	plt.axis([0, 365, -1, 1])
	plt.xlabel('Day of Year',fontsize=25)
	plt.ylabel('Average Positivity of all Posts',fontsize=25)
	plt.title('Average Daily Positivity of Facebook Posts vs. Day of Year',fontsize=30)

	plt.show()



	#****************CODE BELOW HERE FOR GENDER-BASED NLP ANALYSIS*************
	# post_dict = create_post_date_dictionary(facebook)

	# for post_el in post_dict:
	# 	print str(post[0]) + str(post[1])


	# my_dict = create_friend_post_dictionary(facebook)

	# male_sent = []
	# fem_sent = []

	# male_sub = []
	# fem_sub = []

	# for friend, friend_info in my_dict.iteritems():
	# 	if str(friend[3])=='m':
	# 		male_sent.append(my_dict[friend][1])
	# 		male_sub.append(my_dict[friend][2])
	# 	elif str(friend[3])=='f':
	# 		fem_sent.append(my_dict[friend][1])
	# 		fem_sub.append(my_dict[friend][2])


	# print "Average male sentimentality: " + str(np.mean(male_sent))
	# print "Average female sentimentality: " + str(np.mean(fem_sent))
	# print "Average male subjectivity: " + str(np.mean(male_sub))
	# print "Average female subjectivity: " + str(np.mean(fem_sub))
	#**************************************************************************

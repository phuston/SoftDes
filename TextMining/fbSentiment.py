# fb_license = CAAEuAis8fUgBAH31cSTZCiUpBQpuqyqIZC7V2dSNnfjZANXoRv6aVCoUdBO8kcg4Bo5MUAZCZBdfmZCZAW2mB1v3ye5BQbZAXjaxQ94kL1PqaQhZBZBu42aGBoE1Vbvd6qgFe7kpVP2234lazFnuUktsGYcmbfMdj25KsZA4jZAZAHobqpKCZBZCq2EGEjT

from pattern.web import *
from pattern.en import *
from datetime import datetime
import re

def is_useful_post(post_text):
	'''Given the input post text, determines
	whether or not the post is substantial, 
	not just sharing a link or updating photos'''

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
	me = fb.profile()
	friend_dict = {}

	my_friends = fb.search(me[0], type=FRIENDS, count=5)
	for friend in my_friends:
		friend_prof = fb.profile(id=friend.id)
		friend_dict[friend_prof] = create_user_element(friend, fb)
	return friend_dict


def create_user_element(friend, fb):
	friend_posts = {}
	friend_news = fb.search(friend.id, type=NEWS, count=10)
	for news in friend_news:
		dt = datetime.strptime(news.date, "%Y-%m-%dT%H:%M:%S+0000")
		if is_useful_post(news.text):
			friend_posts[str(news.id)] = sentiment(news.text)
	return friend_posts



if __name__ == "__main__":
	facebook = Facebook(license='CAAEuAis8fUgBAH31cSTZCiUpBQpuqyqIZC7V2dSNnfjZANXoRv6aVCoUdBO8kcg4Bo5MUAZCZBdfmZCZAW2mB1v3ye5BQbZAXjaxQ94kL1PqaQhZBZBu42aGBoE1Vbvd6qgFe7kpVP2234lazFnuUktsGYcmbfMdj25KsZA4jZAZAHobqpKCZBZCq2EGEjT')
	
	create_post_dictionary(facebook)

	my_dict = create_post_dictionary(facebook)

	print my_dict

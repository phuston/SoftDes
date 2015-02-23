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


my_friends = f.search(me[0], type=FRIENDS, count=10)
for friend in my_friends:
    friend_news = f.search(friend.id, type=NEWS, count=100000)
    for news in friend_news:
    	dt = datetime.strptime(news.date, "%Y-%m-%dT%H:%M:%S+0000")
    	if is_useful_post(news.text):
        	print news.text



if __name__ == "__main__":
	f = Facebook(license='CAAEuAis8fUgBAH31cSTZCiUpBQpuqyqIZC7V2dSNnfjZANXoRv6aVCoUdBO8kcg4Bo5MUAZCZBdfmZCZAW2mB1v3ye5BQbZAXjaxQ94kL1PqaQhZBZBu42aGBoE1Vbvd6qgFe7kpVP2234lazFnuUktsGYcmbfMdj25KsZA4jZAZAHobqpKCZBZCq2EGEjT')
	me = f.profile()
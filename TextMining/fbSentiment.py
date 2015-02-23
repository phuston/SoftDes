# fb_license = CAAEuAis8fUgBAH31cSTZCiUpBQpuqyqIZC7V2dSNnfjZANXoRv6aVCoUdBO8kcg4Bo5MUAZCZBdfmZCZAW2mB1v3ye5BQbZAXjaxQ94kL1PqaQhZBZBu42aGBoE1Vbvd6qgFe7kpVP2234lazFnuUktsGYcmbfMdj25KsZA4jZAZAHobqpKCZBZCq2EGEjT

from pattern.web import *
from datetime import datetime
import re

def is_useful_post(post_text):
	"""Given the input post text, determines
	whether or not the post is substantial, 
	not just sharing a link or updating photos"""

	cov_photo = re.match(r".*?updated.*?cover photo", post_text)
	life_event = re.match(r".*?added a life event.*?", post_text)
	share_photo = re.match(r".*?shared.*?photo.*?", post_text)
	share_video = re.match(r".*?shared.*?video.*?", post_text)
	share_link = re.match(r".*?shared.*?link.*?", post_text)

	if cov_photo or life_event or share_photo or share_video or share_link:
		return False

	else:
		return True

f = Facebook(license='CAAEuAis8fUgBAH31cSTZCiUpBQpuqyqIZC7V2dSNnfjZANXoRv6aVCoUdBO8kcg4Bo5MUAZCZBdfmZCZAW2mB1v3ye5BQbZAXjaxQ94kL1PqaQhZBZBu42aGBoE1Vbvd6qgFe7kpVP2234lazFnuUktsGYcmbfMdj25KsZA4jZAZAHobqpKCZBZCq2EGEjT')
me = f.profile()
print len(f.search(me[0], type=FRIENDS, count=10000))


my_friends = f.search(me[0], type=FRIENDS, count=10)
for friend in my_friends:
    friend_news = f.search(friend.id, type=NEWS, count=100000)
    for news in friend_news:
    	dt = datetime.strptime(news.date, "%Y-%m-%dT%H:%M:%S+0000")
    	if is_useful_post(news.text):
        	print news.text



# print is_useful_post("Patrick updated his cover photo.")
# print is_useful_post("Patrick added a life event from June 25, 1996: Was born.")
# print is_useful_post("Oh my god I want to love people from all places!")
# print is_useful_post("Jeffrey Aubin shared a video to Kyle Armillotti's timeline.")
# print is_useful_post("Kyle Armillotti shared The Ghost of Patrick Swayze's photo.")
# print is_useful_post("Dylan Matthew Coito added a life event from March 2013: First Met Madalyn Schultz.")



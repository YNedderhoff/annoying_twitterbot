# -*- coding: utf-8 -*-

import tweepy
import json
import random
from replies import replies_list_wenn, replies_list_haette
from access import consumer_secret, consumer_key, access_token, access_token_secret, user_var

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.get_user(user_var)

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
	last_own_tweet = None
	def on_data(self, data):
		# Twitter returns data in JSON format - we need to decode it first
		data = json.loads(data)
		username = data.get('user').get('screen_name')
		text = data.get('text')
		if random.randint(0, 10) == 4:
			if text.lower().startswith('wenn'):
				new_status = random.choice(replies_list_wenn)
				while new_status == self.last_own_tweet:
					new_status = random.choice(replies_list_wenn)
				last_own_tweet = new_status
				print "Tweet: "+text
				print "Answer: "+last_own_tweet
				api.update_status(status='@%s %s' % (data.get('user').get('screen_name'), last_own_tweet), in_reply_to_status_id=data.get('id'))
			elif text.lower().startswith(u'hätte'):
				new_status = random.choice(replies_list_haette)
				while new_status == self.last_own_tweet:
					new_status = random.choice(replies_list_haette)
				last_own_tweet = new_status
				print "Tweet: "+text
				print "Answer: "+last_own_tweet
				api.update_status(status='@%s %s' % (data.get('user').get('screen_name'), last_own_tweet), in_reply_to_status_id=data.get('id'))
		else:
			print "Tweet: "+text
			print "--> Der Zufall wollte nicht antworten ..."""
		return True

	def on_error(self, status):
		print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = tweepy.Stream(auth, l)
    stream.filter(track=['Wenn', u'Hätte'],
                      languages=['de'])

	

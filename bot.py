# -*- coding: utf-8 -*-

import tweepy
import json
import random
from replies import replies_list_wenn
from replies import replies_list_haette

consumer_secret = "ThI2q4Q0eC7aOl1cWiwrbuYtgBKFDUibQCmNQzMIKeA6Qbx4fG"
consumer_key = "xfssNUzqIfE1C5FC3daLUzygn"

access_token = "2996189218-Xvw0iHz9R3YU7SUZhsgTquEel7Q4KCMqcwjgGm1"
access_token_secret = "3FRkM6Pn5qrl9wq4eL5zBZLo48XmFztoNSAiHrqocyjL4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.get_user('scheisshund')

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    last_own_tweet = None
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        data = json.loads(data)
        username = data.get('user').get('screen_name')
        text = data.get('text')
        if text.lower().startswith('wenn'):
            if random.randint(0, 10) == 4:
                new_status = random.choice(replies_list_wenn)
                while new_status == self.last_own_tweet:
                    new_status = random.choice(replies_list_wenn)
                last_own_tweet = new_status
                print "Tweet: "+text
                print "Answer: "+last_own_tweet
                api.update_status(status='@%s %s' % (data.get('user').get('screen_name'),
                                                     last_own_tweet),
                                  in_reply_to_status_id=data.get('id')
                              )

            else:
                print "Tweet: "+text
                print "--> Der Zufall wollte nicht antworten ..."
        elif text.lower().startswith('haette'):
            new_status = random.choice(replies_list_haette)
            while new_status == self.last_own_tweet:
                new_status = random.choice(replies_list_haette)
            last_own_tweet = new_status
            print "Tweet: "+text
            print "Answer: "+last_own_tweet
            api.update_status(status='@%s %s' % (data.get('user').get('screen_name'),
                                                 last_own_tweet),
                              in_reply_to_status_id=data.get('id')
                          )
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['Wenn'],
                      languages=['de'])



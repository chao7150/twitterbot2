import tweepy
import sys, os
import profiles
import rep
import random

auth = tweepy.OAuthHandler(profiles.CONSUMER_KEY, profiles.CONSUMER_SECRET)
auth.set_access_token(profiles.ACCESS_TOKEN, profiles.ACCESS_SECRET)
api = tweepy.API(auth)

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.in_reply_to_screen_name == 'pcuso5':
            rep.response_chain(api, status)
        elif ('bot' in status.text) or ('pcuso5' in status.text):
            coin = random.random()
            if coin < 0.05:
                api.update_status('はい', in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)
            else:
                api.create_favorite(status.id)
        print(status.text)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.userstream()
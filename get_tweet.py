#!/usr/bin/env python
# -*- coding:utf-8 -*-

#Tweepyのインポート
import profile
import morph
import tweepy

#keyの取得
auth = tweepy.OAuthHandler(profile.CONSUMER_KEY, profile.CONSUMER_SECRET)
auth.set_access_token(profile.ACCESS_TOKEN, profile.ACCESS_SECRET)

api = tweepy.API(auth)

recentTweets = api.user_timeline('pcuso4', count = 2)
for t in recentTweets:
    words = morph.morph(t.text)
    print(words)
    generate = words[0]
    for w in words[1:]:
        generate = generate + "/" +w
    print(generate)
    api.update_status(generate)
#!/usr/bin/env python
# -*- coding:utf-8 -*-

#Tweepyのインポート
import profile
import morph
import tweepy
import DBconnect
import hashlib
import sys
import re
import os

#keyの取得
auth = tweepy.OAuthHandler(profile.CONSUMER_KEY, profile.CONSUMER_SECRET)
auth.set_access_token(profile.ACCESS_TOKEN, profile.ACCESS_SECRET)
api = tweepy.API(auth)

dirname = os.path.dirname(os.path.abspath(__file__)) + "/newest.txt"
print(dirname)
with open(dirname, "r") as f:
    since = f.read()

recentTweets = api.user_timeline(profile.USERNAME, since_id=since)
if not recentTweets:
    print("nothing to retrieve")
    sys.exit()

ids = [int(t.id) for t in recentTweets]
print(ids)
newest = max(ids)
with open(dirname, "w") as f:
    print(f.write(str(newest)))

db = DBconnect.Database()
for t in recentTweets:
    if t.text[:3] == "RT ":
        continue
    if t.in_reply_to_user_id:
        continue
    text = re.sub(r'#([\w一-龠ぁ-んァ-ヴ]+)', '', t.text)
    text = re.sub(r'@[\w]{1,15}', '', text)
    text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', text).strip()
    if not text:
        continue
    words = morph.morph(text)
    words.insert(0, "STARTKEY")
    words.append("ENDKEY")
    num = len(words)
    for n in range(num - 2):
        hsh = hashlib.md5((words[n] + words[n + 1] + words[n + 2]).encode('utf-8')).hexdigest()
        db.insert([hsh, words[n], words[n + 1], words[n + 2], 1])

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import morph
import DBconnect
import hashlib
import re
import json
import os
import random

filelist = sorted(os.listdir("tweets"))
k = 6
for filename in filelist:
    k += 2
    filename = "tweets/"+filename
    print(filename)
    with open(filename, 'r') as f:
        next(f)
        tweets = json.load(f)
    samples = random.sample(tweets, k)

    db = DBconnect.Database()
    for t in samples:
        text = t["text"]
        if text[:3] == "RT ":
            continue
        if t["entities"]["user_mentions"]:
            continue
        text = re.sub(r'#([\w一-龠ぁ-んァ-ヴ]+)', '', text)
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
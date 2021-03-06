import DBconnect
import random
import math
import tweepy
import feature
import profiles
import sys
from collections import Counter

def weighted_choice(res):
    weight = [int(math.log(row[4])) + 1 for row in res]
    return list(random.choices(res, weights=weight)[0])

def merge_dict_add_values(dic1, dic2):
    return dict(Counter(dic1) + Counter(dic2))

def double_chain(api, status):
    db = DBconnect.Database()
    first = weighted_choice(db.read_single("STARTKEY", "first"))
    chain = []
    chain.append(first[2])
    chain.append(first[3])
    while(chain[-1] != "ENDKEY"):
        rawchain = db.read_double(chain[-2], chain[-1])
        ring = weighted_choice(rawchain)
        chain.append(ring[3])
    chain.pop()
    text = "".join(chain)
    api.update_status(text, in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)

def response_chain(api, status):
    db = DBconnect.Database()
    recent = api.home_timeline(count=5)
    dic = {}
    for t in recent:
        tmpdic = feature.get(t.text)
        dic = merge_dict_add_values(dic, tmpdic)
    words = []
    weights = []
    for word, weight in dic.items():
        words.append(word)
        weights.append(weight)
    keyword = random.choices(words, weights=weights)[0]
    first_rawchain = db.read_single(keyword, "second")
    if first_rawchain:
        first_ring = weighted_choice(first_rawchain)
        chain = first_ring[1:4]
        while(chain[-1] != "ENDKEY"):
            rawchain = db.read_double(chain[-2], chain[-1])
            ring = weighted_choice(rawchain)
            chain.append(ring[3])
        while(chain[0] != "STARTKEY"):
            rawchain = db.read_double_back(chain[0], chain[1])
            ring = weighted_choice(rawchain)
            chain.insert(0, ring[1])
        chain.pop()
        text = "".join(chain[1:])
        api.update_status(text, in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)
    else:
        double_chain(api, status)
        return

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(profiles.CONSUMER_KEY, profiles.CONSUMER_SECRET)
    auth.set_access_token(profiles.ACCESS_TOKEN, profiles.ACCESS_SECRET)
    api = tweepy.API(auth)

    coin = random.random()
    if coin < 0.4:
        single_chain(api)
    elif coin < 0.8:
        double_chain(api)
    else:
        response_chain(api)
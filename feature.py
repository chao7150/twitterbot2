import requests
import profile
import json
import profile

def get(text):
    baseurl = "http://jlp.yahooapis.jp/KeyphraseService/V1/extract"
    params = {
        'appid' : profile.YAHOO_APPID,
        'sentence' : text,
        'output' : 'json'
    }
    r = requests.get(baseurl, params=params)
    return json.loads(r.text)
#coding: utf-8
#copied from http://qiita.com/OvKNyRgir3BuEJj/items/9b8f2ab97ba856671848

import requests
import profile
from xml.etree.ElementTree import *

def POST(body):
    request_URL = "http://jlp.yahooapis.jp/MAService/V1/parse"

    parameter = {'appid': profile.YAHOO_APPID,
                'sentence': body,
                'results': 'ma'}
    r = requests.get(request_URL, params=parameter)
    yield (r, r.text)

def XML_parse(body):
    elem = fromstring(body)
    words = []
    for e in elem.getiterator("{urn:yahoo:jp:jlp}surface"):
        words.append(e.text)
    return words

def morph(body):
    for response in POST(body):
        r = response[0]
        text = response[1]
    return XML_parse(text.encode('utf-8'))#encodeしないとUnicode-error  

if __name__ == '__main__':
    for response in POST(body="今日はいい天気ですね"):
        r = response[0]
        text = response[1]
    XML_parse(text.encode('utf-8'))#encodeしないとUnicode-error
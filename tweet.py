#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from requests_oauthlib import OAuth1Session
from dateutil import parser
from pytz import timezone
from datetime import datetime

CK = os.environ["CONSUMER_KEY"]                            # Consumer Key
CS = os.environ["CONSUMER_SECRET"]                          # Consumer Secret
AT = os.environ["ACCESS_TOKEN_KEY"] # Access Token
AS = os.environ["ACCESS_TOKEN_SECRET"]        # Accesss Token Secert

# OAuth認証で POST method で投稿
twitter = OAuth1Session(CK, CS, AT, AS)

def tweet(params):
  # ツイート投稿用のURL
  url = "https://api.twitter.com/1.1/statuses/update.json"
  req = twitter.post(url, params = params)

def mentions():
  # ツイート投稿用のURL
  url = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json'
  params = {"count": "20"}
  return twitter.get(url, params = params)


req = mentions()

f = open('time.txt', 'r')
last_time_str = f.read()
f.close()

if last_time_str == '':
  last_time = datetime(1,1,1,tzinfo=timezone('Asia/Tokyo'))
else:
  last_time = parser.parse(last_time_str)

# レスポンスを確認
if req.status_code == 200:
#    print ("OK")

    most_lated_time = last_time;
    for r in req.json():
#      text = r['text']
      user_name = r['user']['screen_name']
      id_str = r['id_str']
      utc_string = r['created_at']
      jst_time = parser.parse(utc_string).astimezone(timezone('Asia/Tokyo'))
      # 前回の最終時刻より後のツイートを表示
      if jst_time > last_time:
        # ツイート本文
        text = '@'+user_name+' そうじゃないよ!'
        params = { "status": text, "in_reply_to_status_id": id_str}    
        tweet(params)
#        print(text)
#        print(jst_time)
      # 一番最後のツイートの時間を記録
      if jst_time > most_lated_time:
        most_lated_time = jst_time

else:
#    print ("Error: %d" % req.status_code)


f = open('time.txt', 'w')
f.write(str(most_lated_time))
f.close()
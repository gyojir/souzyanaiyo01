#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import MySQLdb
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

def run():

  connector = MySQLdb.connect(host=os.environ["MYSQL_SERVICE_HOST"], db=os.environ["MYSQL_DATABASE"], user=os.environ["MYSQL_USER"], passwd=os.environ["MYSQL_PASSWORD"], charset="utf8")
  connector.autocommit(False)
  cursor = connector.cursor()

  cursor.execute('select dt from time where id=0')
  records = cursor.fetchall()

  if records:
    last_time = records[0][0].replace(tzinfo=timezone('Asia/Tokyo'))
  else:
    last_time = datetime(2017,1,1,tzinfo=timezone('Asia/Tokyo'))
  print last_time

  req = mentions()

  # レスポンスを確認
  if req.status_code == 200:
      print ("OK")

      most_lated_time = last_time;
      for r in req.json():
        text = r['text']
        user_name = r['user']['screen_name']
        id_str = r['id_str']
        utc_string = r['created_at']
        jst_time = parser.parse(utc_string).astimezone(timezone('Asia/Tokyo'))
        # 前回の最終時刻より後のツイートを表示
        if jst_time > last_time:
          # ツイート本文
          text = '@'+user_name+u' そうじゃないよ!'
          text = text.encode('utf-8')
          params = { "status": text, "in_reply_to_status_id": id_str}    
          tweet(params)
          print(text)
          print(jst_time)
        # 一番最後のツイートの時間を記録
        if jst_time > most_lated_time:
          most_lated_time = jst_time

  else:
      print ("Error: %d" % req.status_code)

  try:
    cursor.execute('update time set dt="'+most_lated_time.strftime('%Y-%m-%d %H:%M:%S')+'" where id=0')
    cursor.execute('select * from time')
    connector.commit()
    records = cursor.fetchall()
    for record in records:
      print record
    print 'Complete!'
  except Exception as e:
    connector.rollback()
    raise e
  finally:
    cursor.close()
    connector.close()

def random_tweet():
  connector = MySQLdb.connect(host=os.environ["MYSQL_SERVICE_HOST"], db=os.environ["MYSQL_DATABASE"], user=os.environ["MYSQL_USER"], passwd=os.environ["MYSQL_PASSWORD"], charset="utf8")
  connector.autocommit(False)
  cursor = connector.cursor()

  cursor.execute('select word from words order by rand() limit 1')
  records = cursor.fetchall()

  if records:
    text = records[0][0]#.encode('utf-8')
  else:
    return
  print text

  # ツイート本文
  params = {"status": text}  
  tweet(params)

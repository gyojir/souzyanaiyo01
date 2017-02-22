# -*- coding: utf-8 -*-

from flask import Flask
import tweet
application = Flask(__name__)

@application.route("/")
def hello():
    tweet.run()
    return "Hello World!"

@application.route("/rand")
def rand():
    tweet.random_tweet()
    return "souzyanaiyo!"

if __name__ == "__main__":
    application.run()
# -*- coding: utf-8 -*-

from flask import Flask
import tweet
application = Flask(__name__)

@application.route("/")
def hello():
    tweet.run()
    return "Hello World!"

if __name__ == "__main__":
    application.run()
#!/usr/bin/env python3

import tweepy
from creds import consumer_key, consumer_secret, access_token, access_token_secret
from time import sleep
from html import unescape

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def criteria(tweet):
    if ("RT" in tweet.text) or ("t.co" in tweet.text) or (len(tweet.text) > 48):
        return False
    if api.get_status(tweet.id).retweeted:
        return False
    return True

def retweet():
    blacklist = open("blacklist.txt", "r").read().splitlines()
    search = "\"an inside job\" -" + " -".join(blacklist)

    tweets = api.search(q=search, lang='en', count=100)
    tweets[:] = [tweet for tweet in tweets if criteria(tweet)]
    tweet = tweets.pop(0)

    print("\"" + unescape(tweet.text) + "\" from @" + tweet.user.screen_name, 
          "at", str(tweet.created_at), "UTC (" + str(len(tweets)), "left)")

    api.retweet(tweet.id)

while True:
    try:
        retweet()
        sleep(60 * 60)
    except tweepy.error.TweepError as e:
        print(e)
        sleep(15 * 60)
    except IndexError as e:      # in case the list of
        print("IndexError:", e)  # tweets is empty
        sleep(15 * 60)
    except Exception as e:
        print(e)
        raise


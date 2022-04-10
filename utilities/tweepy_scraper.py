"""
## Twitter Celebrity Matcher

This is a standalone script that scrapes tweets based on a given Twitter handle

Author: [Ahmed Shahriar Sakib](https://www.linkedin.com/in/ahmedshahriar)
Source: [Github](https://github.com/ahmedshahriar/TwitterCelebrityMatcher)
"""
import tweepy
import pandas as pd
import schedule
import time
import os
import glob

from dotenv import load_dotenv

load_dotenv()

access_key = os.environ.get("ACCESS_KEY")
access_secret = os.environ.get("ACCESS_SECRET")
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")

# screen_name="apotofvestiges"

# https://gist.github.com/mbejda/9c3353780270e7298763

handler_df = pd.read_csv("../celebrity-listing/Top-1000-Celebrity-Twitter-Accounts.csv", header=0)

#  list of accounts
# screen_names = handler_df.twitter.unique().tolist()

screen_names_all = handler_df.twitter.unique().tolist()
screen_names_parsed = [x.split('\\')[1].replace('.csv', '').strip() for x in glob.glob(
    "../twitter-celebrity-tweets-data/*.csv")]
# missing Twitter accounts to be parsed
screen_names = list(set(screen_names_all) - set(screen_names_parsed))
i = 0


def parser():
    try:
        print("\n\nstarting...")
        global screen_names
        global i
        print(i)
        name = screen_names[i]
        print(name)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        alltweets = []
        new_tweets = api.user_timeline(screen_name=name, count=200, tweet_mode="extended")
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        while len(new_tweets) > 0:
            print("getting tweets before %s" % (oldest))
            new_tweets = api.user_timeline(screen_name=name, count=200, max_id=oldest, tweet_mode="extended")
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1
            print("...%s tweets downloaded so far" % (len(alltweets)))

        out_tweets = [[tweet.id_str, tweet.created_at, tweet.full_text.encode("utf-8")] for tweet in alltweets]
        df = pd.DataFrame(out_tweets, columns=['twitter_id', 'date', 'tweet'])
        # dump tweets under dataset directory
        df.to_csv("../twitter-celebrity-tweets-data/%s.csv" % name, index=False)
        i = i + 1
        print(i)
    except Exception as e:
        print(e)
        i = i + 1
        pass


# Cron Job

parser()
# configure schedule job
schedule.every(5).seconds.do(parser)
# schedule.every(1).minutes.do(parser)
# schedule.every().hour.do(parser)
# schedule.every().day.at("23:19").do(parser)
# schedule.every().day.at("23:24").do(parser)
# schedule.every().day.at("23:30").do(parser)
# schedule.every().day.at("23:40").do(parser)
# schedule.every(5).to(10).minutes.do(parser)
# schedule.every().monday.do(parser)
# schedule.every().wednesday.at("13:15").do(parser)
# schedule.every().minute.at(":17").do(parser)


while len(screen_names) > i:
    schedule.run_pending()
    time.sleep(1)

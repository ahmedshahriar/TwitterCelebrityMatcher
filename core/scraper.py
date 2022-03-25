import logging
import os
from typing import Optional

import pandas as pd
import tweepy


class TwitterScraper:
    def __init__(self, consumer_key: str,
                 consumer_secret: str,
                 access_key: str, access_secret: str,
                 file_path: Optional[str] = None) -> None:
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret
        self.file_path = os.path.join(os.getcwd(), file_path) if file_path else None

    def scrape_tweets(self, screen_name: str) -> Optional[pd.DataFrame]:
        try:
            logging.info("\n\nstarting...")
            logging.info(screen_name)
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_key, self.access_secret)
            api = tweepy.API(auth)
            alltweets = []
            # Get the tweets
            new_tweets = api.user_timeline(screen_name=screen_name,
                                           count=200,
                                           tweet_mode="extended")
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1
            while len(new_tweets) > 0:
                logging.info("getting tweets before %s" % oldest)
                new_tweets = api.user_timeline(screen_name=screen_name,
                                               count=200,
                                               max_id=oldest,
                                               tweet_mode="extended")  # to get full texts/ No ellipsis
                alltweets.extend(new_tweets)
                oldest = alltweets[-1].id - 1
                logging.info("...%s tweets downloaded so far" % (len(alltweets)))

            out_tweets = [[tweet.id_str, tweet.created_at, tweet.full_text.encode("utf-8")] for tweet in alltweets]
            # Create a dataframe from the list of tweets
            return pd.DataFrame(out_tweets, columns=['twitter_id', 'date', 'tweet'])
        except Exception as e:
            logging.warning(e)

    def save_tweets(self, screen_name: str) -> None:
        df = self.scrape_tweets(screen_name)
        # Save the dataframe to a csv file
        df.to_csv(os.path.join(self.file_path, "%s.csv" % screen_name), index=False)

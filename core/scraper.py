"""
## Twitter Celebrity Matcher

This app is a tool to match celebrities from Twitter with their respective tweets.

Author: [Ahmed Shahriar Sakib](https://www.linkedin.com/in/ahmedshahriar)
Source: [Github](https://github.com/ahmedshahriar/TwitterCelebrityMatcher)
"""

import logging
import os
from typing import Optional, Union

import pandas as pd
import tweepy


class TwitterScraper:
    def __init__(self, consumer_key: Optional[str],
                 consumer_secret: Optional[str],
                 access_key: Optional[str],
                 access_secret: Optional[str],
                 file_path: Union[str, os.PathLike[str]] = None) -> None:
        """
        Initialize the scraper
        :param consumer_key:
        :param consumer_secret:
        :param access_key:
        :param access_secret:
        :param file_path:
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret
        self.file_path = os.path.join(os.getcwd(), file_path) if file_path else None
        # initialize the tweepy api
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(auth)

    def verify_tweepy_api(self) -> bool:
        """
        Verify if the tweepy api is working
        :return:
        """
        try:
            self.api.verify_credentials()
            return True
        except Exception as e:
            logging.error(e, exc_info=True)
            return False

    def check_user(self, screen_name: str) -> bool:
        """
        Check if a user exists
        :param screen_name:
        :return:
        """
        try:
            # NB : pass keyword argument `screen_name` to get_user()
            self.api.get_user(screen_name=screen_name)
            return True
        except Exception as e:
            logging.error(e, exc_info=True)
            return False

    def scrape_tweets(self, screen_name: str) -> Optional[pd.DataFrame]:
        """
        Scrape the tweets from a Twitter user
        :param screen_name:
        :return:
        """
        try:
            logging.info("\n\nstarting...")
            logging.info(screen_name)
            alltweets = []
            # Get the tweets
            # use tweet_mode="extended" to get the entire untruncated text of the Tweet
            # more here - https://docs.tweepy.org/en/stable/extended_tweets.html
            new_tweets = self.api.user_timeline(screen_name=screen_name,
                                                count=200,
                                                tweet_mode="extended")
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1
            while len(new_tweets) > 0:
                logging.info("getting tweets before %s" % oldest)
                new_tweets = self.api.user_timeline(screen_name=screen_name,
                                                    count=200,
                                                    max_id=oldest,
                                                    tweet_mode="extended")
                alltweets.extend(new_tweets)
                oldest = alltweets[-1].id - 1
                logging.info("...%s tweets downloaded so far" % (len(alltweets)))

            out_tweets = [[tweet.id_str, tweet.created_at, tweet.full_text.encode("utf-8")] for tweet in alltweets]
            # Create a dataframe from the list of tweets
            df = pd.DataFrame(out_tweets, columns=['twitter_id', 'date', 'tweet'])
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
        else:
            return df

    def save_tweets(self, screen_name: str) -> None:
        """
        Save the tweets to a csv file
        :param screen_name:
        :return:
        """
        df = self.scrape_tweets(screen_name)
        # Save the dataframe to a csv file
        if df:
            df.to_csv(os.path.join(self.file_path, "%s.csv" % screen_name), index=False)

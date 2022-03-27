"""
## Twitter Celebrity Matcher

This app is a tool to match celebrities from Twitter with their respective tweets.

Author: [Ahmed Shahriar Sakib](https://www.linkedin.com/in/ahmedshahriar)
Source: [Github](https://github.com/ahmedshahriar/TwitterCelebrityMatcher)
"""

import logging
import os
from typing import Mapping, Optional

import pandas as pd

from core.dataprep import TwitterDataPrep
from core.scraper import TwitterScraper

from config import CONSUMER_KEY, ACCESS_SECRET, CONSUMER_SECRET, ACCESS_KEY, MODEL_PATH, TWITTER_USER_LIST_FILE


def scrape_embed_tweets(username: str) -> Optional[pd.DataFrame]:
    """
    Scrape tweets and generate embedding dataframe
    :param username: Twitter username
    :return:
    """
    df_embeddings = pd.DataFrame()
    # Create a TwitterScraper object for tweepy
    twitter_scraper = TwitterScraper(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
                                     access_key=ACCESS_KEY,
                                     access_secret=ACCESS_SECRET)
    twitter_data_prep = TwitterDataPrep(model_path=MODEL_PATH)
    try:
        # Get the tweets of the user
        df = twitter_scraper.scrape_tweets(username)
        if type(df) is pd.DataFrame:
            df = twitter_data_prep.preprocess_data(df)
            df = twitter_data_prep.get_embeddings(df)
            temp_df = twitter_data_prep.process_embedding_data(df, username)
            # merge embedding and username
            df_embeddings = pd.concat([df_embeddings, temp_df], ignore_index=True)
    except Exception as e:
        logging.error(e)
        # return e

    return df_embeddings


def username_dict() -> Mapping:
    """
    Generate a dictionary of usernames
    :return:
    """
    df_list = pd.read_csv(os.path.join(os.getcwd(), TWITTER_USER_LIST_FILE), header=0) # + os.sep + os.pardir for current dir
    return pd.Series(df_list.name.values, index=df_list.twitter).to_dict()

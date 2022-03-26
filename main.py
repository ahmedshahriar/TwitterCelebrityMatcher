import logging
import os
import time

import pandas as pd

from app.app import App
from config import (DATA_PATH, CONSUMER_KEY, ACCESS_SECRET, CONSUMER_SECRET,
                    ACCESS_KEY, EMBED_DATA_PATH, MODEL_PATH, TWITTER_USER_LIST_FILE)
from core.dataprep import TwitterDataPrep
from core.matcher import TwitterUserMatcher
from core.scraper import TwitterScraper
from core.utils import username_dict


def fetch_users():
    # Get the Twitter account names
    handler_df = pd.read_csv(TWITTER_USER_LIST_FILE, header=0)
    screen_names = handler_df.twitter.unique().tolist()
    return screen_names


def tweepy_scraper(twitter_scraper: TwitterScraper, screen_names: list) -> None:
    if not os.path.exists(os.path.join(os.getcwd(), DATA_PATH)):
        os.mkdir(os.path.join(os.getcwd(), DATA_PATH))

    for c, screen_name in enumerate(screen_names, 1):
        twitter_scraper.save_tweets(screen_name)
        logging.info(f"#{c} {screen_name} tweets scraped")
        time.sleep(3)


def data_preparation():
    if not os.path.exists(os.path.join(os.getcwd(), EMBED_DATA_PATH)):
        os.mkdir(os.path.join(os.getcwd(), EMBED_DATA_PATH))
    twitter_data_prep = TwitterDataPrep(model_path=MODEL_PATH, data_path=DATA_PATH, embed_data_path=EMBED_DATA_PATH)
    twitter_data_prep.load_data()


def set_config():
    logging.basicConfig(encoding='utf-8',
                        level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[
                            logging.FileHandler("debug.log"),
                            logging.StreamHandler()
                        ])


def main():
    set_config()

    # Create a TwitterScraper object for tweepy
    # twitter_scraper = TwitterScraper(consumer_key=CONSUMER_KEY,
    #                                  consumer_secret=CONSUMER_SECRET,
    #                                  access_key=ACCESS_KEY,
    #                                  access_secret=ACCESS_SECRET,
    #                                  file_path=DATA_PATH)

    # check the Twitter user
    # twitter_scraper.check_user(screen_name='aaaaaaaaaaaaaaaaaaaaaaa')

    # fetch Twitter usernames
    # screen_names = fetch_users()

    # scrape tweets using tweepy
    # tweepy_scraper(twitter_scraper, screen_names)

    # generate vector embeddings
    # data_preparation()

    # Twitter profile matcher
    # matcher = TwitterUserMatcher(EMBED_DATA_PATH)

    # Get the Twitter account names dictionary
    # usernames_dict = username_dict()

    """match users from celebrity dataset"""
    # match two random users
    # usernames, similarity_score = matcher.match_single_user(random_state=43)

    # match one user by username with another random user
    # random_state=43 returns `Schwarzenegger` xD
    # usernames, similarity_score = matcher.match_single_user('Schwarzenegger', random_state=43)

    # match two users by their twitter handlers
    # usernames, similarity_score = matcher.match_single_user('Schwarzenegger', 'RobertDowneyJr', random_state=43)

    """match unknown users"""
    # match with an unknown user with another random user from the celebrity dataset
    # usernames, similarity_score = matcher.match_single_user('ahmed__shahriar', random_state=43)

    # match with two unknown users
    # usernames, similarity_score = matcher.match_single_user('ahmed__shahriar', 'Comicstorian', random_state=43)

    # print the results
    # print(f"Similarity between {usernames[0]} and {usernames[1]} is: {similarity_score * 100:.2f}%")

    """match top users for a single user"""
    # match with a single user from celebrity dataset
    # username = 'RobertDowneyJr'

    # match with a single user excluding celebrity dataset
    # username = 'ahmed__shahriar'

    # top_n = 10
    # top_results = matcher.match_top_users(username) # returns a zip object

    # for k, v in sorted(top_results, key=lambda item: item[1], reverse=True)[1:top_n+1]:
    #     print(f"Twitter username: {k} ({usernames_dict.get(k)}): {v}")


if __name__ == '__main__':
    # main()
    App().render()
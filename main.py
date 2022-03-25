import logging
import os
import time

import pandas as pd

from config import (DATA_PATH, CONSUMER_KEY, ACCESS_SECRET, CONSUMER_SECRET,
                    ACCESS_KEY, EMBED_DATA_PATH, MODEL_PATH, TWITTER_USER_LIST_FILE)
from core.dataprep import TwitterDataPrep
from core.matcher import TwitterUserMatcher
from core.scraper import TwitterScraper


def tweepy_scraper(screen_names: list) -> None:
    if not os.path.exists(os.path.join(os.getcwd(), DATA_PATH)):
        os.mkdir(os.path.join(os.getcwd(), DATA_PATH))

    # Create a TwitterScraper object for tweepy
    twitter_scraper = TwitterScraper(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_key=ACCESS_KEY,
                                     access_secret=ACCESS_SECRET, file_path=DATA_PATH)
    for c, screen_name in enumerate(screen_names, 1):
        twitter_scraper.save_tweets(screen_name)
        logging.info(f"#{c} {screen_name} tweets scraped")
        time.sleep(3)


def fetch_users():
    # Get the Twitter account names
    handler_df = pd.read_csv(TWITTER_USER_LIST_FILE, header=0)
    screen_names = handler_df.twitter.unique().tolist()
    return screen_names


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

    # fetch Twitter usernames
    # screen_names = fetch_users()

    # scrape tweets using tweepy
    # tweepy_scraper(screen_names)

    # generate vector embeddings
    # data_preparation()

    # Twitter profile matcher
    # matcher = TwitterUserMatcher(EMBED_DATA_PATH)

    """match users from celebrity dataset"""
    # match two random users
    # print(matcher.match_random_user(random_state=43))

    # match one user by username with another random user
    # print(matcher.match_random_user('Schwarzenegger', random_state=43))  # random_state=43 returns `Schwarzenegger` xD

    # match two users by their usernames
    # print(matcher.match_random_user('Schwarzenegger', 'RobertDowneyJr', random_state=43))

    """match unknown users"""
    # match with an unknown user with another random user from the celebrity dataset
    # print(matcher.match_random_user('ahmed__shahriar', random_state=43))

    # match with two unknown users
    # print(matcher.match_users('ahmed__shahriar', 'Comicstorian', random_state=43))


if __name__ == '__main__':
    main()

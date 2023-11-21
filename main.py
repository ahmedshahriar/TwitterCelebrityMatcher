import logging
import os
import time

import pandas as pd
import uvicorn

from api.api import app  # import fastAPI app
from app.app import App
from config import (DATA_PATH, CONSUMER_KEY, ACCESS_SECRET, CONSUMER_SECRET, ACCESS_KEY,
                    EMBED_DATA_PATH, MODEL_PATH, TWITTER_USER_LIST_PATH, TWITTER_USER_LIST_FILE)
from core.dataprep import TwitterDataPrep
from core.matcher import TwitterUserMatcher
from core.scraper import TwitterScraper
from core.utils import username_dict


def set_config() -> None:
    logging.basicConfig(encoding='utf-8',
                        level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[
                            logging.FileHandler("debug.log"),
                            logging.StreamHandler()
                        ])


def fetch_users() -> list:
    # Get the Twitter account names
    handler_df = pd.read_csv(os.path.join(os.getcwd(), TWITTER_USER_LIST_PATH, TWITTER_USER_LIST_FILE), header=0)
    screen_names = handler_df.twitter_username.unique().tolist()
    return screen_names


# scraper
def twitter_scraper_users(twitter_scraper: TwitterScraper, screen_names: list) -> None:
    # create a directory for the scraped data if not exists
    if not os.path.exists(os.path.join(os.getcwd(), DATA_PATH)):
        os.mkdir(os.path.join(os.getcwd(), DATA_PATH))

    # scrape the data from the Twitter username list
    for c, screen_name in enumerate(screen_names, 1):
        twitter_scraper.save_tweets(screen_name)
        logging.info(f"#{c} {screen_name} tweets scraped")
        time.sleep(3)


def scrape_celebrity_tweets(twitter_scraper: TwitterScraper) -> None:
    # check the Twitter user
    twitter_scraper.check_user_twiiter(screen_name='BarackObama')  # check an invalid user by Twitter handle

    # fetch Twitter usernames
    screen_names = fetch_users()

    # scrape all users' tweets and save them in the data folder as CSV files
    twitter_scraper_users(twitter_scraper, screen_names)


def scraper_in_action(twitter_scraper: TwitterScraper) -> None:
    # verify Twitter API credentials
    twitter_scraper.verify_tweepy_api()

    # check a Twitter username
    twitter_scraper.check_user_twiiter(screen_name='BarackObama')

    # fetch Twitter display name by Twitter handle
    twitter_scraper.fetch_profile_name(screen_name='kingjames')  # with or without `@` prefix

    # scrape tweets and export to csv by Twitter handle
    twitter_scraper.scrape_tweets(screen_name='elonmusk')


# data preparation
def data_preparation(twitter_data_prep: TwitterDataPrep) -> None:
    # preprocess the tweets, generate embeddings and save them in a single CSV file
    twitter_data_prep.load_data()


# twitter_user_matcher
def matcher_in_action(twitter_user_matcher: TwitterUserMatcher, usernames_dict) -> None:
    """match users from celebrity dataset"""
    # match two random users
    # random_state=43 returns `Schwarzenegger` xD
    usernames, similarity_score = twitter_user_matcher.match_twitter_user(random_state=43)

    # match one user by username with another random user
    # random_state=44 returns `EvaLongoria`
    usernames, similarity_score = twitter_user_matcher.match_twitter_user('Schwarzenegger', random_state=44)

    # match two users by their twitter handlers
    usernames, similarity_score = twitter_user_matcher.match_twitter_user('Schwarzenegger', 'RobertDowneyJr',
                                                                          random_state=43)

    """match unknown users"""
    # match with an unknown user with another random user from the celebrity dataset
    usernames, similarity_score = twitter_user_matcher.match_twitter_user('ahmed__shahriar', random_state=43)

    # match with two unknown users
    usernames, similarity_score = twitter_user_matcher.match_twitter_user('ahmed__shahriar', 'Comicstorian',
                                                                          random_state=43)

    # print the results
    print(f"Similarity between {usernames[0]} and {usernames[1]} is: {similarity_score * 100:.4f}%")

    """match top users for a single user"""
    # match with a single user from celebrity dataset
    username = 'RobertDowneyJr'

    # match with a single user excluding celebrity dataset
    username = 'ahmed__shahriar'

    top_n = 10
    top_results = twitter_user_matcher.match_top_celeb_users(username)  # returns a zip object

    for k, v in sorted(top_results, key=lambda item: item[1], reverse=True)[1:top_n + 1]:
        print(f"Twitter username: {k} ({usernames_dict.get(k)}): {v}")


def main() -> None:
    # create a TwitterScraper object for tweepy
    twitter_scraper = TwitterScraper(consumer_key=CONSUMER_KEY,
                                     consumer_secret=CONSUMER_SECRET,
                                     access_key=ACCESS_KEY,
                                     access_secret=ACCESS_SECRET,
                                     file_path=DATA_PATH)

    """scraper functionalities"""
    # scrape all the celebrity tweets
    scrape_celebrity_tweets(twitter_scraper=twitter_scraper)

    # twitter scraper functionalities
    scraper_in_action(twitter_scraper)

    """data preparation"""
    # create a data preparation object
    twitter_data_prep = TwitterDataPrep(model_path=MODEL_PATH, data_path=DATA_PATH, embed_data_path=EMBED_DATA_PATH)

    # save a single file containing all the generated vector embeddings per user
    data_preparation(twitter_data_prep=twitter_data_prep)

    """twitter user matcher"""
    # create Twitter profile matcher object
    matcher = TwitterUserMatcher(EMBED_DATA_PATH)

    # get the Twitter account names dictionary
    usernames_dict = username_dict()

    # twitter matcher functionalities
    matcher_in_action(matcher, usernames_dict)


if __name__ == '__main__':
    # set the configuration
    set_config()
    # run the main function
    # main()
    App().render()  # run the streamlit app
    # run fast API
    # uvicorn.run("__main__:app", host='127.0.0.1', log_level="info", reload=True, debug=True, port=8000)

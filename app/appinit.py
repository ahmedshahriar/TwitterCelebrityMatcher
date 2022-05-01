"""
## Twitter Celebrity Matcher - Streamlit App

This app is a tool to match celebrities from Twitter with their respective tweets.

This is a helper class that initializes the core objects - scraper and matcher.
Author: [Ahmed Shahriar Sakib](https://www.linkedin.com/in/ahmedshahriar)
Source: [Github](https://github.com/ahmedshahriar/TwitterCelebrityMatcher)
"""

from app.appdata import AppData
from core.matcher import TwitterUserMatcher
from core.scraper import TwitterScraper


class AppInit:
    def __init__(self, data: AppData) -> None:
        self.data = data

    def init_twitter_scraper(self) -> TwitterScraper:
        """
        Initialize the Twitter scraper object
        :return:
        """
        return TwitterScraper(consumer_key=self.data.consumer_key, consumer_secret=self.data.consumer_secret,
                              access_key=self.data.access_key, access_secret=self.data.access_secret)

    def init_twitter_user_matcher(self) -> TwitterUserMatcher:
        """
        Initialize the Twitter user twitter_user_matcher object
        :return:
        """
        return TwitterUserMatcher(embed_data_path=self.data.embed_data_path)

"""
## Twitter Celebrity Matcher - Streamlit App

This app is a tool to match celebrities from Twitter with their respective tweets.

This is a helper class that contains all the configuration variables and utilities that is used in the app.

Author: [Ahmed Shahriar Sakib](https://www.linkedin.com/in/ahmedshahriar)
Source: [Github](https://github.com/ahmedshahriar/TwitterCelebrityMatcher)
"""

from dataclasses import dataclass
from typing import Optional
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, EMBED_DATA_PATH, TWITTER_USER_LIST_FILE, TWITTER_USER_LIST_PATH
from core.utils import username_dict


# great intro https://youtu.be/vBH6GRJ1REM
@dataclass
class AppData:
    consumer_key: Optional[str] = CONSUMER_KEY
    consumer_secret: Optional[str] = CONSUMER_SECRET
    access_key: Optional[str] = ACCESS_KEY
    access_secret: Optional[str] = ACCESS_SECRET
    twitter_user_list_file: str = TWITTER_USER_LIST_FILE
    twitter_user_list_path: str = TWITTER_USER_LIST_PATH
    embed_data_path: str = EMBED_DATA_PATH
    usernames_dict = username_dict()

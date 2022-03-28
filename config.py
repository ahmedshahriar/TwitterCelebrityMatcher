import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY: Optional[str] = os.environ.get("ACCESS_KEY")
ACCESS_SECRET: Optional[str] = os.environ.get("ACCESS_SECRET")
CONSUMER_KEY: Optional[str] = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET: Optional[str] = os.environ.get("CONSUMER_SECRET")

# folder path
DATA_PATH = 'twitter-data'  # path to save tweets for each user
EMBED_DATA_PATH = 'twitter-celebrity-embed-data'  # path to save embedding data
MODEL_PATH = 'models'  # path to save/load models

# user listing path
TWITTER_USER_LIST_PATH = 'celebrity-listing'
# user listing file
TWITTER_USER_LIST_FILE = 'Top-1000-Celebrity-Twitter-Accounts.csv'

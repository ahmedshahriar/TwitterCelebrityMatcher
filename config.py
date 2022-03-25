import os

from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.environ.get("ACCESS_KEY")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")

# folder path
DATA_PATH = 'twitter-data'  # path to save tweets for each user
EMBED_DATA_PATH = 'twitter-embed-data'  # path to save embedding data
MODEL_PATH = 'models'  # path to save/load models

# user listing file
TWITTER_USER_LIST_FILE = 'celebrity-listing/Top-1000-Celebrity-Twitter-Accounts.csv'

import logging
import os.path

import numpy as np
import pandas as pd
from sentence_transformers import util

from core import utils


class TwitterUserMatcher:
    def __init__(self, embed_data_path: str) -> None:
        self.embed_data = pd.read_csv(os.path.join(os.getcwd(), embed_data_path, embed_data_path + '.csv'))

    def match_users(self, *args, random_state=None) -> str:
        try:
            if len(args) == 0:
                random_users_df = self.embed_data.sample(n=2, random_state=random_state)
            elif len(args) == 1:
                if args[0] in self.embed_data.username.values:
                    random_users_df = pd.concat(
                        [self.embed_data[self.embed_data.username == args[0]],
                         self.embed_data.sample(random_state=random_state)])
                else:
                    random_users_df = pd.concat(
                        [utils.scrape_user_tweets(args[0]), self.embed_data.sample(random_state=random_state)])
            else:
                random_users_df = pd.concat(
                    [self.embed_data[self.embed_data.username == args[0]]
                     if args[0] in self.embed_data.username.values
                     else utils.scrape_user_tweets(args[0]),

                     self.embed_data[self.embed_data.username == args[1]]
                     if args[1] in self.embed_data.username.values
                     else utils.scrape_user_tweets(args[1])
                     ])
            usernames = random_users_df.username.values
            similarity_score = util.cos_sim(random_users_df.iloc[:, 1:].values[0], random_users_df.iloc[:, 1:].values[1])
            return f"Similarity between {usernames[0]} and {usernames[1]} is: {np.squeeze(similarity_score) * 100:.2f}%"
        except Exception as e:
            logging.error(e)





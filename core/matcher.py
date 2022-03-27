"""
## Twitter Celebrity Matcher

This app is a tool to match celebrities from Twitter with their respective tweets.

Author: [Ahmed Shahriar Sakib](https://www.linkedin.com/in/ahmedshahriar)
Source: [Github](https://github.com/ahmedshahriar/TwitterCelebrityMatcher)
"""

import logging
import os

import numpy as np
import pandas as pd
from sentence_transformers import util

from core import utils


class TwitterUserMatcher:
    def __init__(self, embed_data_path: str) -> None:
        """
        :param embed_data_path: celebrity user embedding data path
        """
        self.embed_data = pd.read_csv(os.path.join(os.getcwd(), embed_data_path, embed_data_path + '.csv'))

    def match_twitter_user(self, *args, random_state=None) -> tuple:
        """
        returns users with the cosine similarity score
        :param args: twitter usernames Optional
        :param random_state:
        :return:
        """
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
                        [utils.scrape_embed_tweets(args[0]), self.embed_data.sample(random_state=random_state)])
            else:
                random_users_df = pd.concat(
                    [self.embed_data[self.embed_data.username == args[0]]
                     if args[0] in self.embed_data.username.values
                     else utils.scrape_embed_tweets(args[0]),

                     self.embed_data[self.embed_data.username == args[1]]
                     if args[1] in self.embed_data.username.values
                     else utils.scrape_embed_tweets(args[1])
                     ])
            usernames = random_users_df.username.values
            similarity_score = util.cos_sim(random_users_df.iloc[:, 1:].values[0],
                                            random_users_df.iloc[:, 1:].values[1])
            return usernames, np.squeeze(similarity_score)

        except Exception as e:
            logging.error(e)

    def match_top_celeb_users(self, username) -> zip:
        """
        returns a list of the top users with the highest cosine similarity score to the given user
        :param username:
        :return:
        """
        try:
            if username in self.embed_data.username.values:
                user_df = self.embed_data[self.embed_data.username == username]
            else:
                user_df = utils.scrape_embed_tweets(username)

            # handle RuntimeError: expected scalar type Double but found Float
            # https://github.com/pytorch/pytorch/issues/2138
            cos_sim_results = np.squeeze(
                util.cos_sim(user_df.iloc[:, 1:].values.astype(np.float32),
                             self.embed_data.iloc[:, 1:].values.astype(np.float32)).numpy())

            top_user_dict = zip(self.embed_data.iloc[:, 0], cos_sim_results)
            return top_user_dict
        except Exception as e:
            logging.error(e)

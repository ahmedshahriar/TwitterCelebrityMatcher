"""
## Twitter Celebrity Matcher

This app is a tool to match celebrities from Twitter with their respective tweets.

Author: [Ahmed Shahriar Sakib](https://www.linkedin.com/in/ahmedshahriar)
Source: [Github](https://github.com/ahmedshahriar/TwitterCelebrityMatcher)
"""

import ast
import json
import logging
import os
import re
import sys
from operator import itemgetter
from pathlib import Path
from typing import Optional, Union

import demoji
import numpy.typing as npt
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer


class TwitterDataPrep:
    def __init__(self, model_path: str, data_path: Union[str, os.PathLike[str]] = None,
                 embed_data_path: Union[str, os.PathLike[str]] = None) -> None:
        """
        Initialize the class.
        :param data_path:
        :param model_path:
        :param embed_data_path:
        """
        self.model_path = model_path
        self.data_path = data_path
        self.embed_data_path = embed_data_path
        self.error_list: list[Optional[str]] = []

        # download and save the model
        # https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
        # model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        # model.save(model_path)
        if not os.path.exists(os.path.join(os.getcwd(), embed_data_path)):
            os.mkdir(os.path.join(os.getcwd(), embed_data_path))
        if not os.path.exists(os.path.join(os.getcwd(), model_path)):
            os.mkdir(os.path.join(os.getcwd(), model_path))
        if model_path and len(os.listdir(model_path)) != 0:
            self.model = SentenceTransformer(model_path)
        else:
            self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        if torch.cuda.is_available():
            self.model = self.model.to(torch.device("cuda"))
        # self.model = SentenceTransformer(model_path, device='cuda')  # remove cuda if not available
        emoticon_data_folder = Path("utilities/")
        emoticon_file_path = emoticon_data_folder / "emoticon_dict.json"
        with open(emoticon_file_path) as f:
            self.emoticons_dict = json.load(f)

    def clean_text(self, text: str) -> str:
        """
        Clean the tweets in a basic way.
        :param text:
        :return: text
        """
        pat1 = r'@[^ ]+'  # remove username @
        pat2 = r'https?://[A-Za-z0-9./]+'  # remove urls
        pat3 = r'\'s'  # remove apostrophe todo: check if it is necessary for the model
        pat4 = r'\#\w+'  # remove hashtag
        pat5 = r'&amp '  # remove unicode `&`
        # pat6 = r"[\n\t]*" # r'[^A-Za-z\s]'
        pat7 = r'RT'  # remove RT / retweet
        pat8 = r'www\S+'  # remove link www
        combined_pat = r'|'.join((pat1, pat2, pat3, pat4, pat5, pat7, pat8))  # combine all patterns
        text = re.sub(combined_pat, "", text)  # .lower()
        text = re.sub(r'\s+', ' ', text)  # remove extra spaces
        return text.strip()

    def _parse_bytes(self, field: Union[str, ast.AST]) -> Union[str, ast.AST]:
        """ Convert string represented in Python byte-string literal syntax into a
        decoded character string. Other field types returned unchanged.
        :param field: string or bytestring
        :return: string
        """

        result = field
        try:
            result = ast.literal_eval(field)
        finally:
            return result.decode() if isinstance(result, bytes) else field

    def replace_emoticons(self, text) -> str:
        """
        Replace emoticons in the text with their corresponding word.
        :param text:
        :return:
        """
        for emoticon, context in self.emoticons_dict.items():
            text = text.replace(emoticon, ' ' + context + ' ')
            text = re.sub(' +', ' ', text)
        return text

    def replace_emojis(self, text: str) -> str:
        """
        Replace emojis in the text with their corresponding word using demoji.
        :param text:
        :return:
        """
        for emoji, context in demoji.findall(text).items():
            text = text.replace(emoji, ' ' + context + ' ')
            text = re.sub(' +', ' ', text)
        return text

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the tweets.
        :param df: dataframe
        :return: dataframe
        """
        logging.info('Preprocessing data...')
        # open encoded file
        df['tweet'] = df['tweet'].apply(self._parse_bytes)
        # normalize the text
        # df['tweet'] = df['tweet'].map(lambda x:BeautifulSoup(x, "html").get_text(strip=True))
        df['tweet'] = df['tweet'].str.normalize('NFKD')
        # clean the text
        df['tweet'] = df['tweet'].map(self.clean_text)

        # .str.encode('ascii', 'ignore').str.decode('utf-8')

        # replace emoticons with custom dictionary
        # df['tweet'].replace(emoticon_dict_escape, regex=True, method='pad') # to use regex with replace method
        df['tweet'] = df['tweet'].apply(lambda x: self.replace_emoticons(x))
        # replace emojis
        df['tweet'] = df['tweet'].apply(lambda x: self.replace_emojis(x))
        logging.info('Preprocessing done.')
        return df

    def get_embeddings(self, twitter_data: pd.DataFrame) -> Optional[npt.NDArray]:
        """
        Get the embeddings of the tweets.
        :param twitter_data:
        :return: embeddings
        """
        vectors = self.model.encode(twitter_data.tweet)
        return vectors.mean(axis=0)

    def process_embedding_data(self, embeddings: Optional[npt.NDArray], username: str) -> pd.DataFrame:
        """
        Process the embeddings.
        :param username:
        :param embeddings:
        :return:
        """
        # create a temporary dataframe to split embeddings
        temp_df = pd.DataFrame({"emb": [embeddings]})
        # indices range for embeddings
        indices = range(len(temp_df['emb'][0]))
        # split embedding values into individual columns
        # https://stackoverflow.com/a/63198715/11105356
        temp_df = temp_df['emb'].transform({f'v{i + 1}': itemgetter(i) for i in indices})
        # insert username at the first column
        temp_df.insert(0, 'username', username)
        return temp_df

    def load_data(self) -> None:
        """
        Dump the generated embeddings to a csv file.
        :return:
        """
        df_embeddings = pd.DataFrame()
        logging.info(f"Loading data from the folder...{self.data_path}")
        count = 1
        # check file in subdirectory
        for root, dirs, files in os.walk(os.path.join(os.getcwd(), self.data_path)):
            dirs.sort(key=str)
            files.sort(key=str)
            for file in files:
                # folder_name = os.path.basename(root)
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    try:
                        # get username from csv file names
                        username = re.sub(r'\.csv$', '', file)
                        logging.info(f"User: {username}")
                        # read the data
                        df = pd.read_csv(file_path)
                        # preprocess the data
                        data = self.preprocess_data(df)
                        # get the embeddings
                        embeddings = self.get_embeddings(data)

                        temp_df = self.process_embedding_data(embeddings, username)
                        # merge embedding and username
                        df_embeddings = pd.concat([df_embeddings, temp_df], ignore_index=True)

                        logging.info(f"{count} user(s) processed.")
                        count += 1
                    except IndexError as ie:
                        logging.exception(f"{ie}")
                        # file names which contains exceptions
                        self.error_list.append(file)
                        logging.info(f"Unexpected error: {sys.exc_info()[0]}")
                        self.error_list.append(str(sys.exc_info()[0]))

        # dump the data to a csv file
        df_embeddings.to_csv(os.path.join(os.getcwd(), self.embed_data_path, "%s.csv" % self.embed_data_path),
                             index=False)
        logging.warning(f"Error list: {self.error_list}")
        logging.info(
            f"Data saved to {os.path.join(os.getcwd(), self.embed_data_path, '%s.csv' % self.embed_data_path)}")

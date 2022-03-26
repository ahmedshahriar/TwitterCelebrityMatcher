import random
from dataclasses import dataclass

import pandas as pd
import streamlit as st

from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, EMBED_DATA_PATH
from core.matcher import TwitterUserMatcher
from core.scraper import TwitterScraper
from core.utils import username_dict


# great intro https://youtu.be/vBH6GRJ1REM
@dataclass
class AppData:
    consumer_key: str = CONSUMER_KEY
    consumer_secret: str = CONSUMER_SECRET
    access_key: str = ACCESS_KEY
    access_secret: str = ACCESS_SECRET
    embed_data_path: str = EMBED_DATA_PATH
    usernames_dict = username_dict()


class AppInit:

    def __init__(self, data: AppData):
        self.data = data

    def init_twitter_scraper(self):
        return TwitterScraper(consumer_key=self.data.consumer_key, consumer_secret=self.data.consumer_secret,
                              access_key=self.data.access_key, access_secret=self.data.access_secret)

    def init_matcher(self):
        return TwitterUserMatcher(embed_data_path=self.data.embed_data_path)


class AppHome:

    def __init__(self, app):
        self.app = app

    @property
    def usernames_dict(self):
        return self.app.data.usernames_dict

    @property
    def twitter_scraper(self):
        return self.app.init.init_twitter_scraper()

    @property
    def twitter_user_matcher(self):
        return self.app.init.init_matcher()

    @property
    def random_suggested_usernames(self):
        random.seed(15)
        return random.sample(self.usernames_dict.keys(), 5)

    def render_select_user(self):
        st.session_state.username = st.selectbox("Select a celebrity:", self.usernames_dict.keys())

    def render_suggested_users(self):
        st.markdown("Or Try one of these users:")
        columns = st.columns(len(self.random_suggested_usernames))
        for col, user in zip(columns, self.random_suggested_usernames):
            with col:
                if st.button(user):
                    st.session_state.username = user

    def render_search_form(self):
        st.markdown("Or Enter a username:")
        with st.form("search_form"):
            if st.session_state.get('username'):
                st.session_state.username = st.text_input("Username", value=st.session_state.username.strip())
            else:
                st.session_state.username = st.text_input("Username")
            return st.form_submit_button("Search")

    def render_search_results(self):
        top_n = 100
        username = st.session_state.username.strip()
        with st.spinner("Searching for " + username):
            is_exists = self.twitter_scraper.check_user(username)
        if not is_exists:
            return st.markdown("This twitter user does not exist or some error occurred!")
        with st.spinner("Found user, searching for matches..."):
            closest_list = self.twitter_user_matcher.match_top_users(username)
        results = sorted(closest_list, key=lambda item: item[1], reverse=True)[1:top_n + 1]
        result_df = pd.DataFrame(results, columns=['Twitter Username', 'Similarity Score'])
        result_df.insert(1, 'Name', result_df['Twitter Username'].map(lambda x: self.usernames_dict.get(x)))
        result_df['Similarity Score'] = result_df['Similarity Score'].map(lambda x: round(x, 4))
        st.dataframe(result_df)

    def render(self):
        self.render_select_user()
        self.render_suggested_users()

        submitted = self.render_search_form()
        if submitted:
            self.render_search_results()


class App:
    title = "Twitter Celebrity Matcher"
    description = "This app is a tool to match celebrities from Twitter with their respective tweets."
    author = "Ahmed Shahriar Sakib"
    version = "1.0.0"

    def __init__(self):
        self.data = AppData()
        self.init = AppInit(self.data)

    def render(self):
        st.title(self.title)
        AppHome(self).render()

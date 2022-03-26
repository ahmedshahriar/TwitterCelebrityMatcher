import random
from dataclasses import dataclass

import streamlit as st

from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
from core.scraper import TwitterScraper
from core.utils import username_dict


# great intro https://youtu.be/vBH6GRJ1REM
@dataclass
class AppData:
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    access_key = ACCESS_KEY
    access_secret = ACCESS_SECRET
    usernames_dict = username_dict()


class AppInit:

    def __init__(self, data: AppData):
        self.data = data

    def init_twitter_scraper(self):
        return TwitterScraper(consumer_key=self.data.consumer_key, consumer_secret=self.data.consumer_secret,
                              access_key=self.data.access_key, access_secret=self.data.access_secret)


class AppHome:

    def __init__(self, app):
        self.app = app

    @property
    def usernames_dict(self):
        return self.app.data.usernames_dict

    @property
    def twitter_scraper(self):
        return self.app.init_twitter_scraper()

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
                st.session_state.username = st.text_input("Username", value=st.session_state.username)
            else:
                st.session_state.username = st.text_input("Username")
            return st.form_submit_button("Search")

    def render_search_results(self):
        username = st.session_state.username
        if username:
            st.markdown("## {}".format(username))
            # self.render_user_page(username)
        else:
            st.markdown("Please enter a username")

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
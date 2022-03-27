"""
## Twitter Celebrity Matcher

This app is a tool to match celebrities from Twitter with their respective tweets.

Author: [Ahmed Shahriar Sakib](https://www.linkedin.com/in/ahmedshahriar)
Source: [Github](https://github.com/ahmedshahriar/TwitterCelebrityMatcher)
"""
import logging
import random
from dataclasses import dataclass

import pandas as pd
import streamlit as st
from pandas import option_context

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

    def init_twitter_user_matcher(self):
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
        return self.app.init.init_twitter_user_matcher()

    @property
    def random_suggested_usernames(self):
        random.seed(15)  # will return ['gusttavo_lima' 'selenagomez' 'officialtulisa' 'drdre' 'Eminem']
        return random.sample(self.usernames_dict.keys(), 5)

    def capture_change_value(self):
        st.session_state.username = st.session_state.get('selected_username')

    def render_select_random_celebrity(self):
        # helpful link - https://github.com/streamlit/streamlit/issues/3601
        st.selectbox("Select a celebrity (twitter username) :", self.usernames_dict.keys(),
                     key='selected_username', on_change=self.capture_change_value)

    def render_suggested_users(self):
        st.markdown("Or Try one of these users:")
        random_celebrity_usernames = ['taylorswift13', 'Cristiano', 'BillGates',
                                      'coldplay', 'iamsrk', 'johngreen']
        # or use self.random_suggested_usernames
        columns = st.columns(len(random_celebrity_usernames))
        for col, user in zip(columns, random_celebrity_usernames):
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

    def render_top_search_results(self):
        # set the max results to 100
        top_n = 100
        username = st.session_state.username.strip()
        if len(username) == 0:
            return st.warning("The username can not be empty!")
        else:
            # check for username
            with st.spinner("Searching for " + username):
                is_exists = self.twitter_scraper.check_user(username)
            if not is_exists:
                return st.error("This twitter user does not exist or some error occurred!")

        # get the top n results
        with st.spinner("**Twitter User Found**! searching for matches..."):
            closest_list = self.twitter_user_matcher.match_top_celeb_users(username)

        # could be a user with no tweets
        if not closest_list:
            return st.error("An error occurred!")

        # sort the list by the similarity score
        # [1:] to remove the first item which is the username itself
        results = sorted(closest_list, key=lambda item: item[1], reverse=True)[1:top_n + 1]
        result_df = pd.DataFrame(results, columns=['Twitter Username', 'Similarity Score'])

        # show the Celebrity Names
        result_df.insert(1, 'Name', result_df['Twitter Username'].map(lambda x: self.usernames_dict.get(x)))
        # result_df['Similarity Score'] = result_df['Similarity Score'].map(lambda x: round(x, 4)) # no need

        # display the Twitter profile link
        result_df['Twitter link'] = result_df['Twitter Username'].map(lambda x: 'https://twitter.com/' + x)

        # display the top n results
        st.markdown(f"#### Top {top_n} Most Similar Celebrities For '[{username}](https://twitter.com/{username})' ({n if (n := self.usernames_dict.get(username)) else ''}):")

        # todo: display full text of the twitter link
        # more customization/ a possible option : https://github.com/PablocFonseca/streamlit-aggrid
        with option_context('display.max_colwidth', None):
            # result_df.style.set_properties(subset=['link'], **{'width': '900px'})
            # st.dataframe(result_df.style.set_precision(4)) # deprecated
            st.dataframe(result_df.style.format({'Similarity Score': '{:.4f}'}))

    def match_two_celeb_users(self):
        st.markdown("#### Match Two Celebrities From The List")
        celeb_usernames = st.multiselect("Select Two Celebrity (twitter username) :",
                                         self.usernames_dict.keys(),
                                         key='celeb_usernames',
                                         help='Click the box and start typing celebrity Twitter username')
        if len(celeb_usernames) != 2:
            return st.warning("Please select two celebrities!")
        else:
            # get the similarity score
            with st.spinner("Calculating the similarity score..."):
                try:
                    _, similarity_score = self.twitter_user_matcher.match_twitter_user(celeb_usernames[0], celeb_usernames[1])
                except Exception as e:
                    logging.info(e)
                    return st.error(f"An error occurred!")
            if similarity_score is None:
                return st.error("An error occurred!")
            else:
                st.success(
                    f"The similarity score between [{celeb_usernames[0]}](https://twitter.com/{celeb_usernames[0]}) "
                    f"and [{celeb_usernames[1]}](https://twitter.com/{celeb_usernames[1]}) is: "
                    f"**{similarity_score:.4f}**")

    def match_two_users(self):
        st.markdown("#### Match Two Twitter Users")
        user1 = st.text_input('Select Twitter User1', 'BarackObama').strip()
        user2 = st.text_input('Select Twitter User2', 'BorisJohnson').strip()

        if len(user1) == 0 or len(user2) == 0:
            return st.warning("Usernames can not be empty!")
        if user1 == user2:
            return st.warning("Please select two different users!")

        if st.button('Check Similarity'):
            if len(user1) > 0 and len(user2) > 0:
                # get the similarity score
                with st.spinner("Calculating the similarity score... Please wait..."):
                    try:
                        _, similarity_score = self.twitter_user_matcher.match_twitter_user(user1, user2)
                    except Exception as e:
                        logging.info(e)
                        return st.error(f"An error occurred!")
                if similarity_score is None:
                    return st.error("An error occurred!")
                else:
                    st.success(
                        f"The similarity score between [{user1}](https://twitter.com/{user1}) "
                        f"and [{user2}](https://twitter.com/{user2}) is: "
                        f"**{similarity_score:.4f}**")

    def render(self):
        st.subheader("Most Similar Twitter Celebrities")
        self.render_select_random_celebrity()
        self.render_suggested_users()

        submitted = self.render_search_form()
        if submitted:
            self.render_top_search_results()

        st.subheader("Match 1v1 Twitter Users")
        self.match_two_celeb_users()

        self.match_two_users()


class App:
    title = "Twitter Celebrity Matcher"
    description = "This app is a tool to match celebrities from Twitter with their respective tweets."
    author = "Ahmed Shahriar Sakib"
    version = "1.0.0"

    def __init__(self):
        self.data = AppData()
        self.init = AppInit(self.data)

    def set_config(self):
        st.set_page_config(
            page_title="Twitter Celebrity Matcher",
            menu_items={
                'About': "# This is a header. This is an *extremely* cool app!"
            }
        )

    def render(self):
        self.set_config()
        st.header(self.title)
        AppHome(self).render()

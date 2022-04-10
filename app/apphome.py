"""
## Twitter Celebrity Matcher - Streamlit App

This app is a tool to match celebrities from Twitter with their respective tweets.
This script contains the core functionalities of the app.

Author: [Ahmed Shahriar Sakib](https://www.linkedin.com/in/ahmedshahriar)
Source: [Github](https://github.com/ahmedshahriar/TwitterCelebrityMatcher)
"""

import logging
import random

import pandas as pd
import streamlit as st
from pandas import option_context

from core.matcher import TwitterUserMatcher
from core.scraper import TwitterScraper
from core.utils import lower_dict


class AppHome:
    # set the max results to 100
    top_n = 100

    def __init__(self, app) -> None:
        self.app = app

    @property
    def usernames_dict(self) -> dict:
        """
        Get the usernames dictionary
        :return:
        """
        return self.app.data.usernames_dict

    @property
    def twitter_scraper(self) -> TwitterScraper:
        """
        Initialize the Twitter scraper object
        :return:
        """
        return self.app.init.init_twitter_scraper()

    @property
    def twitter_user_matcher(self) -> TwitterUserMatcher:
        """
        Initialize the Twitter user matcher object
        :return:
        """
        return self.app.init.init_twitter_user_matcher()

    @property
    def random_suggested_usernames(self) -> list:
        """
        Get the random suggested usernames
        :return:
        """
        random.seed(15)  # will return ['gusttavo_lima' 'selenagomez' 'officialtulisa' 'drdre' 'Eminem']
        return random.sample(self.usernames_dict.keys(), 5)

    def capture_change_value(self) -> None:
        """
        Capture the state username value
        :return:
        """
        st.session_state.username = st.session_state.get('selected_username')

    def render_select_random_celebrity(self) -> None:
        """
        Render the select random celebrity selectbox
        :return:
        """
        # helpful link - https://github.com/streamlit/streamlit/issues/3601
        st.selectbox("Select a celebrity (twitter username) :", self.usernames_dict.keys(),
                     key='selected_username', on_change=self.capture_change_value)

    def render_suggested_users(self) -> None:
        """
        Render the suggested user buttons
        :return:
        """
        st.markdown("Or Try one of these users:")
        random_celebrity_usernames = ['taylorswift13', 'Cristiano', 'BillGates',
                                      'coldplay', 'iamsrk', 'johngreen']
        # or use self.random_suggested_usernames
        columns = st.columns(len(random_celebrity_usernames))
        for col, user in zip(columns, random_celebrity_usernames):
            with col:
                if st.button(user):
                    st.session_state.username = user

    def render_search_form(self) -> bool:
        """
        Render the search form
        :return:
        """
        st.markdown("Or Enter a username:")
        with st.form("search_form"):
            if st.session_state.get('username'):
                st.session_state.username = st.text_input("Username", value=st.session_state.username)
            else:
                st.session_state.username = st.text_input("Username")
            return st.form_submit_button("Search")

    def render_top_search_results(self) -> None:
        """
        Render the top search results
        :return:
        """
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
        results = sorted(closest_list, key=lambda item: item[1], reverse=True)[1:self.top_n + 1]
        result_df = pd.DataFrame(results, columns=['Twitter Username', 'Similarity Score'])

        # show the Celebrity Names
        result_df.insert(1, 'Name', result_df['Twitter Username'].map(lambda x: self.usernames_dict.get(x)))
        # result_df['Similarity Score'] = result_df['Similarity Score'].map(lambda x: round(x, 4)) # no need

        # display the Twitter profile link
        result_df['Twitter link'] = result_df['Twitter Username'].map(lambda x: 'https://twitter.com/' + x)

        # display the top n results
        st.markdown(
            f"#### Top {self.top_n} Most Similar Celebrity Accounts For '[{username}](https://twitter.com/{username})' "
            f"({n if (n := lower_dict(self.usernames_dict).get(username.lower())) else self.twitter_scraper.fetch_profile_name(username)}):")  # lower() to bypass case issue

        # todo: display full text of the twitter link
        # more customization/ a possible option : https://github.com/PablocFonseca/streamlit-aggrid
        with option_context('display.max_colwidth', None):
            # result_df.style.set_properties(subset=['link'], **{'width': '900px'})
            # st.dataframe(result_df.style.set_precision(4)) # deprecated
            st.dataframe(result_df.style.format({'Similarity Score': '{:.4f}'}))

    def match_two_celeb_users(self) -> None:
        """
        Match two Celebrity users
        :return:
        """
        st.markdown("#### Match Two Celebrities From The Celebrity Account List")
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
                    if score_result := self.twitter_user_matcher.match_twitter_user(celeb_usernames[0],
                                                                                    celeb_usernames[1]):
                        _, similarity_score = score_result
                except Exception as e:
                    logging.info(e)
                    return st.error(f"An error occurred!")
            if similarity_score is None:
                return st.error("An error occurred!")
            else:
                st.success(
                    f"The similarity score between **[{celeb_usernames[0]}](https://twitter.com/{celeb_usernames[0]})**"
                    f" and **[{celeb_usernames[1]}](https://twitter.com/{celeb_usernames[1]})** is: "
                    f"**{similarity_score:.4f}**")

    def match_two_users(self) -> None:
        """
        Match two Twitter users
        :return:
        """
        st.markdown("#### Match Two Twitter Users")
        with st.expander("Behind the scene"):
            st.markdown(
                """
            If the username is not in the list then the scraper scrapes user's latest ~3200 tweets. (~14sec max) 
            And, it takes 7-8 seconds to preprocess the tweets. Also, if not GPU it might take a long time 
            (for ~3200 tweets - 1min+) to generate the vector embeddings. 
            That's why it takes a while to get the results.
            """)
        user1 = st.text_input('Select Twitter User1', 'BarackObama').strip()
        user2 = st.text_input('Select Twitter User2', 'BorisJohnson').strip()

        if len(user1) == 0 or len(user2) == 0:
            return st.warning("Usernames can not be empty!")
        if user1 == user2:
            return st.warning("Please select two different users!")

        if st.button('Check Similarity'):
            if len(user1) > 0 and len(user2) > 0:
                # get the similarity score
                with st.spinner("Calculating the similarity score... Please wait...This might take a while..."):
                    try:
                        if score_result := self.twitter_user_matcher.match_twitter_user(user1, user2):
                            _, similarity_score = score_result
                    except Exception as e:
                        logging.info(e)
                        return st.error(f"An error occurred!")
                if similarity_score is None:
                    return st.error("An error occurred!")
                else:
                    st.success(
                        f"The similarity score between **[{user1}](https://twitter.com/{user1})** "
                        f"and **[{user2}](https://twitter.com/{user2})** is: "
                        f"**{similarity_score:.4f}**")

    def render_overview(self) -> None:
        """
        Render the overview page
        :return:
        """
        st.markdown("""
        #### Overview 
        This app finds similar Twitter users based on their tweets. It works in two ways 
        1. Get a list of most similar celebrity twitter accounts based on a predefined Twitter celebrity list (917\
        Twitter celebrity accounts). 
        2. Find similarity between two Twitter users based on their tweets. 
        
        Source -
        - GitHub Project Link: [ahmedshahriar/TwitterCelebrityMatcher](https://github.com/ahmedshahriar/TwitterCelebrityMatcher)
        - Kaggle Notebook Link: [Twitter Celebrity Matcher (SBERT+ Tweepy)](https://www.kaggle.com/code/ahmedshahriarsakib/twitter-celebrity-matcher-sbert-tweepy)
        """)

        with st.expander("Check out the Datasets"):
            st.markdown("""
        Feel free to use the datasets -

        1. [Top 1000 Twitter Celebrity Accounts - Kaggle](https://www.kaggle.com/datasets/ahmedshahriarsakib/top-1000-twitter-celebrity-accounts)
        2. [Top 1000 Twitter Celebrity Tweets And Embeddings - Kaggle](https://www.kaggle.com/datasets/ahmedshahriarsakib/top-1000-twitter-celebrity-tweets-embeddings)
        3. [Emoticon Dictionary - Kaggle](https://www.kaggle.com/datasets/ahmedshahriarsakib/emoticon-dictionary)
        """)

        with st.expander("Click to see how this app works"):
            st.markdown(
                """
            #### Functionalities
            - Enter a Twitter username (from the list) to see the most similar celebrities based on tweets. 
            The celebrities list was collected from the GitHub Gist - 
            [Top-1000-Celebrity-Twitter-Accounts.csv](https://gist.github.com/mbejda/9c3353780270e7298763). 
            - You can also enter two Twitter usernames to see the similarity score between them.

            #### How it works?
            The celebrity tweets were collected using [tweepy](https://tweepy.readthedocs.io). 
            After preprocessing the tweets, the tweets were embedded using 
            [sentence-transformers](https://www.sbert.net/) **pretrained multilingual** model -
            [paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2).
            The similarity score between tweets embeddings is calculated using 
            [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity).

            This app - 
            1. Takes a Twitter username
            2. Scrapes the tweets if it's unavailable
            3. Generate embeddings of the given Twitter account's tweets
            5. Calculate the mean embedding of the tweets (limitation **~3200** tweets)
            4. Finds the **cosine similarity** between 
                - Given user's tweets embeddings and celebrity tweets embeddings
                - Given two user's tweets embeddings
            5. Returns the most similar celebrity twitter accounts based on similarity score or just score between two users 

            #### Performance
            - With CUDA enabled GPU the app runs ~5x faster than CPU.

            For ~3200 tweets in my rig (AMD 2600x, 1050ti, 768 CUDA cores)- 
            - With the current scraping scripts, it takes **~14-16 seconds** to download tweets
            - With **pandas** it takes **~8 seconds** to preprocess the tweets (AMD 2600x)
            - It takes **~6 seconds** to generate embeddings from processed tweets (1050ti, 768 CUDA cores)
            - Took **~2h 5m** in total to preprocess and generate embedding for all users' (917 total) tweets

            ---

            N.B: With the free version of Twitter API, it limits the user to the last 3200 tweets in a timeline
                """)

    def render(self) -> None:
        self.render_overview()
        st.subheader("Most Similar Twitter Celebrities")
        self.render_select_random_celebrity()
        self.render_suggested_users()

        submitted = self.render_search_form()
        if submitted:
            self.render_top_search_results()

        st.subheader("Match 1v1 Twitter Users")
        # match 1v1 celebrity users
        self.match_two_celeb_users()
        # match 1v1 random users
        self.match_two_users()

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
                success_msg = f"The similarity score between " \
                              f"**[{celeb_usernames[0]}](https://twitter.com/{celeb_usernames[0]})** and " \
                              f"**[{celeb_usernames[1]}](https://twitter.com/{celeb_usernames[1]})** is: " \
                              f"**{similarity_score:.4f}** "
                st.success(success_msg)

                # st.markdown('<svg width="24px" height="24px" enable-background="new 0 0 512 512" version="1.1"
                # viewBox="0 0 512 512" xml:space="preserve" xmlns="http://www.w3.org/2000/svg"><path d="m509.01
                # 206.16-176.92-176.92c-2.917-2.917-7.304-3.789-11.115-2.21-3.81 1.579-6.296 5.299-6.296
                # 9.423v96.287h-49.705c-70.777 0-137.32 27.562-187.36 77.609s-77.609 116.59-77.609 187.36v77.833c0
                # 4.209 2.586 7.986 6.51 9.509 1.199 0.466 2.449 0.691 3.687 0.691 2.81 0 5.561-1.163
                # 7.531-3.32l92.966-101.74c50.333-55.084 122-86.677 196.61-86.677h7.374v96.288c0 4.126 2.486 7.844
                # 6.296 9.423 3.811 1.581 8.198 0.706 11.115-2.21l176.92-176.92c1.912-1.912 2.987-4.507
                # 2.987-7.212s-1.075-5.299-2.987-7.211zm-173.94
                # 159.51v-81.864c0-5.633-4.567-10.199-10.199-10.199h-17.573c-80.331 0-157.48 34.012-211.67
                # 93.316l-75.237 82.339v-51.551c0-134.86 109.72-244.58 244.58-244.58h59.904c5.632 0 10.199-4.566
                # 10.199-10.199v-81.864l152.3 152.3-152.3 152.3z"/><path d="m255.45 170.33c-2.779 0-5.588 0.057-8.35
                # 0.168-5.628 0.226-10.008 4.973-9.78 10.601 0.221 5.489 4.74 9.789 10.184 9.789 0.139 0 0.278-2e-3
                # 0.417-9e-3 2.49-0.1 5.022-0.151 7.529-0.151 5.633 0 10.199-4.566
                # 10.199-10.199s-4.566-10.199-10.199-10.199z"/><path d="m221.1
                # 183.28c-1.279-5.485-6.759-8.895-12.249-7.616-26.861 6.264-51.802 17.74-74.131 34.11-4.544
                # 3.33-5.526 9.713-2.196 14.255 1.998 2.725 5.094 4.169 8.234 4.169 2.093 0 4.205-0.641 6.023-1.975
                # 20.096-14.733 42.54-25.06 66.704-30.696 5.485-1.277 8.894-6.761 7.615-12.247z"/></svg>',
                # unsafe_allow_html=True)

                social_share_msg = f"""
                Share the result on - <span><a href="https://twitter.com/intent/tweet?hashtags=streamlit%2Cpython
                &amp;text=The%20similarity%20score%20between%20@{celeb_usernames[0]}%20and%20@{celeb_usernames[1]}%20
                is%20{similarity_score*100:.3f}%25%21%20Check%20this%20app%20to%20compare%20twitter%20users%0A&amp
                ;url=https%3A%2F%2Fshare .streamlit.io%2Fahmedshahriar%2Ftwittercelebritymatcher%2Fmain%2Fmain.py" 
                target="_blank" rel="noopener noreferrer"><svg width="36" height="36" viewBox="0 0 48 48" fill="none" 
                xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="24" r="24" fill="#56CCF2"></circle><path 
                d="M35 15.0003C34.0424 15.6758 32.9821 16.1924 31.86 16.5303C31.2577 15.8378 30.4573 15.347 29.567 
                15.1242C28.6767 14.9015 27.7395 14.9575 26.8821 15.2847C26.0247 15.612 25.2884 16.1947 24.773 
                16.954C24.2575 17.7133 23.9877 18.6126 24 19.5303V20.5303C22.2426 20.5759 20.5013 20.1861 18.931 
                19.3957C17.3607 18.6054 16.0103 17.4389 15 16.0003C15 16.0003 11 25.0003 20 29.0003C17.9405 30.3983 
                15.4872 31.0992 13 31.0003C22 36.0003 33 31.0003 33 19.5003C32.9991 19.2217 32.9723 18.9439 32.92 
                18.6703C33.9406 17.6638 34.6608 16.393 35 15.0003Z" fill="white"></path></svg></a>   <a 
                href="https://www.linkedin.com/sharing/share-offsite/?summary=https%3A%2F%2Fshare.streamlit.io
                %2Fahmedshahriar%2Ftwittercelebritymatcher%2Fmain%2Fmain.py%20%23streamlit%20%23python&amp;title
                =Check%20out%20this%20awesome%20Streamlit%20app%20I%20built%0A&amp;url=https%3A%2F%2Fshare.streamlit
                .io%2Fahmedshahriar%2Ftwittercelebritymatcher%2Fmain%2Fmain.py" target="_blank" rel="noopener 
                noreferrer"><svg width="36" height="36" viewBox="0 0 48 48" fill="none" 
                xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="24" r="24" fill="#1C83E1"></circle><path 
                d="M28 20C29.5913 20 31.1174 20.6321 32.2426 21.7574C33.3679 22.8826 34 24.4087 34 26V33H30V26C30 
                25.4696 29.7893 24.9609 29.4142 24.5858C29.0391 24.2107 28.5304 24 28 24C27.4696 24 26.9609 24.2107 
                26.5858 24.5858C26.2107 24.9609 26 25.4696 26 26V33H22V26C22 24.4087 22.6321 22.8826 23.7574 
                21.7574C24.8826 20.6321 26.4087 20 28 20Z" fill="white"></path><path d="M18 21H14V33H18V21Z" 
                fill="white"></path><path d="M16 18C17.1046 18 18 17.1046 18 16C18 14.8954 17.1046 14 16 14C14.8954 
                14 14 14.8954 14 16C14 17.1046 14.8954 18 16 18Z" fill="white"></path></svg></a></span> """

                st.markdown(social_share_msg, unsafe_allow_html=True)

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
                    success_msg = f"The similarity score between **[{user1}](https://twitter.com/{user1})** " \
                                  f"and **[{user2}](https://twitter.com/{user2})** is: " \
                                  f"**{similarity_score:.4f}**"
                    st.success(success_msg)

    def render_overview(self) -> None:
        """
        Render the overview page
        :return:
        """
        st.markdown("""
        #### Overview 
        This app finds similar Twitter users based on their tweets. It works in two ways -
        1. Generate a list of most similar celebrity twitter accounts based on a predefined Twitter celebrity list (917\
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

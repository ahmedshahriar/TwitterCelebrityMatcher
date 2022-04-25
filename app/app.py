"""
## Twitter Celebrity Matcher - Streamlit App

This app is a tool to match celebrities from Twitter with their respective tweets.

Author: [Ahmed Shahriar Sakib](https://www.linkedin.com/in/ahmedshahriar)
Source: [Github](https://github.com/ahmedshahriar/TwitterCelebrityMatcher)
"""

import streamlit as st

from app.appdata import AppData
from app.apphome import AppHome
from app.appinit import AppInit


class App:
    title = "Twitter Celebrity Matcher"
    description = """
    This app is a tool to match Twitter users with their respective tweets.
    
    Made by: [Ahmed Shahriar Sakib](https://www.linkedin.com/in/ahmedshahriar).
    Source: [Github](https://github.com/ahmedshahriar/TwitterCelebrityMatcher)
    """
    author = "Ahmed Shahriar Sakib"
    version = "1.0.1"

    def __init__(self) -> None:
        self.data = AppData()
        self.init = AppInit(self.data)

    def set_config(self) -> None:
        st.set_page_config(
            page_title=self.title,
            menu_items={
                'About': self.description,
            }
        )

    def render(self):
        self.set_config()  # set web app config
        st.title(self.title)  # set the page title
        AppHome(self).render()  # render the home page

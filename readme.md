# Twitter Celebrity Matcher
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ahmedshahriar/TwitterCelebrityMatcher/main) [![Live in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/ahmedshahriar/twittercelebritymatcher/main/main.py)

The objective of this project is to match celebrity users with their respective tweets by making use of Semantic Textual Similarity.

This app finds similar Twitter users based on their tweets. It works in two ways -
1. Get a list of the most similar celebrity Twitter accounts based on a predefined Twitter celebrity list (917\
 Twitter celebrity accounts). 
2. Find similarities between two Twitter users based on their tweets. 

:computer: [**Streamlit App**](#streamlit-app) | :ballot_box_with_check: [**How it works?**](#how-it-works) | :hammer_and_wrench: [**Project Structure**](#project-structure) | :floppy_disk: [**Dataset**](#dataset) |:camera: [**Screenshots**](#screenshots) | 🔎 [**Findings**](#findings) | :arrow_down: [**Built With**](#built-with)
--- | --- | --- | --- |--- | --- | ---

## Setup 🔧


Add the following to your `.env` file to work with tweepy:
```
ACCESS_KEY=YOUR_ACCESS_KEY
ACCESS_SECRET=YOUR_ACCESS_SECRET
CONSUMER_KEY=YOUR_CONSUMER_KEY
CONSUMER_SECRET=YOUR_CONSUMER_SECRET

```
### Virtual Environment Setup
Set up a virtual environment (preferably python 3.8+, features such as `walrus` operator was used) and run:
```
$ pip install -r requirements.txt
```
Check main.py file to run the streamlit app or API.

### Docker Setup

Build -
```
docker build -t twitter-celebrity-matcher .
```

Run - 
```
docker run -p 8501:8501 twitter-celebrity-matcher
```

If you have CUDA enabled GPU, you can [set up pytorch](https://pytorch.org/get-started/locally/) (for **SBERT**) with pip -

```
$ pip install --no-cache-dir --force-reinstall torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio===0.11.0+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
```

Static type testing - 
```
$ mypy main.py --ignore-missing-imports
```

### Streamlit App💻

The app file is located at `app/app.py`.

To run the app, run the following command after installing necessary dependencies from `requirements.txt` -

```
$ streamlit run main.py
```
will start the app at default port `8501`.

#### App Walkthrough

![](https://github.com/ahmedshahriar/TwitterCelebrityMatcher/blob/main/assets/walkthrough.gif)

## Project Structure

```
TwitterCelebrityMatcher
├── api
│   ├── __init__.py
│   ├── api.py
├── app
│   ├── __init__.py
│   ├── app.py
├── celebrity-listing
│   ├── Top-1000-Celebrity-Twitter-Accounts.csv
├── core
│   ├── __init__.py
│   ├── dataprep.py
│   ├── matcher.py
│   ├── scraper.py
│   ├── utils.py
├── twitter-celebrity-embed-data
│   ├── twitter-celebrity-embed-data.csv
└── .env
    |
    config.py
    |
    main.py    
```
- **api** - fastApi script
- **app** - streamlit app script
- **core** - contains 3 helper scripts
  - **dataprep.py** - scripts for all preprocessing tasks ( tweet cleaning, embedding generation etc.)
  - **matcher.py** - core functionalities to match twitter users
  - **matcher.py** - twitter scraper helper script
- **config.py** - all configuration variables
- **main.py** - run 3 apps - console scripts, streamlit app or API

`utitlities` directory contains a standalone tweepy scraper scripts - `tweepy_scraper.py` and emoticon proprocessing scripts (original from `ekphrasis` module)

## How it works?
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
4. Calculate the mean embedding of the tweets (limitation ~3200 tweets)
5. Finds the **cosine similarity** between 
    - Given user's tweets embeddings and celebrity tweets embeddings
    - Given two user's tweets embeddings
6. Returns the most similar celebrity Twitter accounts based on similarity score or just score between two users 

## Dataset

### List of Celebrity Twitter Accounts
Open Source GitHub Gist - 
[Top-1000-Celebrity-Twitter-Accounts.csv](https://gist.github.com/mbejda/9c3353780270e7298763)

NB: 
- There are some duplicates in the dataset. (986 after filtering)
- There are some unofficial Celebrity accounts (ex - [twitter.com/sonunigam](https://twitter.com/sonunigam)) with very small amount of tweets. Here is a good research paper on this topic - [25 Tweets to Know You: A New Model to Predict Personality with Social Media](https://arxiv.org/abs/1704.05513) 

### Generated Embeddings of Celebrity Tweets

The final embeddings of all celebrity tweets  - 
- [Twitter Celebrity Embed Data](https://github.com/ahmedshahriar/TwitterCelebrityMatcher/blob/main/twitter-celebrity-embed-data/twitter-celebrity-embed-data.csv)

### Data Preprocessing
Current pipeline : 
 - Removed hashtags, urls, and mentions 
 - Replaced emoticons with their textual representation ([`ekphrasis`](https://github.com/cbaziotis/ekphrasis))
 - Replaced emoji with their textual representation ([`demoji`](https://pypi.org/project/demoji) package)
 
## Model
- [sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)

<details>
<summary> Citation </summary>

```
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "http://arxiv.org/abs/1908.10084",
}
```

</details>

Word embedding dimension : 384

Download SBERT pretrained models directly from [here](https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/)

## Screenshots

### Match Top Celebrities
![](https://github.com/ahmedshahriar/TwitterCelebrityMatcher/blob/main/assets/Twitter-celebrity-matcher-1.png)

### Match 1v1 Celebrities
#### User Interface
![](https://github.com/ahmedshahriar/TwitterCelebrityMatcher/blob/main/assets/Twitter-celebrity-matcher-2.png)

#### Result Section
![](https://github.com/ahmedshahriar/TwitterCelebrityMatcher/blob/main/assets/Twitter-celebrity-matcher-1v1.png)

## Findings!🔎
- Most of the celebrities are from music, film or sports industry. The similarity results in these categories are very impressive.  

### Music

<details>
 <summary> Click to view similar celebrities from music industry - <b>individual</b> (query - <code>Taylor Swift</code>) </summary>
 
 ![](https://github.com/ahmedshahriar/TwitterCelebrityMatcher/blob/main/assets/Twitter-celebrity-matcher-singer.png)
 
 </details>
 
<details>
 <summary> Click to view similar celebrities from music industry - <b>band</b> (query - <code>Coldplay</code>)  </summary>
 
 ![](https://github.com/ahmedshahriar/TwitterCelebrityMatcher/blob/main/assets/Twitter-celebrity-matcher-band.png)
 
 </details>
 
### Sports

 <details>
 <summary> Click to view similar celebrities from music industry - <b>footballer</b> (query - <code>Cristiano Ronaldo</code>)  </summary>
 
 ![](https://github.com/ahmedshahriar/TwitterCelebrityMatcher/blob/main/assets/Twitter-celebrity-matcher-footballer.png)
 
 </details>
 
### Regional Film Industry

- The multilingual model does a great job finding region/culture specific attributes. Below is an example of bollywood celebrities 

 <details>
 <summary> Click to view similar celebrities from film industry - <b>actor</b> (query - <code>Shah Rukh Khan</code>)  </summary>
 
 ![](https://github.com/ahmedshahriar/TwitterCelebrityMatcher/blob/main/assets/Twitter-celebrity-matcher-indian-actor.png)
 
 </details>
 
### Author

- The number of **authors** in this celebrity list is comparatively lower than other dominating professions (actors, singers, footballers etc.). So in this example the first few results (first two from the results -> both are above `0.94` score )  were good but then the score drops. The **drop rate** is higher that the results from the dominating celebrity professions where the top score is around `0.96+` and first 10 or 20 from the list have very close score. This will vary but with only 917 users the performance of the pretrained model is great in this case
  
 <details>
 <summary> Click to view similar celebrity authors - (query - <code>John Green</code>)  </summary>
 
 ![](https://github.com/ahmedshahriar/TwitterCelebrityMatcher/blob/main/assets/Twitter-celebrity-matcher-author.png)
 
 </details>

### Multiple Roles - Business Magnet/ Philanthropist

- From the screenshot below, it's very clear that there are few people on the list who are very active in multiple categories. 
  - The closest of them all (for **Bill Gates**) is **Richard Branson** although the score is comparatively lower (`0.82`) than what we see in other categories. Considering how close their roles are (both are billionaires, investor, tech) this is a very positive result.
  - `Leonardo DiCaprio` is the second placeholder because he falls into **Philanthropist** category, same goes for `Tony Robbins`
  - Other famous **billionaires** such as - `anand mahindra` and `Ratan N. Tata` makes it to the top 10
  - Most of the top people are either founders of large organizations, activists, philanthropists or authors. (**Bill Gates** published few books, so this could be another factor)

 <details>
 <summary> Click to view similar celebrity billionaires/investors/businessmen/investor - (query - <code>Bill Gates</code>)  </summary>
 
 ![](https://github.com/ahmedshahriar/TwitterCelebrityMatcher/blob/main/assets/twitter-matcher-bill-gates.png)
 
 </details>


NB: Due to space limitation, the screenshots above displays only top 10 results, try the app to view more top results which are very similar to the query 

## FYI
- With CUDA enabled GPU the app runs ~5x faster than CPU.
                
For ~3200 tweets in my rig (AMD 2600x, 1050ti, 768 CUDA cores) - 
  - With the current scraping scripts, it takes ~14-16 seconds to download tweets
  - With `pandas` it takes ~8 seconds to **preprocess** the tweets
  - It takes ~6 seconds to **generate embeddings** from processed tweets
  - Takes **~2h 5m** in total to preprocess and generate embedding for all users' (917 total) tweets

## Built With
```
demoji==1.1.0
ekphrasis==0.5.1
jupyter==1.0.0
python-dotenv==0.19.2
schedule==1.1.0
sentence-transformers==2.2.0
torch==1.11.0+cu113
torchaudio==0.11.0+cu113
torchvision==0.12.0+cu113
streamlit==1.7.0
tweepy==4.7.0
```
## Reference
- [Identifying Insomnia From Social Media Posts: Psycholinguistic Analyses of User Tweets](https://www.jmir.org/2021/12/e27613)
- [An Effective BERT-Based Pipeline for Twitter Sentiment Analysis: A Case Study in Italian](https://www.mdpi.com/1424-8220/21/1/133)
- [SBERT Multilingual Models](https://www.sbert.net/examples/training/multilingual/README.html)
- [Twitter Sentiment Analysis with Deep Learning using BERT and Hugging Face](https://medium.com/mlearning-ai/twitter-sentiment-analysis-with-deep-learning-using-bert-and-hugging-face-830005bcdbbf)
- [Twitter Sentiment Analysis with Twint and Textblob](https://medium.com/@andrew.schleiss/twitter-sentiment-analysis-with-twint-and-textblob-53edbb133bbd)

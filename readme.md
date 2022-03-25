The objective of this project is to match celebrity users with their respective tweets

## Setup

Add the following to your `.env` file to work with tweepy:
```
ACCESS_KEY=YOUR_ACCESS_KEY
ACCESS_SECRET=YOUR_ACCESS_SECRET
CONSUMER_KEY=YOUR_CONSUMER_KEY
CONSUMER_SECRET=YOUR_CONSUMER_SECRET
```
Setup a virtual environment and run:
```
pip install -r requirements.txt
```
## Dataset

### Celebrity Twitter Accounts
Open Source GitHub Gist - 
[Top-1000-Celebrity-Twitter-Accounts.csv](https://gist.github.com/mbejda/9c3353780270e7298763)

NB: There are some duplicates in the dataset. (986 after filtering)

### Data Preprocessing
Filter : 
 - removed hashtags, urls, and mentions 
 - replaced emoticons with their textual representation ([`ekphrasis`](https://github.com/cbaziotis/ekphrasis))
 - replaced emoji with their textual representation ([`demoji`](https://pypi.org/project/demoji) package)
 
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

## Project Details
- Took ~6s to encode each user's tweets (max ~3200 tweets per user) with CUDA (GPU: 1050ti)
- Took ~2h 5m in total to preprocess and encode all users' (917) tweets
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
- [An Effective BERT-Based Pipeline for Twitter Sentiment Analysis: A Case Study in Italian](https://www.mdpi.com/1424-8220/21/1/133)
- [Twitter Sentiment Analysis with Deep Learning using BERT and Hugging Face](https://medium.com/mlearning-ai/twitter-sentiment-analysis-with-deep-learning-using-bert-and-hugging-face-830005bcdbbf)
- [Twitter Sentiment Analysis with Twint and Textblob](https://medium.com/@andrew.schleiss/twitter-sentiment-analysis-with-twint-and-textblob-53edbb133bbd)
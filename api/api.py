import logging
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from config import EMBED_DATA_PATH
from core.matcher import TwitterUserMatcher
from core.utils import username_dict


class TwitterUsername(BaseModel):
    """
    TwitterUsername model: input Twitter username for the model
    """
    username: str


class Prediction(BaseModel):
    """
    Prediction model: output of the model
    """
    similarity_result: Optional[list] = None


class TwitterMatcherModel:
    """ TwitterMatcherModel: class for the model """
    matcher: Optional[TwitterUserMatcher] = None  # matcher object
    usernames_dict = username_dict()  # Get the Twitter account names dictionary
    top_n: int = 100  # Top n results

    def load_model(self):
        """Twitter profile matcher"""
        self.matcher = TwitterUserMatcher(EMBED_DATA_PATH)

    async def predict(self, input_username: TwitterUsername) -> Prediction:  # dependency
        """Runs a prediction"""
        if not self.matcher:
            # raise RuntimeError("Model is not loaded")
            raise HTTPException(status_code=400, detail="Model is not loaded")
        input_username_dict = input_username.dict()
        closest_list = self.matcher.match_top_celeb_users(input_username_dict.get("username"))
        if not closest_list:
            # raise RuntimeError("Result is not found")
            raise HTTPException(status_code=400, detail="An error occurred!")
        results = sorted(closest_list, key=lambda item: item[1], reverse=True)[1:self.top_n + 1]
        #     # orjson doesn't support serializing individual numpy input_data types yet, converting to `python float`
        #     # https://github.com/tiangolo/fastapi/issues/1733
        results = [{"username": k, "similarity": round(float(v), 4)} for k, v in results]
        logging.info(results)
        return Prediction(similarity_result=results)


app = FastAPI()

twitter_matcher_model = TwitterMatcherModel()


@app.get("/")
async def root():
    return {"message": "Welcome to Twitter Celebrity Matcher API"}


@app.post('/results')
async def predict(output: Prediction = Depends(twitter_matcher_model.predict, )) -> Prediction:
    """
    Predict sentiment of a review
    :param output: Prediction
    :return:
    """
    return output


@app.on_event("startup")
async def startup():
    twitter_matcher_model.load_model()

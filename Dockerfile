FROM python:3.9
EXPOSE 8501

COPY twitter-celebrity-embed-data src/twitter-celebrity-embed-data
COPY celebrity-listing src/celebrity-listing
COPY api /src/api
COPY app /src/app
COPY core /src/core
COPY utilities /src/utilities
COPY .env /src
COPY config.py /src
COPY main.py /src
COPY requirements.txt /tmp

WORKDIR /src
RUN pip3 install -r /tmp/requirements.txt
RUN python3 -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'); model.save('models')"
CMD ["streamlit","run",  "main.py"]
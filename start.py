# coding: utf-8

import pickle

from app import settings
from app import lefaso_net
from app import extract_comments_by_article_date
from app import flaubert_large_cased
from app import dehatebert
from app import comments_sentiment_prediction
from app import hate_comments_prediction

# lefaso_net.run()

comments_by_article_date = extract_comments_by_article_date(
    settings.DATASET_PATH
)

an_comments_by_article_date = comments_sentiment_prediction(
    comments=comments_by_article_date,
    model=flaubert_large_cased
)

an_comments_by_article_date = hate_comments_prediction(
    comments=comments_by_article_date,
    model=flaubert_large_cased
)

with open('an_comments_by_article_date.pickle', 'wb') as file:
    pickle.dump(an_comments_by_article_date, file)

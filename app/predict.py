# coding: utf-8

from rich.progress import track

from app import ModelBase


def comments_sentiment_prediction(comments: list, model: ModelBase):
    for comment in track(comments):
        text = comment['comment']
        prediction = model.predict(text)[0]
        sentiment_label = prediction['label']
        sentiment_score = prediction['score']
        comment['sentiment_label'] = sentiment_label
        comment['sentiment_score'] = sentiment_score
    return comments


def hate_comments_prediction(comments: list, model: ModelBase):
    for comment in track(comments):
        text = comment['comment']
        prediction = model.predict(text)[0]
        hate_label = prediction['label']
        hate_score = prediction['score']
        comment['hate_label'] = hate_label
        comment['hate_score'] = hate_score
    return comments

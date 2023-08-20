# coding: utf-8

from pathlib import Path
import json

from unidecode import unidecode


def text_cleaner(text: str) -> str:
    unidecode_text = unidecode(text)
    lower_text = unidecode_text.lower()
    text_words = lower_text.split()
    remove_text_multispaces = ' '.join(text_words)
    return remove_text_multispaces


def extract_comments_by_article_date(dataset_path: Path) -> list:
    dataset: list = []
    comments_by_article_date: list = []
    with open(dataset_path, 'r') as file:
        dataset = json.load(file)

    for article in dataset:
        article_date = article['published_date']
        comments = article['comments']
        for comment in comments:
            comments_by_article_date.append(
                {
                    'article_published_date': article_date,
                    'comment': text_cleaner(comment)
                }
            )
    return comments_by_article_date

# coding: utf-8

import spacy

class NamedEntities:
    def __init__(self) -> None:
        pass

    def get_model(self):
        return spacy.load("fr_core_news_sm")



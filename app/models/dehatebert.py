# coding: utf-8

from typing import Any

from transformers import pipeline

from app.models import ModelBase


class Dehatebert(ModelBase):

    _nlp: Any

    def __init__(self):
        self._nlp = pipeline(
            'text-classification',
            model='Hate-speech-CNERG/dehatebert-mono-french',
            truncation=True,
        )
    
    def predict(self, input_text: str) -> Any:
        return self._nlp(input_text)

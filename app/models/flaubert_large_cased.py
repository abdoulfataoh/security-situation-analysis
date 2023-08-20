# coding: utf-8

from typing import Any

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

from app.models import ModelBase

class FlaubertLargeCased(ModelBase):
    _nlp: Any

    def __init__(self) -> None:
        loaded_tokenizer = AutoTokenizer.from_pretrained(
            'flaubert/flaubert_large_cased'
        )
        loaded_model = AutoModelForSequenceClassification.from_pretrained(
            'DemangeJeremy/4-sentiments-with-flaubert'
        )
        self._nlp = pipeline('sentiment-analysis', model=loaded_model, tokenizer=loaded_tokenizer)

    def predict(self, input_text: str) -> Any:
        return self._nlp(input_text)

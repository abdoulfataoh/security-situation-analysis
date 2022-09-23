# coding: utf-8

from transformers import AutoTokenizer, AutoModelForSequenceClassificatin

class DhateBert:

    def __init__(self):
        ...

    def get_model(self):
        tokenizer = AutoTokenizer.from_pretrained("Hate-speech-CNERG/dehatebert-mono-french")
        model = AutoModelForSequenceClassification.from_pretrained("Hate-speech-CNERG/dehatebert-mono-french")
        return model
    
    DhateBert().get_model()
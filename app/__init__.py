# coding: utf-8

from app import settings
from app.sciences import Sciences

sc = Sciences(str(settings.DATASET_PATH )+ '/dataset.json')
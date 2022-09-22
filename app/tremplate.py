# coding: utf-8

from typing import Literal, List
from dataclasses import dataclass
from datetime import datetime

from app import settings

@dataclass
class Article:
    article_type: Literal['press', 'report']
    published_date: datetime
    origin: str
    url_source: str
    title: str
    content: str
    comments = List[str]
    
    def __post_init__(self):
        ...
        
    @staticmethod
    def to_json(**kwargs) -> dict:
        dic = Article(**kwargs).__dict__
        dic['published_date'].strftime(settings.DATE_FORMAT)
        return dic

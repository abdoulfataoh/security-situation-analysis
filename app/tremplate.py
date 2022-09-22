# coding: utf-8

from typing import Literal, List, Optional
from dataclasses import dataclass
from datetime import datetime

from app import settings

@dataclass
class Article:
    article_type: Literal['press', 'report']
    article_title: str
    published_date: datetime
    origin: str
    url: str
    content: str
    comments: List[str]
    
    def __post_init__(self):
        ...
        
    @staticmethod
    def to_json(**kwargs) -> dict:
        dic = Article(**kwargs).__dict__.copy()
        p_date = dic['published_date'].strftime(settings.DATE_FORMAT)
        dic['published_date'] = p_date
        return dic

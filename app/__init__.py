# coding: utf-8

# coding: utf-8

from app import settings
from app.scraper import DatasetManager
from app.scraper import LefasoNetScraper
from app.preprocessing import extract_comments_by_article_date
from app.models import ModelBase
from app.models import FlaubertLargeCased
from app.models.dehatebert import Dehatebert
from app.predict import comments_sentiment_prediction
from app.predict import hate_comments_prediction

__all__ = [
    'lefaso_net',
    'extract_comments_by_article_date',
    'ModelBase',
    'flaubert_large_cased',
    'dehatebert',
    'comments_sentiment_prediction',
    'hate_comments_prediction',
]

dataset_manager = DatasetManager(settings.DATASET_PATH, 1_000)

lefaso_net = LefasoNetScraper(
    site_url=settings.LEFASO_SITE_URL,
    section_path=settings.LEFASO_SECTION_PATH,
    paging_step=settings.LEFASO_PAGING_STEP,
    min_paging=settings.LEFASO_MIN_PAGING,
    max_paging=settings.LEFASO_MAX_PAGING,
    article_attr=settings.LEFASO_ARTCILE_ATTR,
    site_date_format=settings.LEFASO_DATE_FORMAT,
    dataset_manager=dataset_manager,
)

flaubert_large_cased = FlaubertLargeCased()
dehatebert = Dehatebert()

# coding: utf-8

from app import settings
from app.scraper.lefaso import LefasoNetScraper

__all__ = [
    'lefaso_net',
]

lefaso_net = LefasoNetScraper(
    site_url=settings.LEFASO_SITE_URL,
    section_path=settings.LEFASO_SECTION_PATH,
    paging_step=settings.LEFASO_PAGING_STEP,
    max_paging=settings.LEFASO_MAX_PAGING,
    article_attr=settings.LEFASO_ARTCILE_ATTR,
    site_date_format=settings.LEFASO_DATE_FORMAT,
)

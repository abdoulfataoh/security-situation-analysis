# coding: utf-8

import logging
from typing import List, Dict
from datetime import datetime
from urllib.parse import urljoin

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from unidecode import unidecode

from app import settings
from app.tremplate import Article

logger = logging.getLogger(__name__)

__all__ = [
    'LefasoNetScraper',
]


class LefasoNetScraper():
    _site_url: str
    _section_path: str
    _paging_step = int
    _article_attr: dict
    _max_paging: int
    _pages_numbering: int = 0
    _site_date_format: str

    def __init__(
        self,
        site_url: str,
        section_path: str,
        paging_step: int,
        max_paging: int,
        article_attr: dict,
        site_date_format: str
    ):
        self._site_url = site_url
        self._section_path = section_path
        self._paging_step = paging_step
        self._max_paging = max_paging
        self._article_attr = article_attr
        self._site_date_format = site_date_format
    
    def run(self):
        asyncio.run(
            self.process(callback=self._get_article_data)
    )
        
    async def process(self, callback):
        for pagination in range(0, self._max_paging, self._paging_step):
            url = urljoin(self._site_url, self._section_path)
            url = url.format(page=pagination)
            logger.info(f"get page {url}")
            req = await self._request(url)
            articles = self._get_page_articles_list(req)
            for article in articles:
                article_link = article.get('article_link')
                article_content = await self._request(article_link)
                callback(article_content, article_link)

    async def _request(self, url: str) -> BeautifulSoup:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                html = await r.text()
                soup = BeautifulSoup(html, features='html.parser')
        return soup

    def _get_page_articles_list(
        self,
        soup_html: BeautifulSoup
    ) -> List[Dict[str, str]]:
        articles = []
        for article in soup_html.findAll('div',attrs=self._article_attr):
            content = article.select('h3 > a')[0]
            article_title = unidecode(content.text)
            article_link = urljoin(self._site_url, content.attrs.get('href'))
            articles.append(
                {
                    'article_title': article_title,
                    'article_link': article_link
                }
            )
        return articles
    
    def _get_article_data(self, soup_html: BeautifulSoup, article_url):

        # article_type
        article_type = 'press'

        # origin
        origin = 'lefaso.net'

        # url source
        url_source = article_url

        # pusblished date
        meta = soup_html.select('#hierarchie > abbr')[0]
        pusblished_date_str = meta.attrs.get('title')
        pusblished_date = datetime.strptime(
            pusblished_date_str,
            self._site_date_format,
        )
        
        # title
        main_divs = soup_html.select('div[class="col-xs-12 col-sm-12 col-md-8 col-lg-8"]')
        content_div = main_divs[0]
        title = content_div.select('h3')[0].text
        
        # content
        content = ''
        div = soup_html.findAll(
            'div',
            attrs={'class':'col-xs-12 col-sm-12 col-md-8 col-lg-8'}    
        )[0].findAll(
            'div',
            attrs={'class': 'article_content'}
        )[0].findAll('p')

        for p in div:
            content = content + '\n' + unidecode(p.text).strip()
        
        # comments
        comments = soup_html.select(
            '.comment-texte'
        )

        for comment in comments:
            print(comment.text)
            print('----------')
            print(article_url)
        
  
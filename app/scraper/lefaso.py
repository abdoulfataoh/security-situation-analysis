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
    _min_paging: int
    _max_paging: int
    _pages_numbering: int = 0
    _site_date_format: str

    def __init__(
        self,
        site_url: str,
        section_path: str,
        paging_step: int,
        min_paging: int,
        max_paging: int,
        article_attr: dict,
        site_date_format: str,
    ):
        self._site_url = site_url
        self._section_path = section_path
        self._paging_step = paging_step
        self._min_paging = min_paging
        self._max_paging = max_paging
        self._article_attr = article_attr
        self._site_date_format = site_date_format
    
    def run(self):
        asyncio.run(
            self.process(callback=self._get_article_data)
    )
        
    async def process(self, callback):
        paginations = range(
            self._min_paging,
            self._max_paging,
            self._paging_step
        )
        for pagination in paginations:
            url = urljoin(self._site_url, self._section_path)
            url = url.format(page=pagination)
            logger.info(f"get page {url}")
            req = await self._request(url)
            articles = self._get_page_articles_list(req)
            for article in articles:
                article_title = article.get('article_title')
                article_link = article.get('article_link')
                article_content = await self._request(article_link)
                callback(article_content, article_title, article_link)

    async def _request(self, url: str) -> BeautifulSoup:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                html = await r.text()
                soup = BeautifulSoup(html, features='html.parser')
        return soup

    
    def _get_article_data(
        self,
        soup_html: BeautifulSoup,
        article_title,
        article_url
    ):

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
        title = article_title

        # content
        sumary_content = soup_html.select(
            'div[class="col-xs-12 col-sm-12 col-md-8 col-lg-8"]'
        )[0].select('h3')[0].text
  
        content = unidecode(sumary_content).strip()

        div = soup_html.findAll(
            'div',
            attrs={'class':'col-xs-12 col-sm-12 col-md-8 col-lg-8'}    
        )[0].findAll(
            'div',
            attrs={'class': 'article_content'}
        )[0].findAll('p')

        for p in div:
            content = sumary_content + '\n' + unidecode(p.text).strip()
        
        # comments
        comments_div = soup_html.select(
            '.comment-texte'
        )

        comments: List[str] = []

        for comment in comments_div:
            if comment != None or comment != '':
                comments.append(
                    unidecode(comment.text).strip()
                )
         

        data = Article.to_json(
            article_type='press',
            article_title=article_title,
            published_date=pusblished_date,
            origin='lefaso.net',
            url=article_url,
            content=content,
            comments=comments,
        )
        print(data)
        exit()
    
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
    
        
  
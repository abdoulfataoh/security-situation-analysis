# coding: utf-8

import logging
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from urllib.parse import urljoin

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from unidecode import unidecode

from app.template import Article


logger = logging.getLogger(__name__)


class DatasetManager:

    _dataset_path: Path
    _buffer_size: int
    _buffer: list
    _buffer_records_counter: int

    def __init__(self, dataset_path: Path, buffer_size: int = 1_000):
        self._dataset_path = dataset_path
        self._buffer_size = buffer_size
        self._buffer = []
        self._buffer_records_counter = 0
        if not self._dataset_path.is_file():
            logger.info(
                f"we can't found existing dataset at {self._dataset_path}"
            )
            logger.info("We will try to create new dataset file")
            with open(self._dataset_path, 'w') as file:
                empty_list = []
                json.dump(empty_list, file)

    def append_record(self, record: dict) -> bool:
        self._buffer.append(record)
        self._buffer_records_counter += 1
        if self._buffer_records_counter > self._buffer_size:
            data: list = []
            updated_data: list = []
            with open(self._dataset_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                data.extend(self._buffer)
            with open(self._dataset_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
                self._buffer = []
                self._buffer_records_counter = 0
        return True


class LefasoNetScraper():
    _site_url: str
    _section_path: str
    _paging_step = int
    _article_attr: dict
    _min_paging: int
    _max_paging: int
    _pages_numbering: int = 0
    _site_date_format: str
    _dataset_manager: DatasetManager

    def __init__(
        self,
        site_url: str,
        section_path: str,
        paging_step: int,
        min_paging: int,
        max_paging: int,
        article_attr: dict,
        site_date_format: str,
        dataset_manager: DatasetManager,
    ):
        self._site_url = site_url
        self._section_path = section_path
        self._paging_step = paging_step
        self._min_paging = min_paging
        self._max_paging = max_paging
        self._article_attr = article_attr
        self._site_date_format = site_date_format
        self._dataset_manager = dataset_manager

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
                logger.info(f"get page from {article_link}")
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

        # pusblished date
        meta = soup_html.select('#hierarchie > abbr')[0]
        pusblished_date_str = meta.attrs.get('title')
        pusblished_date = datetime.strptime(
            pusblished_date_str,
            self._site_date_format,
        )

        # content
        sumary_content = soup_html.select(
            'div[class="col-xs-12 col-sm-12 col-md-8 col-lg-8"]'
        )[0].select('h3')[0].text

        content = unidecode(sumary_content).strip()

        try:
            div = soup_html.findAll(
                'div',
                attrs={'class': 'col-xs-12 col-sm-12 col-md-8 col-lg-8'}
            )[0].findAll(
                'div',
                attrs={'class': 'article_content'}
            )[0].findAll('p')

            for p in div:
                content = sumary_content + '\n' + unidecode(p.text).strip()
        except Exception:
            logger.warning(
                f"we can't find <article_content> class from {article_url}"
            )

        # comments
        comments_div = soup_html.select(
            '.comment-texte'
        )
        comments: List[str] = []

        for comment in comments_div:
            if comment is not None or comment != '':
                comments.append(
                    unidecode(comment.text).strip()
                )
        comments_number = len(comments)

        data = Article.to_json(
            article_type=article_type,
            article_title=article_title,
            published_date=pusblished_date,
            origin=origin,
            url=article_url,
            content=content,
            comments_number=comments_number,
            comments=comments,
        )

        self._dataset_manager.append_record(data)

    def _get_page_articles_list(
        self,
        soup_html: BeautifulSoup
    ) -> List[Dict[str, str]]:
        articles = []
        for article in soup_html.findAll('div', attrs=self._article_attr):
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

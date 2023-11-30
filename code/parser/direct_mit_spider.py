import random
from typing import Any, Iterable

from scrapy import Spider, Request
from scrapy.http import Response
from .settings import USER_AGENTS
from scrapy_splash import SplashRequest


class DirectMitSpider(Spider):
    """
    DirectMit spider
    """
    name = 'springer'
    base_url = 'https://direct.mit.edu'
    search_url = 'https://direct.mit.edu/tacl/issue/volume/11'
    splash_args = {
        'html': 1,
        'width': 600,
        'render_all': 1,
        'wait': 5,
    }

    def search_urls(self, start_page: int, max_pages: int) -> Iterable[str]:
        for url in [self.search_url]:
            yield url

    def start_requests(self) -> Iterable[Request]:
        start_page: int = getattr(self, 'last_page', 1)
        max_pages: int = getattr(self, 'max_pages', 1)
        for url in self.search_urls(start_page, max_pages):
            yield SplashRequest(url=url, callback=self.parse, headers={
                'User-Agent': self.get_random_user_agent()
            }, args=self.splash_args)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for item in response.css('.al-article-items'):
            if len(item.css('i.icon-availability_open')) <= 0:
                continue

            article_link: str = item.css('h5.item-title a::attr(href)').get().strip()
            yield SplashRequest(self.base_url + article_link, callback=self.parse_article, headers={
                'User-Agent': self.get_random_user_agent()
            }, args=self.splash_args)

    def parse_article(self, response: Response, **kwargs: Any) -> Any:
        yield {
            "title": response.css('h1.article-title-main::text').get().strip(),
            "author": '|'.join([
                author.strip()
                for author in response.css('.al-author-name .linked-name::text').getall()
            ]),
            "annotation": response.css('section.abstract p::text').get().strip(),
            "content": ''.join([
                content.strip()
                for content in response.css('div.js-article-section *::text').getall()
            ]),
            "url": response.url,
        }

    def get_random_user_agent(self) -> str:
        return USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)]

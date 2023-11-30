import random
from typing import Any, Iterable
from scrapy import Spider, Request
from scrapy_splash import SplashRequest
from scrapy.http import Response
from .settings import USER_AGENTS


class ElsevierSpider(Spider):
    """
    Elsevier spider
    """
    name = 'elsevier'
    elsevier_base_url = 'https://www.sciencedirect.com'
    elsevier_search_url = 'https://www.sciencedirect.com/search?date=2017-2023&qs=algorithm&langs=en&subjectAreas=1700&accessTypes=openaccess&show=25&offset='
    articles_per_page = 25

    splash_args = {
        'html': 1,
        'width': 600,
        'render_all': 1,
        'wait': 5,
    }

    def search_urls(self, start_page: int, max_pages: int) -> Iterable[str]:
        for page in range(start_page - 1, start_page + max_pages - 1):
            yield self.elsevier_search_url + str(page * self.articles_per_page)

    def start_requests(self) -> Iterable[Request]:
        start_page: int = getattr(self, 'last_page', 1)
        max_pages: int = getattr(self, 'max_pages', 1)
        for url in self.search_urls(start_page, max_pages):
            yield SplashRequest(url=url, callback=self.parse, headers={
                'User-Agent': self.get_random_user_agent()
            }, args=self.splash_args)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for item in response.css('.ResultItem'):
            if len(item.css('.access-indicator-yes')) <= 0:
                continue

            article_link: str = item.css('a.result-list-title-link::attr(href)').get().strip()
            yield SplashRequest(self.elsevier_base_url + article_link, callback=self.parse_article, headers={
                'User-Agent': self.get_random_user_agent()
            }, args=self.splash_args)

    def parse_article(self, response: Response, **kwargs: Any) -> Any:
        yield {
            "title": response.css('.title-text::text').get().strip(),
            "author": '|'.join([
                author.strip()
                for author in response.css('.author-group .react-xocs-alternative-link::text').getall()
            ]),
            "annotation": response.css('.abstract.author p::text').get().strip(),
            "content": ''.join([
                content.strip()
                for content in response.css('section p::text').getall()
            ]),
            "url": response.url,
        }

    def get_random_user_agent(self) -> str:
        return USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)]

import random
from typing import Any, Iterable

from scrapy import Spider, Request
from scrapy.http import Response
from .settings import USER_AGENTS


class SpringerSpider(Spider):
    """
    Springer spider
    """
    name = 'springer'
    springer_base_url = 'https://link.springer.com'
    springer_search_url = 'https://link.springer.com/search?new-search=true&query=new+internet+searching+algorithm&content-type=Article&language=En&facet-discipline=%22Computer+Science%22&date=custom&dateFrom=2018&sortBy=relevance&page='

    def search_urls(self, start_page: int, max_pages: int) -> Iterable[str]:
        for page in range(start_page, start_page + max_pages):
            yield self.springer_search_url + str(page)

    def start_requests(self) -> Iterable[Request]:
        start_page: int = getattr(self, 'last_page', 1)
        max_pages: int = getattr(self, 'max_pages', 1)
        for url in self.search_urls(start_page, max_pages):
            yield Request(url=url, callback=self.parse, headers={
                'User-Agent': self.get_random_user_agent()
            })

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for item in response.css('li.c-card-open'):
            if len(item.css('span.c-meta__item.u-color-open-access')) <= 0:
                continue

            article_link: str = item.css('h3.c-card-open__heading a::attr(href)').get().strip()
            yield Request(self.springer_base_url + article_link, callback=self.parse_article, headers={
                'User-Agent': self.get_random_user_agent()
            })

    def parse_article(self, response: Response, **kwargs: Any) -> Any:
        yield {
            "title": response.css('h1.c-article-title::text').get().strip(),
            "author": '|'.join([
                author.strip()
                for author in response.css('li.c-article-author-list__item a[data-test="author-name"]::text').getall()
            ]),
            "annotation": response.css('section[data-title="Abstract"] p::text').get().strip(),
            "content": ''.join([
                content.strip()
                for content in response.css('div.main-content::text,div.main-content *::text').getall()
            ]),
            "url": response.url,
        }

    def get_random_user_agent(self) -> str:
        return USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)]

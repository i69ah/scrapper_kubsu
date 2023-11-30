import os
import json
from typing import Type
from celery import shared_task
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from articles.models import Article, Source
from django.db.models import Q
from parser.settings import get_settings_for_source
from parser.elsevier_spider import ElsevierSpider
from parser.springer_spider import SpringerSpider
from parser.direct_mit_spider import DirectMitSpider
from scrapy.utils.log import configure_logging
from scrapy import Spider


@shared_task
def scrape_springer():
    springer_source = Source.objects.get(name='Springer')
    scrape_for_source(springer_source)


@shared_task
def scrape_elsevier():
    elsevier_source = Source.objects.get(name='Elsevier')
    scrape_for_source(elsevier_source)


@shared_task
def scrape_direct_mit():
    elsevier_source = Source.objects.get(name='DirectMit')
    scrape_for_source(elsevier_source)


def scrape_for_source(source: Source):
    settings = get_settings_for_source(source)
    configure_logging(settings)
    crawler = CrawlerProcess(settings)
    d = crawler.crawl(
        get_spider_class_by_source(source),
        last_page=source.last_page,
        max_pages=source.max_pages_per_session
    )
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    articles_list = []

    if os.path.isfile(source.file_name):
        with open(source.file_name, encoding='utf-8') as f:
            json_articles = json.load(f)
            for item in json_articles:
                if Article.objects.filter(Q(title=item['title']) | Q(url=item['url'])).exists():
                    continue

                articles_list.append(Article(
                    title=item['title'],
                    author=item['author'],
                    annotation=item['annotation'],
                    content=item['content'],
                    url=item['url'],
                    source=source
                ))

        os.unlink(source.file_name)

    if len(articles_list) > 0:
        Article.objects.bulk_create(articles_list)
        source.last_page += source.max_pages_per_session
        source.save()


def get_spider_class_by_source(source: Source) -> Type[Spider]:
    spiders = {
        'Springer': SpringerSpider,
        'Elsevier': ElsevierSpider,
        'DirectMit': DirectMitSpider,
    }

    return spiders[source.name]

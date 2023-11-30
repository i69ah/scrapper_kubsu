from scrapy.settings import Settings
from articles.models import Source

FEEDS_SETTINGS = {
    'format': 'json',
    'overwrite': True,
    'encoding': 'utf8',
    'store_empty': False,
    'indent': 4,
    'item_export_kwargs': {
        'export_empty_fields': True,
    },
}

DOWNLOAD_DELAY = 2.5

COOKIES_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

# --- For dynamic sites ---

SPLASH_URL = 'http://splash:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# --- For dynamic sites ---

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]


def get_settings_for_source(source: Source) -> Settings:
    settings = Settings()
    settings.set('FEEDS', {source.file_name: FEEDS_SETTINGS})
    settings.set('COOKIES_ENABLED', COOKIES_ENABLED)
    settings.set('DOWNLOAD_DELAY', DOWNLOAD_DELAY)
    if source.type == Source.Type.DYNAMIC:
        settings.set('SPLASH_URL', SPLASH_URL)
        settings.set('DOWNLOADER_MIDDLEWARES', DOWNLOADER_MIDDLEWARES)
        settings.set('SPIDER_MIDDLEWARES', SPIDER_MIDDLEWARES)
        settings.set('DUPEFILTER_CLASS', DUPEFILTER_CLASS)
        settings.set('HTTPCACHE_STORAGE', HTTPCACHE_STORAGE)

    return settings

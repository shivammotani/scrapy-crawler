# product_crawler/spiders/product_spider.py

import scrapy
import re
from urllib.parse import urlparse
from product_crawler.utils.url_normalizer import UrlNormalizer
from product_crawler.items import ProductUrlItem
from scrapy.utils.project import get_project_settings

class ProductSpider(scrapy.Spider):
    name = "productspider"

    def __init__(self, domain=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not domain:
            raise ValueError("Missing domain argument")
        self.currentDomain = urlparse(domain).netloc.lower().removeprefix("www.")
        self.start_urls = [f"https://{self.currentDomain}"]

        self.settings = get_project_settings()
        self.product_patterns = self.settings.get('PRODUCT_URL_PATTERNS', [])
        self.product_regexes = [re.compile(pattern) for pattern in self.product_patterns]

        self.collection_patterns = self.settings.get('COLLECTION_URL_PATTERNS', [])
        self.collection_regexes = [re.compile(pattern) for pattern in self.collection_patterns]

        self.follow_normal_pages = True
        self.seen_product_urls = set()
        self.seen_collections = set()

    def parse(self, response):
        return self._process_links(response)

    def _process_links(self, response):
        hrefs = response.css("a::attr(href)").getall()
        for href in hrefs:
            yield from self._handle_link(href, response)

    def _handle_link(self, href, response):
        if href.startswith(('mailto:', 'tel:', 'javascript:')):
            return
        full_url = response.urljoin(href)
        normalized = UrlNormalizer.normalize(full_url)
        domain = urlparse(normalized).netloc.lower()

        if domain != self.currentDomain:
            return

        if self._is_product_url(normalized):
            if normalized not in self.seen_product_urls:
                self.seen_product_urls.add(normalized)
                yield ProductUrlItem(domain=domain, url=normalized)
            return

        if self._is_collection_url(normalized):
            base_url = normalized.split('?')[0]
            if base_url in self.seen_collections:
                return
            self.seen_collections.add(base_url)
            yield response.follow(full_url, callback=self.parse_collection, dont_filter=True)
            return

        if self.follow_normal_pages:
            yield response.follow(full_url, callback=self.parse)

    def parse_collection(self, response):
        raise NotImplementedError("You must override parse_collection in domain spider")

    def _is_product_url(self, url):
        return any(regex.search(url) for regex in self.product_regexes)

    def _is_collection_url(self, url):
        return any(regex.search(url) for regex in self.collection_regexes)
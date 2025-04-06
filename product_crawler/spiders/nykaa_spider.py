# product_crawler/spiders/nykaa_spider.py

from product_crawler.spiders.product_spider import ProductSpider
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs
import scrapy
import re
import json
from product_crawler.items import ProductUrlItem

class NykaaSpider(ProductSpider):
    name = "nykaa_handler"

    def parse_collection(self, response):
        match = re.search(r'/c/(\d+)', response.url)
        if not match:
            self.logger.warning(f"No category ID found in URL: {response.url}")
            return

        category_id = match.group(1)
        self.logger.info(f"Found category ID: {category_id}")

        api_url = (
            f"https://www.nykaafashion.com/rest/appapi/V2/categories/products"
            f"?categoryId={category_id}&currentPage=1"
        )

        yield scrapy.Request(
            url=api_url,
            callback=self.parse_api_response,
            cb_kwargs={'category_id': category_id, 'page': 1}
        )

    def parse_api_response(self, response, category_id, page):
        try:
            data = json.loads(response.text)
            products = data.get("response", {}).get("products", [])
        except Exception as e:
            self.logger.error(f"Failed to parse API response: {e}")
            return

        if not products:
            self.logger.info(f"Reached end of category {category_id} at page {page}")
            return

        for prod in products:
            action_url = prod.get("actionUrl")
            if action_url:
                full_url = f"https://www.nykaafashion.com{action_url}"
                yield ProductUrlItem(domain=self.currentDomain, url=full_url)

        next_page = page + 1
        next_url = (
            f"https://www.nykaafashion.com/rest/appapi/V2/categories/products"
            f"?categoryId={category_id}&currentPage={next_page}"
        )
        yield scrapy.Request(
            url=next_url,
            callback=self.parse_api_response,
            cb_kwargs={'category_id': category_id, 'page': next_page}
        )
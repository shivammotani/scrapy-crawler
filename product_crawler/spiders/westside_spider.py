# product_crawler/spiders/westside_spider.py

from product_crawler.spiders.product_spider import ProductSpider
from product_crawler.utils.url_normalizer import UrlNormalizer
from product_crawler.items import ProductUrlItem
import re, json, scrapy
from urllib.parse import urlparse

class WestsideSpider(ProductSpider):
    name = "westside_handler"

    def parse_collection(self, response):
        script_text = response.xpath('//script[contains(text(), "defaultConfig")]/text()').get()

        if not script_text:
            return

        match = re.search(r'JSON\.parse\(\'(.*?)\'\)', script_text)
        if not match:
            return

        raw_json = match.group(1)

        try:
            unescaped = raw_json.encode().decode('unicode_escape')
            config = json.loads(unescaped)
            api_key = config.get("credentials", {}).get("apiKey")
            store_id = config.get("credentials", {}).get("storeId")

        except Exception as e:
            return
        
        yield from self.fetch_product_page(api_key, store_id, page=1)

    def fetch_product_page(self, api_key, store_id, page):
        url = "https://westside-api.wizsearch.in/v1/products/filter"

        payload = {
            "filters": json.dumps({
                "page": page,
                "productsCount": 50,
                "inStock": ["true"],
                "searchedKey": "="
            })
        }

        headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "DNT": "1",
        "Origin": "https://www.westside.com",
        "Referer": "https://www.westside.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "x-api-key": api_key,
        "x-store-id": store_id,
        "x-request-id": "static-request-id-or-generate-dynamically"
        }

        yield scrapy.Request(
            url=url,
            method="POST",
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse_product_page,
            cb_kwargs={"api_key": api_key, "store_id": store_id, "page": page},
            dont_filter=True,
        )
            
    def parse_product_page(self, response, api_key, store_id, page):
        if response.status >= 400:
            return

        try:
            data = json.loads(response.text)
            products = data.get("payload", {}).get("result", [])
        except Exception as e:
            return

        for product in products:
            url = product.get("url")
            if url and url.startswith("https://www.westside.com/products/"):
                yield ProductUrlItem(domain=self.currentDomain, url=url)

        next_page = page + 1
        yield from self.fetch_product_page(api_key, store_id, page=next_page)


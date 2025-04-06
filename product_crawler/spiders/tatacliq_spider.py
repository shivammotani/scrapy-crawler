# product_crawler/spiders/tatacliq_spider.py

from product_crawler.spiders.product_spider import ProductSpider
from product_crawler.items import ProductUrlItem
import scrapy, re, json
from urllib.parse import urlencode

class TataCliqSpider(ProductSpider):
    name = "tatacliq_handler"

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.tatacliq.com/",
             meta={
                "playwright": True,
                "playwright_page_methods": [
                    {
                        "method": "wait_for_selector",
                        "args": ["div[data-testid='home-page']"]
                    }
                ],
            },
            callback=self.parse
        )

    def parse_collection(self, response):
        match = re.search(r'/c-([a-zA-Z0-9]+)/', response.url)
        if not match:
            return

        search_code = match.group(1).upper()
        yield from self.fetch_tatacliq_page(search_code=search_code, page=1)


    def fetch_tatacliq_page(self, search_code, page):
        base_url = "https://searchbff.tatacliq.com/products/mpl/search"
        params1 = {
            "channel": "WEB",
            "page": page,
            "pageSize": 100,
            "searchText": f":relevance:category:{search_code}:inStockFlag:true"
        }

        params2 = {
            "channel": "WEB",
            "page": page,
            "pageSize": 100,
            "searchText": f":relevance:brand:{search_code}:inStockFlag:true"
        }

        full_url1 = f"{base_url}?{urlencode(params1)}"
        full_url2 = f"{base_url}?{urlencode(params2)}"

        yield scrapy.Request(
            url=full_url1,
            callback=self.parse_tatacliq_products,
            cb_kwargs={"search_code": search_code, "page": page}
        )

        yield scrapy.Request(
            url=full_url2,
            callback=self.parse_tatacliq_products,
            cb_kwargs={"search_code": search_code, "page": page}
        )
    
    def parse_tatacliq_products(self, response, search_code, page):
        if response.status != 200:
            return

        try:
            data = json.loads(response.text)
            products = data.get("searchresult", [])
        except Exception as e:
            return

        a = response.request.url
        b = response.url
        if not products:
            return

        for product in products:
            web_url = product.get("webURL")
            if web_url and web_url.startswith("/"):
                full_url = f"https://www.tatacliq.com{web_url}"
                yield ProductUrlItem(domain=self.currentDomain, url=full_url)

        yield from self.fetch_tatacliq_page(search_code=search_code, page=page + 1)
# product_crawler/spiders/virgio_spider.py

from product_crawler.spiders.product_spider import ProductSpider
import re
import scrapy

class VirgioSpider(ProductSpider):
    name = "virgio_handler"

    def parse_collection(self, response):
        yield from self._process_links(response, follow_normal_pages=False)

        match = re.search(r'"endCursor":"(.*?)"', response.text)
        if match:
            next_cursor = match.group(1)
            base_url = response.url.split('?')[0]
            next_url = f"{base_url}?direction=next&cursor={next_cursor}"
            yield scrapy.Request(
                next_url, 
                callback=self.parse_collection, 
                dont_filter=True,
            )

    

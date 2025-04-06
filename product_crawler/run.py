# run.py

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.spider_factory import SpiderFactory

domains = [
    'https://www.nykaafashion.com',
    'https://www.virgio.com',
    'https://www.tatacliq.com',
    'https://www.westside.com',
]

settings = get_project_settings()
process = CrawlerProcess(settings)

for domain in domains:
    SpiderClass = SpiderFactory.get_handler(domain)
    if SpiderClass:
        print(f"Starting crawl for {domain}")
        process.crawl(SpiderClass, domain=domain)
    else:
        print(f"No handler found for domain: {domain}")

process.start()

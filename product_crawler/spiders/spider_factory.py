# product_crawler/spider_factory.py

class SpiderFactory:
    @staticmethod
    def get_handler(domain):
        domain = domain.lower()
        if "nykaa" in domain:
            from product_crawler.spiders.nykaa_spider import NykaaSpider
            return NykaaSpider
        elif "virgio" in domain:
            from product_crawler.spiders.virgio_spider import VirgioSpider
            return VirgioSpider
        elif "tatacliq" in domain:
            from product_crawler.spiders.tatacliq_spider import TataCliqSpider
            return TataCliqSpider
        elif "westside" in domain:
            from product_crawler.spiders.westside_spider import WestsideSpider
            return WestsideSpider
        return None
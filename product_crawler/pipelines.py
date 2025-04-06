from itemadapter import ItemAdapter
import json
import os

class ProductUrlPipeline:
    def open_spider(self, spider):
        current_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(os.path.dirname(current_file))
        relative_output_dir = spider.settings.get('CUSTOM_FEED_OUTPUT_DIR')
        domain_name = getattr(spider, 'currentDomain', 'unknown').replace('.', '_')
        file_name = f"{domain_name}_output.jsonl"
        output_dir = os.path.join(base_dir, relative_output_dir)
        os.makedirs(output_dir, exist_ok=True)
        self.output_path = os.path.join(output_dir, file_name)
        self.file = open(self.output_path, 'w', encoding='utf-8')
        self.seen_urls = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        url = adapter.get('url')
        if url in self.seen_urls:
            return None
        self.seen_urls.add(url)
        try:
            self.file.write(json.dumps(adapter.asdict()) + '\n')
        except Exception as e:
            spider.logger.error(f"Failed to write item: {e}")
        return item

    def close_spider(self, spider):
        self.file.close()

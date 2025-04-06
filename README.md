# 🕷️ Product Crawler

This is a flexible and extensible product URL crawler built with **Scrapy**. It supports crawling multiple e-commerce websites using a common base spider, with domain-specific logic handled by individual spider handlers.

---

## 🚀 Features

- Crawl multiple e-commerce sites (e.g. Nykaa, TataCliq, Westside, Virgio)
- Extract and normalize product URLs
- Smart filtering using domain-specific product/collection patterns
- Pagination support (cursor or page-based)
- Modular architecture using a spider factory
- Output via Scrapy pipeline (e.g. per-domain CSVs or JSONs)

---

## 🗂️ Project Structure

```
scrapy-crawler/
├── product_crawler/
│  ├── spiders/
│  │   ├── product_spider.py        # Base spider
│  │   ├── spider_factory.py        # Creates domain-specific spiders
│  │   ├── nykaa_spider.py          
│  │   ├── tatacliq_spider.py       
│  │   ├── westside_spider.py       
│  │   └── virgio_spider.py         
│  ├── utils/                       # URL normalization and helpers
│  ├── items.py                     # ProductUrlItem definition
│  ├── pipelines.py                 # File writing/deduplication logic
│  ├── settings.py                  # Scrapy settings
│  ├── run.py                       # Main runner (invokes factory per domain)
├── scrapy.cfg                      # Scrapy configuration
├── .gitignore                      
├── README.md                       
└── requirements.txt                # Python dependencies
```

---

## 📦 Setup

1. **Clone the repo**

```bash
git clone https://github.com/shivammotani/scrapy-crawler.git
cd scrapy-crawler
```

2. **Set up virtual environment (optional but recommended)**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🧪 Running the Crawler

Use the custom runner script to loop through domains:

```bash
cd product-crawler
python run.py
```

This will:
- Load domains from settings
- Use the spider factory to pick the appropriate handler
- Start crawling and extracting product URLs

---

## 📝 Output

Extracted product URLs are saved per domain via the pipeline, e.g.:

```
output/nykaa_product_urls.json
output/tatacliq_product_urls.json
output/westside_product_urls.json
output/virgio_product_urls.json
```

You can modify the storage format inside `pipelines.py`.

---

## 🛠️ Customize

- Add domain-specific logic inside `spiders/{domain}_spider.py`
- Define matching patterns in `settings.py`:
  ```python
  PRODUCT_URL_PATTERNS = [r"/p/\d+", r"/products/"]
  COLLECTION_URL_PATTERNS = [r"/c-\w+"]
  ```

---

## 📚 Requirements

- Python 3.8+
- Scrapy
- scrapy-playwright (for JS-rendered sites like TataCliq)

Install via:

```bash
pip install scrapy scrapy-playwright
playwright install
```

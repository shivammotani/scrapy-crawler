# Scrapy settings for product_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "product_crawler"

SPIDER_MODULES = ["product_crawler.spiders"]
NEWSPIDER_MODULE = "product_crawler.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DEPTH_PRIORITY = 1
CONCURRENT_REQUESTS = 64

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "product_crawler.middlewares.ProductCrawlerSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "product_crawler.middlewares.MockHeaderAgentMiddleWare": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "product_crawler.pipelines.ProductUrlPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = False
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# PlayWright
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30 * 1000  # 30s
PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}

# Custom settings
CUSTOM_FEED_OUTPUT_DIR = 'Output/'

PRODUCT_URL_PATTERNS = [
    r'/product/',                 # common pattern
    r'/products/',                # plural
    r'/p/',                       # shortform (Shopify, Nykaa, etc.)
    r'/item/',                    # used by some retail platforms
    r'/prod/',                    # short for "product"
    r'/shop/',                    # e.g. /shop/red-dress
    r'/detail/',                 # often used in Asian e-comm
    r'/view/',                   # used in some CMSs
    r'/goods/',                  # used in China/Japan-based stores
    r'/catalogue/',              # UK/EU style
    r'/listing/',                # generic, used in templates
    r'/store/',                  # /store/product-name
    r'/sku/',                    # some APIs / catalogues
    r'/[^/]+/p-[\w\d]+',         #tata-cliq
]

COLLECTION_URL_PATTERNS = [
    r'/collections/',    # existing Virgio pattern
    r'/c/',              # Nykaa pattern for e.g. /c/
    r'/[^/]+/c-[\w\d]+', #tata-cliq
]

SCRAPEOPS_API_KEY = 'YOUR_SECRET_HERE'
SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = 'https://headers.scrapeops.io/v1/browser-headers'
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 60
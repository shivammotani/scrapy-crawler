from urllib.parse import urlparse, urlunparse
import re

class UrlNormalizer:
    @staticmethod
    def normalize(url):
        parsed = urlparse(url)

        netloc = parsed.netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]

        path = re.sub(r'/+', '/', parsed.path)
        path = parsed.path.rstrip('/')
        
        cleaned = parsed._replace(
            netloc=netloc,
            path=path,
            query='',
            fragment=''
        )
        return urlunparse(cleaned)

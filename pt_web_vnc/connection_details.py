from urllib.parse import urlparse


class VncConnectionDetails:
    def __init__(self, url) -> None:
        self._parsed_url = urlparse(url)

    @property
    def url(self):
        return self._parsed_url.geturl()

    @property
    def hostname(self):
        return self._parsed_url.hostname

    @property
    def port(self):
        return self._parsed_url.port

    @property
    def path(self):
        return f"{self._parsed_url.path}?{self._parsed_url.query}"

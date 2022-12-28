from bs4 import BeautifulSoup
from .requests import api_request
from .exceptions import RequestError


class QuoteIterator:
    def __init__(self, author_obj):
        self._author_obj = author_obj

    def _get_quotes(self, page: int = 1) -> list:
        response = api_request('GET', self._author_obj.url, params={'page': page}, allow_redirects=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = [i.text for i in soup.find_all('p', class_='blockquote-text')]
        return quotes

    def __iter__(self):
        self._page = 1
        self._quotes = self._get_quotes(self._page)
        return self

    def __next__(self) -> str:
        try:
            if not self._quotes:
                self._page += 1
                self._quotes = self._get_quotes(self._page)
        except RequestError:
            raise StopIteration

        return self._quotes.pop(0)


class Author:
    def __init__(self, author: str, url: str):
        self._author = author
        self._url = url

    @property
    def author(self) -> str:
        return self._author

    @property
    def url(self):
        return self._url

    def get_quotes(self):
        return QuoteIterator(self)

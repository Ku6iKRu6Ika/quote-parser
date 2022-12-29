from bs4 import BeautifulSoup
from .requests import api_request
from .objects import Author
from .exceptions import RequestError

_cache = {}


class CitatyAPI:
    @staticmethod
    def find_author(name):
        for key in _cache.keys():
            if name.lower() in key.lower():
                return Author(key, _cache[key])

        page = 1
        response = api_request('GET', 'avtory', allow_redirects=True)

        try:
            while True:
                soup = BeautifulSoup(response.text, 'html.parser')

                authors = soup.find_all('div', class_='flex items-center mb-3')

                for i in authors:
                    orig_name = i.h5.a.text
                    link = i.h5.a['href']

                    _cache[orig_name] = link

                    if name.lower() in orig_name.lower():
                        return Author(orig_name, link)

                page += 1
                response = api_request('GET', 'avtory', params={'page': page}, allow_redirects=False)
        except RequestError:
            return None

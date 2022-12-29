from bs4 import BeautifulSoup
from .requests import api_request
from .objects import Author
from .exceptions import RequestError

_cache = {}
_page = 1


class CitatyAPI:
    @staticmethod
    def find_author(name):
        global _page, _cache

        for key in _cache.keys():
            if name.lower() in key.lower():
                return Author(key, _cache[key])


        while True:
            response = api_request('GET', 'avtory', params={'page': _page})
            soup = BeautifulSoup(response.text, 'html.parser')

            btns = soup.find('div', {'id': '_ga_pagination_links'}).find_all('a')

            if len(btns) == 1 and btns[0].text == 'Предыдущая':
                break

            authors = soup.find_all('div', class_='flex items-center mb-3')

            for i in authors:
                orig_name = i.h5.a.text
                link = i.h5.a['href']

                _cache[orig_name] = link

                if name.lower() in orig_name.lower():
                    return Author(orig_name, link)

            _page += 1

        return None

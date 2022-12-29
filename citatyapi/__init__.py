from bs4 import BeautifulSoup
from .requests import api_request
from .objects import Author
from .exceptions import RequestError


class CitatyAPI:
    @staticmethod
    def find_author(name):
        response = api_request('GET', 'poisk', params={'h': name})
        soup = BeautifulSoup(response.text, 'html.parser')
        author = soup.find('div', class_='flex items-center mb-3')

        if author is None:
            return

        return Author(author.div.h5.a.text, author.a['href'])

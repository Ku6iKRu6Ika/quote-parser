import requests
from urllib.parse import urljoin

from .exceptions import RequestError

API_HOST = 'https://ru.citaty.net/'


def _build_url(path: str) -> str:
    return urljoin(API_HOST, path)


def api_request(request_method: str, method: str, **kwargs) -> requests.Response:
    url = _build_url(method)
    response = requests.api.request(request_method.lower(), url, **kwargs)

    if response.status_code != 200:
        raise RequestError(response.url, response.status_code, response.text)

    return response

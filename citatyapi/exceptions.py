class RequestError(Exception):
    def __init__(self, url: str, status_code: int, body: str):
        self.url = url
        self.status_code = status_code
        self.body = body

    def __str__(self):
        return f'{self.url}, {self.status_code}:\n{self.body}'

import os
from time import sleep
from typing import List, Literal
from urllib.parse import urljoin

import requests


class GitHub:
    BASE_URL = 'https://api.github.com'

    def __init__(self, token: str = None):
        self.token = token

    @property
    def headers(self):
        return {'Authorization': 'token ' + self.token} if self.token else {}

    def get_redirect_url(self, image_url: str):
        response = requests.get(image_url, headers=self.headers)
        return response.url

    def _get_recursively(self, response: requests.Response, j: List[dict] = []):
        sleep(1)
        j = j + response.json()
        if next_ := response.links.get("next"):
            response = requests.get(next_.get("url"), headers=self.headers)
            response.raise_for_status()
            return self._get_recursively(response, j)
        else:
            return j

    def get_issues(self, owner: str, repository: str, state: Literal["open", "closed", "all"] = "open"):
        url = urljoin(self.BASE_URL, os.path.join("repos", owner, repository, "issues"))
        response = requests.get(url=url, params=dict(per_page=10, state=state), headers=self.headers)
        response.raise_for_status()
        items = self._get_recursively(response)
        return items

    def get_comments(self, url):
        response = requests.get(url=url, params=dict(per_page=10), headers=self.headers)
        response.raise_for_status()
        items = self._get_recursively(response)
        return items

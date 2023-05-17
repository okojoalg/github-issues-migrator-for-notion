from urllib.parse import urljoin

import markdown
import requests
from bs4 import BeautifulSoup

from github import GitHub


class Notion:
    BASE_URL = 'https://api.notion.com/v1/'

    def __init__(self, github: GitHub, page_id: str, token: str):
        self.github = github
        self.database_id = None
        self.page_id = page_id
        self.token = token

    @property
    def headers(self):
        return {
            "Accept": "application/json",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }

    def append_block(self, type_: str, text: str):
        return {
            "object": "block",
            "type": type_,
            type_: {
                "rich_text": [{"text": {"content": text}}],
            },
        }

    def constract_blocks(self, html_text):
        blocks = []
        if html_text:
            soup = BeautifulSoup(html_text, 'html.parser')
            targetTags = soup.find_all(['h1', 'h2', 'h3', 'p', 'span', 'img', 'li', 'pre', 'blockquote'])
            for tag in targetTags:
                if tag.name == 'h1':
                    if tag.get_text(strip=True):
                        blocks.append(self.append_block("heading_1", tag.get_text(strip=True)))
                if tag.name == 'h2':
                    if tag.get_text(strip=True):
                        blocks.append(self.append_block("heading_2", tag.get_text(strip=True)))
                if tag.name == 'h3':
                    if tag.get_text(strip=True):
                        blocks.append(self.append_block("heading_3", tag.get_text(strip=True)))
                if tag.name == 'li':
                    if tag.get_text(strip=True):
                        blocks.append(self.append_block("bulleted_list_item", tag.get_text(strip=True)))
                if tag.name == 'p':
                    if tag.parent.name == 'blockquote':
                        continue
                    if tag.get_text(strip=True):
                        blocks.append(self.append_block("paragraph", tag.get_text(strip=True)))
                if tag.name == 'img':
                    blocks.append(
                        {
                            "type": "image",
                            "image": {
                                "type": "external",
                                "external": {
                                    "url": self.github.get_redirect_url(tag['src'])
                                }
                            }
                        }
                    )
                if tag.name == 'pre':
                    if tag.get_text(strip=True):
                        blocks.append(self.append_block(tag.get_text(strip=True)))
                if tag.name == 'blockquote':
                    if tag.get_text(strip=True):
                        blocks.append(self.append_block("quote", tag.get_text(strip=True)))
        return blocks

    def create(self, title):
        payload = {
            "parent": {
                "type": "page_id",
                "page_id": self.page_id
            },
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": title,
                    }
                }
            ],
            "properties": {
                "title": {
                    "title": {}
                },
                "number": {
                    "number": {}
                },
                "status": {
                    "select": {}
                },
                "author": {
                    "select": {}
                },
                "assignees": {
                    "multi_select": {}
                },
                "labels": {
                    "multi_select": {}
                },
                "ref": {
                    "url": {}
                },
                "created_at": {
                    "date": {}
                },
                "updated_at": {
                    "date": {}
                },
                "closed_at": {
                    "date": {}
                },
            }
        }
        url = urljoin(self.BASE_URL, "databases")
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        self.database_id = response.json().get("id")

    def post(self, issue, comments):
        properties = {
            "title": {
                "title": [{"text": {"content": issue.get("title", "")}}],
            },
            "number": {"number": issue.get("number", "")},
            "status": {"select": {"name": issue.get("state", "")}},
            "author": {"select": {"name": issue.get("user").get("login")}},
            "assignees": {"multi_select": [{"name": assignee.get("login")} for assignee in issue.get("assignees")]},
            "labels": {"multi_select": [{"name": label.get("name")} for label in issue.get("labels")]},
            "ref": {"url": issue.get("html_url")},
            "created_at": {"date": {"start": issue.get("created_at"), "time_zone": "Asia/Tokyo"}},
            "updated_at": {"date": {"start": issue.get("updated_at"), "time_zone": "Asia/Tokyo"}},
        }
        if issue.get("closed_at"):
            properties["closed_at"] = {"date": {"start": issue.get("closed_at")}}
        children = []
        if body := issue.get("body"):
            html = markdown.markdown(body)
            children += self.constract_blocks(html)
        if comments:
            children.append({
                "type": "divider",
                "divider": {}
            })
            children.append(self.append_block("heading_1", "Comments"))
            for comment in comments:
                children.append({
                    "type": "divider",
                    "divider": {}
                })
                if body := comment.get("body"):
                    html = markdown.markdown(body)
                    children += self.constract_blocks(html)
                    children += [self.append_block(
                        "paragraph",
                        f'created_by: {comment.get("user").get("login")}, '
                        f'created_at: {comment.get("created_at")}, '
                        f'updated_at: {comment.get("updated_at")}'
                    )]
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
        }
        if children:
            payload["children"] = children
        url = urljoin(self.BASE_URL, "pages")
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()

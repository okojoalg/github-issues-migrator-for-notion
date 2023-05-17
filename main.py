import click

from github import GitHub
from notion import Notion


@click.command()
@click.option('--github-token', type=str, default=None)
@click.option('--github-owner', type=str)
@click.option('--github-repository', type=str)
@click.option('--notion-token', type=str)
@click.option('--notion-page-id', type=str)
@click.option('--notion-db-title', type=str)
def cli(github_token, github_owner, github_repository, notion_token, notion_page_id, notion_db_title):
    github = GitHub(github_token)
    notion = Notion(github, page_id=notion_page_id, token=notion_token)
    notion.create(notion_db_title)
    issues = github.get_issues(github_owner, github_repository, "all")
    for issue in issues:
        comments = github.get_comments(issue.get("comments_url"))
        notion.post(issue, comments)


if __name__ == "__main__":
    cli()

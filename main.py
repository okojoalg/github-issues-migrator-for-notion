import click

from github import GitHub
from notion import Notion


@click.command()
@click.option('--github-token', type=str, default=None)
@click.option('--github-owner', type=str, required=True)
@click.option('--github-repository', type=str, required=True)
@click.option('--notion-token', type=str, required=True)
@click.option('--notion-page-id', type=str, required=True)
@click.option('--notion-db-title', type=str, required=True)
@click.option('--time-zone', type=str, default="UTC")
def cli(github_token, github_owner, github_repository, notion_token, notion_page_id, notion_db_title, time_zone):
    github = GitHub(github_token)
    notion = Notion(github, page_id=notion_page_id, token=notion_token, time_zone=time_zone)
    notion.create(notion_db_title)
    issues = github.get_issues(github_owner, github_repository, "all")
    for issue in issues:
        comments = github.get_comments(issue.get("comments_url"))
        notion.post(issue, comments)


if __name__ == "__main__":
    cli()

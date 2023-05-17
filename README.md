# GitHub Issues Migrator for Notion

## About The Project

Here is a template for migrating GitHub Issues to Notion's database. Please
customize it for your own organization and use it!!

## Prerequisites

### Personal access token

You have to create personal access token for GitHub if you don't have it. It
should have permission to access issues and pull-requests.

### Notion Page

You need create a notion page for database belong to.

### Integration token

You need integration token for Notion as this repository access Notion API and
write data to its database. First, create a new "Integration" associated with
your workspace. Second, get integration token for Notion API. Finally, you
should give permission, to use the Integration on, to the created page .

## Usage

Run the "Migration" workflow from the "Actions" page of your replicated
repository. You will be asked to enter the following information:

| Input             | Name                  | Description                                                                            |
|-------------------|-----------------------|----------------------------------------------------------------------------------------|
| github_token      | Your GitHub token     | Enter the personal access token you created.                                           |
| github_owner      | Repository owner name | Enter the owner of the repository where the issues you are migrating from are located. |
| github_repository | Repository name       | Enter the repository where the issues you are migrating from are located.              |
| notion_token      | Your Notion token     | Enter the integration token you created.                                               |
| notion_page_id    | Notion page ID        | Enter the parent page ID of the database you are migrating to.                         |
| notion_db_title   | Notion DB title       | Enter the title of the database  you are migrating to.                                 |
| time_zone         | Time Zone             | Enter time zone of your environment.                                                   |
# Deploy Test Repository

This directory contains files, that aim to create issues in a GitLab and GitHub test repository. This allows to use those two repos to test the main application.

## Repositories Layout

### GitLab Repo

Issue 1
Issue 2 (Modified)
Issue 3 (Deleted)
Issue 4 (Modified)
Issue 5
Issue 6 (Deleted)
Issue 7 (Deleted)
Issue 8 (Deleted)
Issue 9
Issue 10
Issue 11 (Deleted)

### GitHub Repo

Issue 1
Issue 2
Issue 3
Issue 4
Issue 5
Issue 6 (Deleted)
Issue 7 (Deleted)

## Results after executing Main Application

- Updated 2 issues (issue2, issue4)
- Added 2 issues (issue9, issue10)
- Added placeholder (ID:8)
- Undeleted issues (issue3)

## Usage

1. Create a new GitLab repository
2. Create a new GitHub repository
3. Adjust the created issues in the scripts as needed.
4. Create a "authorization.env" file in this directory.
5. Fill out following variables in that file:
  GITLAB_PROJECT_ID
  GITLAB_TOKEN
  GITHUB_REPO_NAME
  GITHUB_REPO_OWNER
  GITHUB_TOKEN
6. Execute *create_gitlab_test_repo.py*
7. Execute *create_github_test_repo.py*
8. Delete the issues that should already have been deleted.

# Deploy Test Repository

This directory contains files, that aim to create a GitLab and GitHub test repository.

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

1. Create a "authorization.env" file in this directory.
2. Fill out following variables in that file:
  GITLAB_PROJECT_ID
  GITLAB_TOKEN
  GITHUB_REPO_NAME
  GITHUB_REPO_OWNER
  GITHUB_TOKEN
3. Execute *create_gitlab_test_repo.py*
4. Execute *create_github_test_repo.py*

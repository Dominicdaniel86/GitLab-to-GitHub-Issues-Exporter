from additional_github_api_calls import check_github_issue_existance
from export_to_github import export_to_github
from read_in_github_format import read_from_github, read_from_gitlab

# adjust the following parameters:
gitlab_token: str = "glpat-CODE-CODE-CODE"
github_token: str = "ghp_CODE"
gitlab_project_id: str = "12345"
github_repo_owner: str = "MaxMustermann"
github_project_name: str = "Test"
number_of_issues: int = 10
import_assignees: bool = False

gitlab_url = f'https://gitlab.com/api/v4/projects/{gitlab_project_id}/issues'
github_url = f"https://api.github.com/repos/{github_repo_owner}/{github_project_name}/issues"

def main():
    # get gitlab issues
    gitlab_issues, max_gitlab_issue = read_from_gitlab(gitlab_url, gitlab_token)
    print(f"max GitLab issue: {max_gitlab_issue}")

    # get github issues
    github_issues, max_github_issue = read_from_github(github_url, github_token)
    print(f"max GitHub issue: {max_github_issue}")

    # get nr of hidden issues
    index = max_github_issue
    while True:
        index += 1
        if check_github_issue_existance(github_url, index, github_token) == "not created":
            break
    max_github_issue_hidden = index - 1
    print(f"max GitHub issue hidden: {max_github_issue_hidden}")

    # export to GitHub
    export_to_github(gitlab_issues, github_issues, max_gitlab_issue, max_github_issue, max_github_issue_hidden, github_url, github_token)


if __name__ == "__main__":
    main()

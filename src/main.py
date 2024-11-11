from read_in_github_format import read_from_github, read_from_gitlab

# adjust the following parameters:
gitlab_project_id: str = "12345"
github_repo_owner: str = "MaxMustermann"
github_project_name: str = "Test"
number_of_issues: int = 10
import_assignees: bool = False

gitlab_url = f'https://gitlab.com/api/v4/projects/{gitlab_project_id}/issues'
github_url = f"https://api.github.com/repos/{github_repo_owner}/{github_project_name}/issues?state=all"

def main():
    gitlab_issues = read_from_gitlab(gitlab_url)
    max_gitlab_issue = gitlab_issues[0].id
    gitlab_issues = gitlab_issues[::-1]
    print(max_gitlab_issue)

    github_issues = read_from_github(github_url)
    max_github_issue = github_issues[0].id
    github_issues = github_issues[::-1]
    print(max_github_issue)


if __name__ == "__main__":
    main()

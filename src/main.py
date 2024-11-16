from api.get import github_get, gitlab_get
from services.helper import get_hidden_github_issue_id
from services.issue_export import export_issues_to_github

# adjust the following parameters:
gitlab_token: str = "glpat-CODE-CODE-CODE"
github_token: str = "ghp_CODE"
gitlab_project_id: str = "12345"
github_repo_owner: str = "MaxMustermann"
github_project_name: str = "Test"
number_of_issues: int = 10
import_assignees: bool = False


# URLs for API requests
gitlab_url = f'https://gitlab.com/api/v4/projects/{gitlab_project_id}'
github_url = f"https://api.github.com/repos/{github_repo_owner}/{github_project_name}"

def main():
    gitlab_issues = gitlab_get.read_gitlab_issues(gitlab_url, gitlab_token)
    gitlab_max_id = max(gitlab_issues.keys())
    
    github_issues = github_get.read_github_issues(github_url, github_token)
    github_max_id = max(github_issues.keys())
    github_hidden_max_id = get_hidden_github_issue_id(github_url, github_token, github_max_id)

    print(f"debug: max GitLab ID = {gitlab_max_id}")
    print(f"debug: max GitHub ID = {github_max_id}")
    print(f"debug: max hidden GitHub ID = {github_hidden_max_id}")

    # check for not included assignee?

    # export issues to GitHub
    modified_issues, new_issues, undeleted_issues, new_placeholders, new_labels, missing_milestones, issues_with_missing_milestones = \
        export_issues_to_github(github_url, github_token, gitlab_issues, github_issues, gitlab_max_id, github_max_id, github_hidden_max_id)
    
    print(f"Updated {len(modified_issues)} issues: {modified_issues}")
    print(f"Created {len(new_issues)} new issues: {new_issues}")
    print(f"{len(undeleted_issues)} undeleted issues: {undeleted_issues}")
    print(f"Created {len(new_placeholders)} placeholders: {new_placeholders}")
    print(f"Created {len(new_labels)} new labels: {new_labels}")
    print(f"{len(missing_milestones)} missing milestones: {missing_milestones}")
    print(f"Issues with missing milestones: {issues_with_missing_milestones}")

if __name__ == "__main__":
    main()

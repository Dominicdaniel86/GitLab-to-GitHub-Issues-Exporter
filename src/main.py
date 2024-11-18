from api.get import github_get, gitlab_get
from services.filter_issues import filter_all_options, filter_assingees, filter_labels
from services.helper import get_hidden_github_issue_id
from services.issue_export import export_issues_to_github

# adjust the following parameters:
gitlab_token: str = "glpat-CODE-CODE-CODE"
github_token: str = "ghp_CODE"
gitlab_project_id: str = "12345"
github_repo_owner: str = "MaxMustermann"
github_project_name: str = "Test"
number_of_issues: int = 10 # temporary

# customization
migrate_options = ["labels", "milestones", "assignees", "description", "comments"] # can include "labels", "milestones", "assignees", "description" and "comments"

one_time_export: bool = False # doesn't add placeholders
let_placeholders_be_closed: bool = True # does add placeholders as closed issues
create_missing_labels: bool = True # creates missing labels
import_assignees: str = "if_possible" # must either be "if_possible", "no" or "yes"
placeholder_options = [let_placeholders_be_closed, create_missing_labels]

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

    # read GitHub comments
    github_comments = {}
    if "comments" in migrate_options:
        for current_issue in github_issues.values():
            comments = github_get.read_comments(github_url, github_token, current_issue.id)
            github_comments[current_issue.id] = comments

    # read GitLab comments
    gitlab_comments = {}
    if "comments" in migrate_options:
        for current_issue in gitlab_issues.values():
            comments = gitlab_get.read_comments(gitlab_url, gitlab_token, current_issue.id)
            gitlab_comments[current_issue.id] = comments

    filter_all_options(gitlab_issues, github_issues, migrate_options)

    # filter for (not) included assignees
    try:
        filter_assingees(github_url, github_token, gitlab_issues, import_assignees)
    except ValueError as e:
        print(f"error - {e}")
        return

    # filter for (not) included labels
    if create_missing_labels == False:
        filter_labels(github_url, github_token, gitlab_issues)

    # export issues to GitHub
    modified_issues, new_issues, undeleted_issues, new_placeholders, new_labels, missing_milestones, issues_with_missing_milestones = \
        export_issues_to_github(github_url, github_token, gitlab_issues, github_issues, gitlab_max_id, github_max_id, github_hidden_max_id, placeholder_options)
    
    print(f"Updated {len(modified_issues)} issues: {modified_issues}")
    print(f"Created {len(new_issues)} new issues: {new_issues}")
    print(f"{len(undeleted_issues)} undeleted issues: {undeleted_issues}")
    print(f"Created {len(new_placeholders)} placeholders: {new_placeholders}")
    print(f"Created {len(new_labels)} new labels: {new_labels}")
    print(f"{len(missing_milestones)} missing milestones: {missing_milestones}")
    print(f"Issues with missing milestones: {issues_with_missing_milestones}")

if __name__ == "__main__":
    main()

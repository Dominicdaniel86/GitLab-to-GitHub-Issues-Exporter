import os
from dotenv import load_dotenv
from api.get import github_get, gitlab_get
from services.filter_issues import filter_all_options, filter_assingees, filter_labels, filter_pipeline
from services.helper import get_hidden_github_issue_id
from services.issue_export import export_comments_to_github, export_issues_to_github

# updated customization
migrate_labels: bool = True
create_missing_labels: bool = True

# customization
migrate_options = ["milestones", "assignees", "description", "comments"] # can include "milestones", "assignees", "description" and "comments"

# customization - placeholders
let_placeholders_be_closed: bool = True # does add placeholders as closed issues

# customization - assignees
import_assignees: str = "if_possible" # must either be "if_possible", "no" or "yes"

# customization - comments
delete_missing_comments = True # deletes all comments that are not found on GitLab

placeholder_options = [let_placeholders_be_closed, create_missing_labels]

# URLs for API requests
gitlab_url = f'https://gitlab.com/api/v4/projects/{os.getenv("GITLAB_PROJECT_ID")}'
github_url = f"https://api.github.com/repos/{os.getenv("GITHUB_REPO_OWNER")}/{os.getenv("GITHUB_REPO_NAME")}"

def main():
    load_dotenv("github_issue_exporter.env")

    # read issues and max IDs
    gitlab_issues = gitlab_get.read_gitlab_issues(gitlab_url)
    gitlab_max_id = max(gitlab_issues.keys())
    
    github_issues = github_get.read_github_issues(github_url)
    github_max_id = max(github_issues.keys())
    github_hidden_max_id = get_hidden_github_issue_id(github_url, github_max_id)

    print(f"debug: max GitLab ID = {gitlab_max_id}")
    print(f"debug: max GitHub ID = {github_max_id}")
    print(f"debug: max hidden GitHub ID = {github_hidden_max_id}")

    # read GitHub comments
    github_comments = {}
    if "comments" in migrate_options:
        for current_issue in github_issues.values():
            if current_issue.comments != 0:
                comments = github_get.read_comments(github_url, current_issue.id)
                github_comments[current_issue.id] = comments

    # read GitLab comments
    gitlab_comments = {}
    if "comments" in migrate_options:
        for current_issue in gitlab_issues.values():
            if current_issue.comments != 0:
                comments = gitlab_get.read_comments(gitlab_url, current_issue.id)
                gitlab_comments[current_issue.id] = comments
    
    # filter
    filter_pipeline(github_url, gitlab_issues, github_issues, migrate_options, migrate_labels, import_assignees, create_missing_labels)

    # export issues to GitHub
    modified_issues, new_issues, undeleted_issues, new_placeholders, new_labels, missing_milestones, issues_with_missing_milestones = \
        export_issues_to_github(github_url, gitlab_issues, github_issues, gitlab_max_id, github_max_id, github_hidden_max_id, placeholder_options)
    
    # lists for comment changes
    updated_comments = [0, []]
    deleted_comments = [0, []]

    # export comments go GitHub
    if "comments" in migrate_options:
        updated_comments, deleted_comments = export_comments_to_github(github_url, gitlab_comments, github_comments, delete_missing_comments)
    
    updated_comments[1].sort()
    deleted_comments[1].sort()
    
    print(f"Updated {len(modified_issues)} issues: {modified_issues}")
    print(f"Created {len(new_issues)} new issues: {new_issues}")
    print(f"{len(undeleted_issues)} undeleted issues: {undeleted_issues}")
    print(f"Created {len(new_placeholders)} placeholders: {new_placeholders}")
    print(f"Created {len(new_labels)} new labels: {new_labels}")
    print(f"{len(missing_milestones)} missing milestones: {missing_milestones}")
    print(f"Issues with missing milestones: {issues_with_missing_milestones}")

    print(f"Added {updated_comments[0]} comments for issues {updated_comments[1]}")
    print(f"Deleted {deleted_comments[0]} comments for issues {deleted_comments[1]}")

    input("Please enter to exit...")

if __name__ == "__main__":
    main()

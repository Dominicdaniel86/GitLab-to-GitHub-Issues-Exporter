import os
from api.get import github_get


def filter_pipeline(github_url, gitlab_issues, github_issues, migrate_labels, migrate_assignees, create_missing_labels, migrate_milestones):
    
    filter_all_options(gitlab_issues, github_issues, migrate_labels, migrate_milestones)
    # filter for (not) included assignees
    try:
        filter_assingees(github_url, gitlab_issues)
    except ValueError as e:
        print(f"error - {e}")
        return
    # filter for (not) included labels
    if create_missing_labels == False:
        filter_labels(github_url, gitlab_issues)

def filter_all_options(gitlab_issues, github_issues, migrate_labels, migrate_milestones, migrate_assignees, migrate_description):
    # filter labels
    if not migrate_labels:
        for single_issue in gitlab_issues.values():
            single_issue.labels = github_issues[single_issue.id].labels

    # filter milestones
    if not migrate_milestones:
        for single_issue in gitlab_issues.values():
            single_issue.milestone_title = github_issues[single_issue.id].milestone_title

    # fiter assignees
    if not migrate_assignees:
        for single_issue in gitlab_issues.values():
            single_issue.assignees = github_issues[single_issue.id].assignees
    
    # filter description
    if not migrate_description:
        for single_issue in gitlab_issues.values():
            single_issue.description = github_issues[single_issue.id].description


def filter_assingees(github_url, gitlab_issues, migrate_assignees, missing_assignees_stop_migration):
    # if "no": remove all asssignees
    if not migrate_assignees:
        for current_issue in gitlab_issues.values():
            current_issue.assignees = []
        return

    collaborators = github_get.read_collaborators(github_url)

    for current_issue in gitlab_issues.values():
        filtered_assignees = []
        for current_assignee in current_issue.assignees:
            if current_assignee in collaborators and not missing_assignees_stop_migration:
                # if "if_possible": remove assingees that are not present on GitHub
                filtered_assignees.append(current_assignee)
            elif current_assignee not in collaborators and missing_assignees_stop_migration and migrate_assignees:
                # if "no": return error if assignee does not exist                
                raise ValueError(f"{current_assignee} is not in GitHub collaborators")
                # if "no": return error
                # might be best to implement a class "AssigneeError"
        current_issue.assignees = filtered_assignees

def filter_labels(github_url, gitlab_issues):

    issues = github_get.read_labels(github_url)

    for current_issue in gitlab_issues.values():
        filtered_labels = []
        for current_label in current_issue.labels:
            if current_label in issues:
                filtered_labels.append(current_label)
        current_issue.labels = filtered_labels

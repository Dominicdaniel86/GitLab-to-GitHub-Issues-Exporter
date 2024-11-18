from api.get import github_get


def filter_all_options(gitlab_issues, github_issues, migrate_options):
    # filter labels
    if "labels" not in migrate_options:
        for single_issue in gitlab_issues.values():
            single_issue.labels = github_issues[single_issue.id].labels

    # filter milestones
    if "milestones" not in migrate_options:
        for single_issue in gitlab_issues.values():
            single_issue.milestone_title = github_issues[single_issue.id].milestone_title

    # fiter assignees
    if "assignees" not in migrate_options:
        for single_issue in gitlab_issues.values():
            single_issue.assignees = github_issues[single_issue.id].assignees
    
    # filter description
    if "description" not in migrate_options:
        for single_issue in gitlab_issues.values():
            single_issue.description = github_issues[single_issue.id].description


def filter_assingees(github_url, github_token, gitlab_issues, import_assignees):
    # if "no": remove all asssignees
    if import_assignees == "no":
        for current_issue in gitlab_issues.values():
            current_issue.assignees = []
        return

    collaborators = github_get.read_collaborators(github_url, github_token)

    for current_issue in gitlab_issues.values():
        filtered_assignees = []
        for current_assignee in current_issue.assignees:
            if current_assignee in collaborators and import_assignees == "if_possible":
                # if "if_possible": remove assingees that are not present on GitHub
                filtered_assignees.append(current_assignee)
            elif current_assignee not in collaborators and import_assignees == "yes":
                # if "no": return error if assignee does not exist                
                raise ValueError(f"{current_assignee} is not in GitHub collaborators")
                # if "no": return error
                # might be best to implement a class "AssigneeError"
        current_issue.assignees = filtered_assignees

def filter_labels(github_url, github_token, gitlab_issues):

    issues = github_get.read_labels(github_url, github_token)

    for current_issue in gitlab_issues.values():
        filtered_labels = []
        for current_label in current_issue.labels:
            if current_label in issues:
                filtered_labels.append(current_label)
        current_issue.labels = filtered_labels

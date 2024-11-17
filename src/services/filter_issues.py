from api.get import github_get


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

def filter_labels():
    pass
from api.get import github_get
from api.modify.github_modify import create_github_issue, update_github_issue
from services.helper import get_not_included_labels, get_not_included_milestones


def export_issues_to_github(github_url, github_token, gitlab_issues, github_issues, gitlab_max_id, github_max_id, github_hidden_max_id):
    
    # needed lists
    modified_issues = [] # { id, title }
    new_issues = [] # { id, title }
    undeleted_issues = [] # { id, title }
    new_placeholders = [] # {id}
    new_labels = [] # { name }
    missing_milestones = [] # { name }

    # determine new labels
    labels = github_get.read_labels(github_url, github_token)
    new_labels = get_not_included_labels(gitlab_issues, labels)

    # determine missing milestones
    milestones = github_get.read_milestones(github_url, github_token)
    missing_milestones = get_not_included_milestones(gitlab_issues, milestones)

    # replace GitLab Milestones with GitHub IDs
    for current_issue in gitlab_issues.values():
        for key, val in milestones.items():
            if current_issue.milestone_title == val:
                current_issue.milestone_id = key

    # determine undeleted issues on GitHub
    for key in github_issues:
        if key not in gitlab_issues:
            undeleted_issues.append([key, github_issues[key].title])
    
    # check which issues have been modified
    for key in gitlab_issues:
        if key <= github_max_id:
            if not github_issues[key] == gitlab_issues[key]:
                modified_issues.insert(0, [key, gitlab_issues[key].title])
    
    # update all modified issues
    for current_issue in modified_issues:
        update_github_issue(github_url, github_token, gitlab_issues[current_issue[0]])

    # create missing issues and/ or placeholders
    for index in range(github_hidden_max_id + 1, gitlab_max_id + 1):
        if index not in gitlab_issues:
            create_github_issue(github_url, github_token, {"title": "placeholder"})
            new_placeholders.append(index)
        else:
            create_github_issue(github_url, github_token, gitlab_issues[index])
            new_issues.append([index, gitlab_issues[index].title])
            # close new issue, if it's already closed on GitLab
            if gitlab_issues[index].state == "closed":
                update_github_issue(github_url, github_token, gitlab_issues[index])
    
    # return results
    return modified_issues, new_issues, undeleted_issues, new_placeholders, new_labels, missing_milestones

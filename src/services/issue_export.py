from api.get import github_get
from api.modify.github_modify import create_github_comment, create_github_issue, delete_github_comment, update_github_issue
from services.helper import contains_comment, get_not_included_labels, get_not_included_milestones


def export_issues_to_github(github_url, github_token, gitlab_issues, github_issues, gitlab_max_id, github_max_id, github_hidden_max_id, placeholders_options):
    
    # needed lists
    modified_issues = [] # { id, title }
    new_issues = [] # { id, title }
    undeleted_issues = [] # { id, title }
    new_placeholders = [] # {id}
    new_labels = [] # { name }
    missing_milestones = [] # { name }
    issues_with_missing_milestones = [] # { id, title }

    # determine new labels
    labels = github_get.read_labels(github_url, github_token)
    new_labels = get_not_included_labels(gitlab_issues, labels)

    # determine missing milestones
    milestones = github_get.read_milestones(github_url, github_token)
    missing_milestones, issues_with_missing_milestones = get_not_included_milestones(gitlab_issues, milestones)

    # replace GitLab Milestones with GitHub IDs
    for current_issue in gitlab_issues.values():
        for key, val in milestones.items():
            if current_issue.milestone_title == val:
                current_issue.milestone_id = key
    # remove GitLab IDs, when no matching Milestone exists
    # this will lead to not trying to add a milestone when calling the API
    # also replace the title with the matching GitHub title, so it will not be updated,
    # if no other value is different from each other
    for current_issue in gitlab_issues.values():
        if current_issue.milestone_title in missing_milestones:
            current_issue.milestone_id = None
            if current_issue.id in github_issues:
                current_issue.milestone_title = github_issues[current_issue.id].milestone_title

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
            if placeholders_options[0] == True:
                update_github_issue(github_url, github_token, {"id": index, "title": "placeholder", "state": "closed"})
        else:
            create_github_issue(github_url, github_token, gitlab_issues[index])
            new_issues.append([index, gitlab_issues[index].title])
            # close new issue, if it's already closed on GitLab
            if gitlab_issues[index].state == "closed":
                update_github_issue(github_url, github_token, gitlab_issues[index])
    
    # return results
    return modified_issues, new_issues, undeleted_issues, new_placeholders, new_labels, missing_milestones, issues_with_missing_milestones

def export_comments_to_github(github_url, github_token, gitlab_comments, github_comments, delete_missing_comments):
    updated_comments = []
    deleted_comments = []    
    
    # add missing comments
    for key in gitlab_comments.keys():
        if key not in github_comments: # then create all comments
            for current_comment in gitlab_comments[key]:
                create_github_comment(github_url, github_token, key, current_comment[0])

        else:
            while(len(gitlab_comments[key]) != 0):
                contained, index = contains_comment(gitlab_comments[key][0][0], github_comments[key])
                if not contained:
                    create_github_comment(github_url, github_token, key, gitlab_comments[key][0][0])
                    gitlab_comments[key].pop(0)
                else:
                    gitlab_comments[key].pop(0)
                    github_comments[key].pop(index)
            
            if delete_missing_comments:
                for reamining_comment in github_comments[key]:
                    delete_github_comment(github_url, github_token, reamining_comment[1])

    return updated_comments, deleted_comments
    
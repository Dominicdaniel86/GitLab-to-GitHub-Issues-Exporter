from api.get.github_get import check_if_github_issue_exists


def get_hidden_github_issue_id(url, token, max_visible_issue_id):
    index = max_visible_issue_id

    while True:
        index += 1
        if not check_if_github_issue_exists(url, index, token):
            break
    
    index -= 1
    return index

def get_not_included_labels(issues, existing_labels):
    new_labels = []

    for current_issue in issues.values():
        for issue_label in current_issue.labels:
            if issue_label not in existing_labels and issue_label not in new_labels:
                new_labels.append(issue_label)
    
    return new_labels

def get_not_included_milestones(issues, existing_milestones):
    missing_milestones = []

    for current_issue in issues.values():
        if current_issue.milestone not in existing_milestones and current_issue.milestone not in missing_milestones:
            missing_milestones.append(current_issue.milestone)

    missing_milestones.remove(None)    
    return missing_milestones

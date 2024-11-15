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

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
    issues_with_missing_milestones = []

    for current_issue in issues.values():
        if current_issue.milestone_title not in existing_milestones.values() and current_issue.milestone_title not in missing_milestones and current_issue.milestone_title != None:
            missing_milestones.append(current_issue.milestone_title)
            issues_with_missing_milestones.append([current_issue.id, current_issue.title])

    return missing_milestones, issues_with_missing_milestones

# returns True and index or False and 0
def contains_comment(single_comment, dictionary_entry):
    index = 0
    for sublist in dictionary_entry:
        if single_comment in sublist[0]:
            return True, index
        index += 1
    return False, 0

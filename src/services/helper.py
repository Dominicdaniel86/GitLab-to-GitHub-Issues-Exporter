from api.get.github_get import check_if_github_issue_exists


def get_hidden_github_issue_id(url, token, max_visible_issue_id):
    index = max_visible_issue_id

    while True:
        index += 1
        if not check_if_github_issue_exists(url, index, token):
            break
    
    index -= 1
    return index

import requests


def create_github_issue(url, token, issue):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/vnd.github+json'
    }
    if not isinstance(issue, dict):
        issue = issue.to_create_dict()
    
    try:
        response = requests.post(f"{url}/issues",
                                 json = issue,
                                 headers = headers)
        
        if response.status_code != 201:
            print(f"error: failed to create GitHub issue (status code: {response.status_code})")
            return
        # print(f"debug: created a new GitHub issue - ID: {issue['id']}, Title: {issue['title']}")
        print(f"debug: created a new GitHub issue - {issue['title']}")

    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to create a GitHub issue - {e}")


def update_github_issue(url, token, issue):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/vnd.github+json'
    }
    if not isinstance(issue, dict):
        issue = issue.to_update_dict()
    
    try:
        response = requests.patch(f"{url}/issues/{issue['id']}",
                                 json = issue,
                                 headers = headers)
        
        if response.status_code != 200:
            print(f"error: failed to update GitHub issue (status code: {response.status_code})")
            return
        print(f"debug: updated a GitHub issue - ID: {issue['id']}, Title: {issue['title']}")

    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to update a GitHub issue - {e}")

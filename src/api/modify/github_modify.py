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

def create_github_comment(url, token, issue_id, body):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/vnd.github+json'
    }
    json_body = {
        'body': body
    }

    try:
        response = requests.post(f"{url}/issues/{issue_id}/comments",
                                 json = json_body,
                                 headers = headers)

        if response.status_code != 201:
            print(f"error: failed to create GitHub comment (status code: {response.status_code})")
            return
        print(f"debug: created a GitHub comment - Issue-ID: {issue_id}, Body: {body}")

    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to update a GitHub issue - {e}")

def delete_github_comment(url, token, comment_id):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/vnd.github+json'
    }

    try:
        response = requests.delete(f"{url}/issues/comments/{comment_id}",
                                 headers = headers)

        if response.status_code != 204:
            print(f"error: failed to delete GitHub comment (status code: {response.status_code})")
            return
        print(f"debug: deleted a GitHub comment - Issue-ID: {comment_id}")

    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to update a GitHub issue - {e}")

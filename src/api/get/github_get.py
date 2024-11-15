import requests

from models.issue import Issue


def read_github_issues(url, token):
    issues = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }
    try:
        response = requests.get(f"{url}/issues?state=all",
                                headers=headers)
        if response.status_code != 200:
            print(f"error: failed to retrieve GitHub issues (status code: {response.status_code})")
            return
        data = response.json()
        
        for current_issue in data:
            id = int(current_issue['number'])
            title = current_issue['title']
            # description
            labels = []
            for current_label in current_issue['labels']:
                labels.append(current_label['name'])

            state = current_issue['state']

            milestone = None
            if current_issue['milestone'] is not None:
                milestone = current_issue['milestone']['number']

            assignees = []
            for current_assignee in current_issue['assignees']:
                assignees.append(current_assignee['login'])

            new_issue = Issue(id, title, "", labels, state, milestone, assignees)
            issues[int(id)] = new_issue

        print(f"debug: read {len(issues)} issues from GitHub API")
        return issues

    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to retrieve GitHub issues - {e}")


def check_if_github_issue_exists(url, issue_id, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    try:
        response = requests.get(f'{url}/issues/{issue_id}',
                                headers=headers)
        if response.status_code == 200:
            return True # exists
        elif response.status_code == 404:
            return False # not created
        elif response.status_code == 410:
            return True # deleted
        else:
            print(f"error: received unexpected error code while trying to check if GitHub issue exists - {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to check if GitHub issue exists - {e}")


def read_comments():
    pass

def read_labels(url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    labels = []
    try:
        response = requests.get(f'{url}/labels',
                                headers=headers)
        if response.status_code != 200:
            print(f"error: received unexpected error code while trying to retrieve GitHub labels - {response.status_code}")
            return
        
        data = response.json()
        for current_milestone in data:
            labels.append(current_milestone['name'])
        return labels
    
    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to retrieve GitHub labels - {e}")

def read_milestones(url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    milestones = []
    try:
        response = requests.get(f'{url}/milestones',
                                headers=headers)
        if response.status_code != 200:
            print(f"error: received unexpected error code while trying to retrieve GitHub milestones - {response.status_code}")
            return
        
        data = response.json()
        for current_milestone in data:
            milestones.append(current_milestone['title'])
        return milestones
    
    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to retrieve GitHub milestones - {e}")

def read_asignees():
    pass

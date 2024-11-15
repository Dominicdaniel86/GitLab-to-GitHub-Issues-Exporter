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
            id = current_issue['number']
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


def read_comments():
    pass

def read_labels():
    pass

def read_milestones():
    pass

def read_asignees():
    pass

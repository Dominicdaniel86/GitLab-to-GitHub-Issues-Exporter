import requests

from models.issue import Issue


def read_gitlab_issues(url, token):
    issues = {}
    headers = {
        'PRIVATE-TOKEN': f'{token}'
    }
    try:
        response = requests.get(f'{url}/issues',
                                headers=headers,
                                params={'per_page': 100, 'page': 1})
        if response.status_code != 200:
            print(f"error: failed to retrieve GitLab issues (status code: {response.status_code})")
            return
        data = response.json()

        for current_issue in data:
            id = current_issue['references']['short'][1:]
            title = current_issue['title']
            description = current_issue['description']
            labels = current_issue['labels']

            state = current_issue['state']
            if state == "opened":
                state = "open"

            milestone = None
            if current_issue['milestone'] is not None:
                milestone = current_issue['milestone']['iid']
            
            assignees = []
            for current_assignee in current_issue['assignees']:
                assignees.append(current_assignee['username'])

            new_issue = Issue(id, title, description, labels, state, milestone, assignees)
            issues[id] = new_issue
        
        print(f"debug: read {len(issues)} issues from GitLab API")
        return issues

    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to retrieve GitLab issues - {e}")

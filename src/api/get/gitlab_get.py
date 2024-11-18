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
            id = int(current_issue['references']['short'][1:])
            title = current_issue['title']
            description = current_issue['description']
            labels = current_issue['labels']

            state = current_issue['state']
            if state == "opened":
                state = "open"

            milestone_title = None
            if current_issue['milestone'] is not None:
                milestone_title = current_issue['milestone']['title']
            
            milestone_id = None
            if current_issue['milestone'] is not None:
                milestone_id = current_issue['milestone']['iid']
            
            assignees = []
            for current_assignee in current_issue['assignees']:
                assignees.append(current_assignee['username'])
            
            comments = current_issue['user_notes_count']

            new_issue = Issue(id, title, description, labels, state, milestone_id, milestone_title, assignees, comments)
            issues[int(id)] = new_issue
        
        print(f"debug: read {len(issues)} issues from GitLab API")
        return issues

    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to retrieve GitLab issues - {e}")

def read_comments(url, token, issue_id):
    headers = {
        'PRIVATE-TOKEN': f'{token}'
    }
    comments = []
    try:
        response = requests.get(f'{url}/issues/{issue_id}/notes',
                                headers=headers)
        if response.status_code != 200:
            print(f"error: received unexpected error code while trying to retrieve GitLab issues - {response.status_code}")
            return
        
        data = response.json()
        for current_comment in data:
            if current_comment['system'] == False:
                comments.append([current_comment['body'], current_comment['id']])
        return comments

    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to retrieve GitLab comments - {e}")

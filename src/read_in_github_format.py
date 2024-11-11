import requests

from objects import GitHubIssue

def read_from_gitlab(url, token):
    issues = []
    headers = { 'PRIVATE-TOKEN': f'{token}'}
    try:
        response = requests.get(url,
                                headers=headers,
                                params={'per_page': 100, 'page': 1})
        if response.status_code == 200:
            data = response.json()
            for d in data:
                id = d['references']['short']
                title = d['title']
                description = d['description']
                labels = d['labels']
                assignees = d['assignees']
                state = d['state']
                state_reason = None
                milestone = None

                if d['milestone'] is not None:
                    milestone = d['milestone']['iid']

                new_issue = GitHubIssue(id, title, description, milestone, labels, assignees, state, state_reason)
                issues.append(new_issue)
            return issues

        else:
            print("failed to retrieve data (status code: " + str(response.status_code) + ")")

    except requests.exceptions.RequestException as e:
        print("An error occured", e)


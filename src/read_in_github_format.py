import requests

from objects import GitHubIssue

def read_from_gitlab(url, token):
    issues = {}
    highest_id = 0
    headers = { 'PRIVATE-TOKEN': f'{token}'}
    try:
        response = requests.get(url,
                                headers=headers,
                                params={'per_page': 100, 'page': 1})
        if response.status_code == 200:
            data = response.json()
            if len(data) != 0:
                highest_id = data[0]['references']['short'][1:]

            for d in data:
                id = int(d['references']['short'][1:])
                title = d['title']
                description = d['description']
                labels = d['labels']
                assignees = d['assignees']
                state = d['state']
                if state == "opened":
                    state = "open"
                milestone = None

                if d['milestone'] is not None:
                    milestone = d['milestone']['iid']

                new_issue = GitHubIssue(id, title, description, milestone, labels, assignees, state)
                issues[id] = new_issue
            return issues, int(highest_id)

        else:
            print("failed to retrieve data (status code: " + str(response.status_code) + ")")

    except requests.exceptions.RequestException as e:
        print("An error occured", e)


def read_from_github(url, token):
    headers = { 'Authorization': f'Bearer {token}'}
    issues = {}
    highest_id = 0
    try:
        response = requests.get(url + "?state=all",
                                headers=headers)
        if response.status_code == 200:
            data = response.json()
            if len(data) != 0:
                highest_id = data[0]['number']

            for d in data:
                id = int(d['number'])
                title = d['title']
                # description: TODO
                if d['milestone'] is not None:
                    milestone = d['milestone']['number']
                else:
                    milestone = None
                labels = []
                for l in d['labels']:
                    labels.append(l['name'])
                assignees = []
                for a in d['assignees']:
                    assignees.append(a['login'])
                state = d['state']

                new_issue = GitHubIssue(id, title, "description", milestone, labels, assignees, state)
                issues[id] = new_issue
            return issues, int(highest_id)

        else:
            print("failed to retrieve data (status code: " + str(response.status_code) + ")")

    except requests.exceptions.RequestException as e:
        print("An error occured", e)

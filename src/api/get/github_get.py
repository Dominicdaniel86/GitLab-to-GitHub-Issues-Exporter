import os
import requests

from models.issue import Issue


def read_github_issues(url):
    issues = {}
    headers = {
        'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}'
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
            description = current_issue['body']
            if description == None:
                description = ""
            labels = []
            for current_label in current_issue['labels']:
                labels.append(current_label['name'])

            state = current_issue['state']

            milestone_title = None
            if current_issue['milestone'] is not None:
                milestone_title = current_issue['milestone']['title']

            milestone_id = None
            if current_issue['milestone'] is not None:
                milestone_id = current_issue['milestone']['number']

            assignees = []
            for current_assignee in current_issue['assignees']:
                assignees.append(current_assignee['login'])
            
            comments = current_issue['comments']

            new_issue = Issue(id, title, description, labels, state, milestone_id, milestone_title, assignees, comments)
            issues[int(id)] = new_issue

        print(f"debug: read {len(issues)} issues from GitHub API")
        return issues

    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to retrieve GitHub issues - {e}")


def check_if_github_issue_exists(url, issue_id):
    headers = {
        'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}'
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


def read_comments(url, issue_id):
    headers = {
        'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}'
    }
    comments = []
    try:
        response = requests.get(f'{url}/issues/{issue_id}/comments',
                                headers=headers)
        if response.status_code != 200:
            print(f"error: received unexpected error code while trying to retrieve GitHub issues - {response.status_code}")
            return

        data = response.json()
        for current_comment in data:
            comments.append([current_comment['body'], current_comment['id']])
        return comments
    
    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to retrieve GitHub comments - {e}")

def read_labels(url):
    headers = {
        'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}'
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

def read_milestones(url):
    headers = {
        'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}'
    }
    milestones = {} # id: title
    try:
        response = requests.get(f'{url}/milestones',
                                headers=headers)
        if response.status_code != 200:
            print(f"error: received unexpected error code while trying to retrieve GitHub milestones - {response.status_code}")
            return
        
        data = response.json()
        for current_milestone in data:
            milestones[current_milestone['number']] = current_milestone['title']
        return milestones
    
    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to retrieve GitHub milestones - {e}")

def read_collaborators(url):
    headers = {
        'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}'
    }
    collaborators = [] # name
    try:
        response = requests.get(f'{url}/collaborators',
                                headers=headers)
        if response.status_code != 200:
            print(f"error: received unexpected error code while trying to retrieve GitHub collaborators - {response.status_code}")
            return
        
        data = response.json()
        for current_collaborators in data:
            collaborators.append(current_collaborators['login'])
        return collaborators
    
    except requests.exceptions.RequestException as e:
        print(f"error: an error occured while trying to retrieve GitHub collaborators - {e}")

import json
import requests

def export_to_github(new_issues, original_issues, max_gitlab_issue, max_github_issue, max_github_issue_hidden, github_url, token):

    # initialize needed lists
    undeleted_issues = []
    modified_issues = []
    added_issues = []
    added_placeholders = []
    
    # determine the undeleted issues on GitHub
    for key in original_issues:
        if key not in new_issues:
            undeleted_issues.append([original_issues[key].id,original_issues[key].title])

    # check all issues that have been modified
    for key in new_issues:
        if key <= max_github_issue:
            if not new_issues[key] == original_issues[key]:
                modified_issues.insert(0, [new_issues[key].id, new_issues[key].title])

    # update all issues that have been modified
    for m in modified_issues:
        modify_issue(new_issues[m[0]], github_url, token, m[0])

    # add missing issues
    for index in range(max_github_issue_hidden+1, max_gitlab_issue+1):
        if index not in new_issues:
            added_placeholders.append(index)
            add_new_issue({"title": "placeholder"}, github_url, token)
        else:
            added_issues.append([new_issues[index].id, new_issues[index].title])
            add_new_issue(new_issues[index], github_url, token)

    # print results
    print(f"issues modified: {modified_issues}")
    print(f"issues added: {added_issues}")
    print(f"placeholders added: {added_placeholders}")
    print(f"issues to delete: {undeleted_issues}")

def add_new_issue(issue, github_url, token):
    if not isinstance(issue, dict):
        issue = issue.to_add_dict()
    headers = { 'Authorization': f'Bearer {token}', 'accept': 'application/vnd.github+json'}

    try:
        response = requests.post(github_url,
                                 json = issue,
                                 headers= headers)
        
        if response.status_code != 201:
            print("failed to retrieve data (status code: " + str(response.status_code) + ")")
        
    except requests.exceptions.RequestException as e:
        print("An error occured", e)


def modify_issue(issue, github_url, token, id):
    issue_dict = issue.to_modify_dict()
    headers = { 'Authorization': f'Bearer {token}', 'accept': 'application/vnd.github+json'}

    try:
        response = requests.patch(f"{github_url}/{id}",
                                 json = issue_dict,
                                 headers= headers)
        
        if response.status_code != 200:
            print("failed to retrieve data (status code: " + str(response.status_code) + ")")
            print(response.json())
        
    except requests.exceptions.RequestException as e:
        print("An error occured", e)

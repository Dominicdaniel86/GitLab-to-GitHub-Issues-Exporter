import os
import requests

project_id = os.getenv('PROJECT_ID')

url = f'https://gitlab.com/api/v4/projects/{project_id}/issues'

try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for d in data:
            print("title: " + str(d['title']))
            print("body: " + str(d['description']))
            print("assignee: " + str(d['assignee']))
            print("assignees: " + str(d['assignees']))
            if d['milestone'] is not None:
                print("milestone: " + str(d['milestone']['iid']))
            print("labels: " + str(d['labels']))
            print("issue_number: " + str(d['references']['short']))
            print("state: " + str(d['state']))
            print("")
    else:
        print("failed to retrieve data (status code: " + str(response.status_code) + ")")

except requests.exceptions.RequestException as e:
    print("An error occured", e)

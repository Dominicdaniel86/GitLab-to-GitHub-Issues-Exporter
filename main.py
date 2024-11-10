import os
import requests

project_id = os.getenv('PROJECT_ID')

url = f'https://gitlab.com/api/v4/projects/{project_id}/issues'

try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data[0])
    else:
        print("failed to retrieve data (status code: " + response.status_code + ")")

except requests.exceptions.RequestException as e:
    print("An error occured", e)

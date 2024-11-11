import requests

def check_github_issue_existance(url, number, token):
    url = url + "/" + str(number)
    headers = { 'Authorization': f'Bearer {token}' }
    try:
        response = requests.get(url,
                                headers=headers)
        if response.status_code == 200:
            return "exists"
        elif response.status_code == 410:
            return "deleted"
        elif response.status_code == 404:
            return "not created"
        else:
            print("failed to retrieve data (status code: " + str(response.status_code) + ")")

    except requests.exceptions.RequestException as e:
        print("An error occured", e)

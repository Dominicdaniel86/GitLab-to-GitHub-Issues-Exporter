import os

from read_in_github_format import read_from_gitlab

project_id = os.getenv('PROJECT_ID')
url = f'https://gitlab.com/api/v4/projects/{project_id}/issues'


def main():
    issues = read_from_gitlab(url)
    issues = issues[::-1]


if __name__ == "__main__":
    main()

import os

from read_from_gitlab import read_from_gitlab

project_id = os.getenv('PROJECT_ID')
url = f'https://gitlab.com/api/v4/projects/{project_id}/issues'


def main():
    issues = read_from_gitlab(url)


if __name__ == "__main__":
    main()

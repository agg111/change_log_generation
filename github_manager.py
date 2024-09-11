import requests
import os
from datetime import datetime, timedelta

from greptile_manager import prepare_change_log

from dotenv import load_dotenv, dotenv_values

load_dotenv()

GITHUB_PAT = os.getenv("GITHUB_PAT")
GREPTILE_KEY = os.getenv("GREPTILE_KEY")

def get_repositories():
    url = 'http://localhost:3000/get-repositories'
    response = requests.get(url)

    if response.status_code == 200:
        # Assuming the response is JSON
        repositories = response.json()
        for repo in repositories:
            print(repo['name'])
    else:
        print(f"Failed to fetch repositories: {response.status_code}")

def get_commits(time_period=7):
    print("commit time == ", time_period)
    params = {
    'owner': 'vercel', 
    'repo': 'next.js',
    'token': {GITHUB_PAT},
    'time_period': time_period
    }
    
    url = 'http://localhost:3000/get-commits'
    response = requests.get(url, params=params)
    commits = response.json()

    

    if response.status_code == 200:
        # Assuming the response is JSON
        # commits = response.json()
        # print("commits ===> ", len(commits))
        # for commit in commits:
        #     print("Name = " + commit['commit']['author']['name'] + "\n Title = " + commit['commit']['message'])
        #     print("Date = " + commit['commit']['author']['date'] + "\n")
        return commits
    else:
        print(f"Failed to fetch commits: {response.status_code}")

def get_diffs(commits):
    headers = {
        'Authorization': f'Bearer {GITHUB_PAT}',
        'Accept': 'application/vnd.github.v3+json',
    }

    commit_diffs = []
    for commit in commits:
        commit_url = commit['url']  # This is the API URL for the individual commit
        commit_response = requests.get(commit_url, headers=headers)
        commit_details = commit_response.json()

        # Prepare a dictionary to store details of the commit and its diffs
        commit_info = {
            'commit_message': commit_details['commit']['message'],
            'author': commit_details['commit']['author']['name'],
            'date': commit_details['commit']['author']['date'],
            'files_changed': []
        }

        # Fetch the patch (diff) information for each file
        if 'files' in commit_details:
            for file in commit_details['files']:
                file_info = {
                    'filename': file['filename'],
                    'diff': file.get('patch', 'No diff available')  # Get the diff or indicate no diff
                }
                commit_info['files_changed'].append(file_info)

        # Append the commit details and diffs to the commit_diffs list
        commit_diffs.append(commit_info)

    # for commit in commit_diffs:
    #     print(f"Commit Message: {commit['commit_message']}")
    #     print(f"Author: {commit['author']}")
    #     print(f"Date: {commit['date']}")
    #     print("Files Changed:")
    #     for file in commit['files_changed']:
    #         print(f"  File: {file['filename']}")
    #         print(f"  Diff: {file['diff']}\n")
    #     print('-' * 80)

    return commit_diffs

if __name__ == "__main__":
    commits = get_commits(time_period=2)
    diffs = get_diffs(commits)
    prepare_change_log(diffs)
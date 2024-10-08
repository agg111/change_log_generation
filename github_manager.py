import requests
import os
from datetime import datetime, timedelta
import logging

from greptile_manager import prepare_change_log
import utils

from dotenv import load_dotenv, dotenv_values

logging.basicConfig(level=logging.INFO,  # Set the logging level to INFO
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('logging/error.log'),  # Log to a file
                              logging.StreamHandler()])  # Log to console

load_dotenv()

GITHUB_PAT = os.getenv("GITHUB_PAT")
GREPTILE_KEY = os.getenv("GREPTILE_KEY")

CHANGE_LOG_FILE_PATH = "change_log/change_log.txt"

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
    logging.info("Fetching commits")
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
        return commits
    else:
        print(f"Failed to fetch commits: {response.status_code}")

def get_diffs(commits):
    logging.info("Fetching diffs")
    headers = {
        'Authorization': f'Bearer {GITHUB_PAT}',
        'Accept': 'application/vnd.github.v3+json',
    }

    commit_diffs = []
    try:
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
    except Exception as e:
        logging.error(f"An error occurred while fetching diffs: {e}")

    return commit_diffs

# persist change_log
# def save(change_log):
#     try:
#         with open(CHANGE_LOG_FILE_PATH, 'a') as file:
#             file.write('\n<<START>>\n' + change_log + '\n<<END>>\n')
#         logging.info("Change log updated successfully!")
#     except Exception as e:
#         logging.error("Error occurred while updating change log")

# # fetch change log
# def fetch():
#     try:
#         # Open the file and read its content
#         with open(CHANGE_LOG_FILE_PATH, 'r') as file:
#             content = file.read()

#         # Split the content into paragraphs using the separators **start** and **end**
#         paragraphs = content.split('<<END>>')  # Assuming paragraphs are separated by two newlines

#         # Add **start** and **end** to each paragraph
#         formatted_paragraphs = [
#             paragraph.replace('<<START>>', '').strip() 
#             for paragraph in paragraphs 
#             if paragraph.strip()
#         ]

#         # # Print the list of formatted paragraphs
#         # for paragraph in formatted_paragraphs:
#         #     print("fetched logs")
#         #     print(paragraph)
#     except Exception as e:
#         # Print an error message if something goes wrong
#         logging.error(f"An error occurred while reading the file: {e}")

# def generate_change_log():
#     commits = get_commits(time_period=2)
#     diffs = get_diffs(commits)
#     change_log = prepare_change_log(diffs, time_period=2)
#     utils.save(change_log)

# def render_change_log():
#     # fetch()

# if __name__ == "__main__":
#     generate_change_log()
#     render_change_log()
from flask import Flask, jsonify, request, render_template
import requests
from datetime import datetime, timedelta
import logging
import os

import utils
from dotenv import load_dotenv, dotenv_values

load_dotenv()

app = Flask(__name__)

# print(os.getenv("GITHUB_PAT"))
github_token = os.getenv("GITHUB_PAT")
greptile_api_key = os.getenv("GREPTILE_KEY")
CHANGE_LOG_FILE_PATH = "change_log/change_log.txt"

@app.template_filter('nl2br')
def nl2br(value):
    return value.replace('\n', '<br>')

@app.route('/')
def render_changelog():
    changelog = utils.fetch_changelog()
    # Render the paragraphs in the UI
    return render_template('changelog.html', changelog=changelog)

# def fetch():
#     try:
#         # Open the file and read its content
#         with open(CHANGE_LOG_FILE_PATH, 'r') as file:
#             content = file.read()

#         # Split the content into paragraphs using the separators **start** and **end**
#         changelogs = content.split('<<END>>')  # Assuming paragraphs are separated by two newlines

#         # Add **start** and **end** to each paragraph
#         formatted_changelogs = [
#             cl.replace('<<START>>', '').strip() 
#             for cl in changelogs 
#             if cl.strip()
#         ]

#         # Print the list of formatted paragraphs
#         for fc in formatted_changelogs:
#             print(fc)
#         return formatted_changelogs[::-1]
#     except Exception as e:
#         # Print an error message if something goes wrong
#         logging.error(f"An error occurred while reading the file: {e}")


@app.route('/get-repositories', methods=['GET'])
def get_repos():
    headers = {"Authorization": "token " + github_token}
    response = requests.get("https://api.github.com/user/repos", headers=headers)

    if response.status_code == 200:
        repositories = response.json()
        return jsonify(repositories) # Return the list of repositories as JSON
    else:
        return f"Failed to fetch repositories: {response.status_code}", response.status_code
    

@app.route('/get-commits', methods=['GET'])
def commits():
    owner = request.args.get('owner')
    repo = request.args.get('repo')
    token = request.args.get('token')
    time_period = request.args.get('time_period', default=7, type=int)
        
    if not owner or not repo or not token:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        commits_data = get_commits(owner, repo, token, time_period)
        return jsonify(commits_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_commits(owner, repo, token, time_period):
    since_date = (datetime.utcnow() - timedelta(days=time_period)).isoformat() + 'Z'  # ISO 8601 format
    # print("Since date = " , since_date)
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?since={since_date}"
    
    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/vnd.github+json'
    }
    
    response = requests.get(url, headers=headers)
    return response.json()

def repository_info():
    url = "https://api.greptile.com/v2/repositories/{repositoryId}"
    headers = {"Authorization": "Bearer <token>"}
    response = requests.request("GET", url, headers=headers)
    print(response.text)

# def index():
#     url = 'https://api.greptile.com/v2/repositories'
#     headers = {
#         'Authorization': f'Bearer {greptile_api_key}',
#         'X-Github-Token': github_token,
#         'Content-Type': 'application/json'
#     }
#     payload = {
#         "remote": "github",
#         "repository": "pandas-dev/pandas",
#         "branch": "main"
#     }

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, port=3000)
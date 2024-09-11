import requests
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

github_token = os.getenv("GITHUB_CLASSIC_PAT")
greptile_api_key = os.getenv("GREPTILE_KEY")


def repository_info(repository_id):
    url = "https://api.greptile.com/v2/repositories/{repository_id}"
    headers = {"Authorization": "Bearer <token>"}
    response = requests.request("GET", url, headers=headers)
    print(response.text)

def index(repo, branch):
    url = 'https://api.greptile.com/v2/repositories'
    headers = {
        'Authorization': f'Bearer {greptile_api_key}',
        'X-Github-Token': github_token,
        'Content-Type': 'application/json'
    }
    payload = {
        "remote": "github",
        "repository": repo,
        "branch": branch
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    return response.json().get('statusEndpoint')

def get_progress(repository_identifier):
    url = f'https://api.greptile.com/v2/repositories/{repository_identifier}'
    headers = {
        'Authorization': f'Bearer {greptile_api_key}',
        'X-Github-Token': github_token
    }

    response = requests.get(url, headers=headers)
    print(response.json())

def query(repo, branch, question):
    url = 'https://api.greptile.com/v2/query'
    headers = {
        'Authorization': f'Bearer {greptile_api_key}',
        'X-Github-Token': github_token,
        'Content-Type': 'application/json'
    }
    payload = {
        "messages": [
            {
                "id": "query-1",
                "content": question,
                "role": "user"
            }
        ],
        "repositories": [
            {
                "remote": "github",
                "repository": repo,
                "branch": branch
            }
        ],
        "sessionId": "test-session-id"  # optional
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())

def prepare_change_log(diffs):
    url = "https://api.greptile.com/v2/query"

    payload = {
        "messages": [
            {
                "id": "id-123",
                "content": f"""Given is a series of diffs for the past 7 days for vercel/next.js repo. Diffs - {diffs} 
                Generate a change log with a succinct overview about the changes STRICTLY in 2-3 sentences.   
                Identify what the features that the changes are about.
                Get the latest data of the change based on the diff.
                Example of a change log - 
                The Auto-Tuning for Workers simplifies Worker management in Temporal by allowing Workers 
                to scale up to the maximum CPU and memory limits of the underlying compute node. 
                Feature Tags - Java SDK, Python SDK, Cloud, Temporal CLI
                Date - Aug 9, 2024
                """,
                "role": "<string>"
            }
        ],
        "repositories": [
            {
                "remote": "github",
                "branch": "canary",
                "repository": "vercel/next.js"
            }
        ],
        "sessionId": "<string>",
        "stream": False,
        "genius": True
    }

    headers = {
        "Authorization": f"Bearer {greptile_api_key}",
        "X-GitHub-Token": github_token,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.json()["message"])

if __name__ == "__main__":
    # index("XCS224N-Handouts", "main")
    # index("huggingface/course", "main")
    
    # get_progress("github%3Amain%3Ahuggingface%2Fcourse")

    repo = "agg111/wallet-pnl"
    branch = "main"
    # index(repo, branch)
    get_progress("github%3Amain%3Aagg111%2Fwallet-pnl")
    # question = "what's this about?"
    question = "Where's the code responsible for concatenating dataframes?"
    query(repo, branch, question)


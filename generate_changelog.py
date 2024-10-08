from github_manager import get_commits, get_diffs, prepare_change_log
from utils import save

def generate_change_log():
    commits = get_commits(time_period=2)
    diffs = get_diffs(commits)
    change_log = prepare_change_log(diffs)
    save(change_log)

if __name__ == "__main__":
    generate_change_log()
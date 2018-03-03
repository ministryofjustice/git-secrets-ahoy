from collections import namedtuple

Context = namedtuple('Context', ['git_repo'])
Secret = namedtuple('Secret', ['commit', 'type'])

def main():
    context = parse_args()
    secrets = scan_repo()
    output = format_output(secrets)
    print(output)
    return 0 if not secrets else 1

def parse_args():
    pass

def scan_repo():
    repo = load_repo()
    commits = find_relevant_commits(repo)
    return find_secrets(commits)

def load_repo():
    pass

def find_relevant_commits(repo):
    return []

def find_secrets(commits):
    secrets = []
    for commit in commits:
        matches = check_commit(commit)
        if matches:
            secrets.extend(matches)
    return secrets

def check_commit():
    pass

def format_output(secrets):
    return "Stuff and Things"

if __name__ == '__main__':
    import sys
    code = main()
    sys.exit(code)

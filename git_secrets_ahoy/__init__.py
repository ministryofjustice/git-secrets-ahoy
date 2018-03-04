import argparse
from collections import namedtuple
import math

import git

Context = namedtuple('Context', ['git_repo'])
Secret = namedtuple('Secret', ['commit', 'type'])


def main():
    context = parse_args()
    secrets = scan_repo(context)
    output = format_output(secrets)
    print(output)
    return 0 if not secrets else 1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('git_repo',
        type=str, default=".", nargs='?',
        help='Path to git repository')
    args = parser.parse_args()
    return Context(args.git_repo)


def scan_repo(context):
    repo = git.Repo(context.git_repo)
    commits = find_relevant_commits(repo)
    return find_secrets(commits)


def find_relevant_commits(repo):
    return repo.iter_commits()


def find_secrets(commits):
    secrets = []
    for commit in commits:
        for match in check_commit(commit):
            secrets.append(match)
    return secrets


def check_commit(commit):
    matches = []
    for diff_obj in commit_diff(commit):
        patch = diff_obj.diff.decode(git.compat.defenc, errors='replace')
        for match in check_entropy(patch):
            matches.append(match)

    return matches


def commit_diff(commit):
    if commit.parents:
        return commit.parents[0].diff(commit, create_patch=True)
    return commit.diff(git.NULL_TREE, create_patch=True)


BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
HEX_CHARS = "1234567890abcdefABCDEF"


def check_entropy(patch):
    matches = []

    for line in patch.split("\n"):
        # Only check lines introduced in this patch
        if not line.startswith("+"):
            continue
        for word in line.split():
            for string in entropic_strings(word, BASE64_CHARS, 4.5):
                matches.append(string)
            for string in entropic_strings(word, HEX_CHARS, 3):
                matches.append(string)

    return matches


def entropic_strings(word, char_set, min_entropy, min_len=20):
    letters = ""
    strings = []
    for char in word:
        if char in char_set:
            letters += char
        else:
            if len(letters) > min_len:
                strings.append(letters)
            letters = ""
    if len(letters) > min_len:
        strings.append(letters)
    return (
        string for string in strings
            if shannon_entropy(string, char_set) > min_entropy
    )


def shannon_entropy(data, iterator):
    """
    Borrowed from http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html
    """
    if not data:
        return 0
    entropy = 0
    for x in iterator:
        p_x = float(data.count(x))/len(data)
        if p_x > 0:
            entropy += - p_x*math.log(p_x, 2)
    return entropy


def format_output(secrets):
    import pprint
    pprint.pprint(secrets)


if __name__ == '__main__':
    import sys
    code = main()
    sys.exit(code)

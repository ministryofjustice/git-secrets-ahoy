import argparse
from datetime import datetime
import json
import math
import sys

import git
import plain_obj

Context = plain_obj.new_type('Context', ['path', 'target'])
DiffSecret = plain_obj.new_type(
    'DiffSecret',
    ['diff', 'path', 'patch', 'matches', 'reason']
)
DiffSecret.ENTROPY = 'high-entropy'
CommitSecret = plain_obj.new_type(
    'CommitSecret',
    ['commit', 'ref', 'datetime', 'message'] + DiffSecret.__slots__
)


def main(args=sys.argv):
    context = parse_args(args)
    secrets = scan_repo(context)
    output = format_output(secrets)
    for chunk in output:
        print(chunk)
    return 0 if not secrets else 1


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        type=str, default=".", nargs='?',
                        help='Path to git repository')
    parser.add_argument('--staged',
                        action='store_true',
                        help='Check changes staged into the git index')
    parsed = parser.parse_args(args)
    return Context(
        path=parsed.path,
        target=("staged",)
    )


def scan_repo(context):
    repo = git.Repo(context.path)
    commits = find_relevant_commits(repo)
    return find_secrets(commits)


def find_relevant_commits(repo):
    if repo.head.is_valid():
        yield from repo.iter_commits()


def find_secrets(commits):
    for commit in commits:
        commit_datetime = datetime.fromtimestamp(commit.committed_date)
        for diff_secret in check_commit(commit):
            yield CommitSecret(
                commit=commit,
                ref=commit.hexsha,
                datetime=commit_datetime,
                message=commit.message,
                **diff_secret.to_dict()
            )


def check_commit(commit):
    for diff_obj in commit_diff(commit):
        patch = diff_obj.diff.decode(git.compat.defenc, errors='replace')

        yield from check_entropy(diff_obj, patch)


def commit_diff(commit):
    if commit.parents:
        return commit.parents[0].diff(commit, create_patch=True)
    return commit.diff(git.NULL_TREE, create_patch=True)


BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
HEX_CHARS = "1234567890abcdefABCDEF"


def listify(func):
    def wrapper(*args):
        return list(func(*args))
    return wrapper


def check_entropy(diff_obj, patch):
    matches = collect_entropic_strings(patch)
    if matches:
        yield DiffSecret(
            diff=diff_obj,
            path=diff_obj.b_path if diff_obj.b_path else diff_obj.a_path,
            patch=patch,
            matches=matches,
            reason=DiffSecret.ENTROPY
        )


@listify
def collect_entropic_strings(patch):
    for line in patch.split("\n"):
        # Only check lines introduced in this patch
        # if not line.startswith("+"):
        #     continue
        for word in line[1:].split():
            for string in entropic_strings(word, BASE64_CHARS, 4.5):
                yield string
            for string in entropic_strings(word, HEX_CHARS, 3):
                yield string


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


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CommitSecret):
            return without(obj.to_dict(), "commit", "diff")
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def without(d, *keys):
    for key in keys: d.pop(key)
    return d


def format_output(secrets):
    for secret in secrets:
        yield json.dumps(secret, indent=2, cls=JSONEncoder)


if __name__ == '__main__':
    sys.exit(main())

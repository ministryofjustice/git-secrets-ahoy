import argparse
from datetime import datetime
import json
import math
import sys
import typing
from typing import Iterable, Collection, List, Callable

import git

from git_secrets_ahoy import types

def main(args: List[str] = sys.argv[1:]) -> int:
    context = parse_args(args)
    secrets = scan_repo(context)
    output = format_output(secrets)
    for chunk in output:
        print(chunk)
    return 0 if not secrets else 1


def parse_args(args: List[str]) -> types.Context:
    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        type=str, default=".", nargs='?',
                        help='Path to git repository')
    group = parser.add_argument_group(
        "target", "Use the following to select what to check"
    )
    group.add_argument('--staged', action='store_true',
                       help='Check changes staged into the git index')
    group.add_argument('--all', action='store_true',
                       help='Check entire history of all branches')
    parsed = parser.parse_args(args)

    target: types.Target.Type
    if parsed.staged:
        target = types.Target.Staged()
    else:
        target = types.Target.All()

    return types.Context(
        path=parsed.path,
        target=target
    )


def scan_repo(context: types.Context) -> Iterable[types.Secret]:
    repo = git.Repo(context.path)
    commits = find_relevant_commits(repo)
    return find_secrets(commits)


def find_relevant_commits(repo: git.Repo) -> Iterable[git.Commit]:
    if repo.head.is_valid():
        yield from repo.iter_commits()


def find_secrets(commits: Iterable[git.Commit]) -> Iterable[types.Secret]:
    for commit in commits:
        yield from check_commit(commit)


def check_commit(commit: git.Commit) -> Iterable[types.Secret]:
    for diff_obj in commit_diff(commit):
        patch = diff_obj.diff.decode(git.compat.defenc, errors='replace')

        yield from check_entropy(patch, diff_obj, commit)


def commit_diff(commit: git.Commit) -> git.DiffIndex:
    if commit.parents:
        return commit.parents[0].diff(commit, create_patch=True)
    return commit.diff(git.NULL_TREE, create_patch=True)


BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
HEX_CHARS = "1234567890abcdefABCDEF"


def listify(
    func: Callable[[str], Iterable[str]]
) -> Callable[[str], List[str]]:
    # Type signature is overly specific for completeness purposes
    # Ideally this should just pass through *args
    # see https://github.com/python/mypy/issues/3157 for details
    def wrapper(arg: str) -> List[str]:
        return list(func(arg))
    return wrapper


def check_entropy(
    patch: str, diff: git.Diff, commit: git.Commit
) -> Iterable[types.Secret]:
    matches = collect_entropic_strings(patch)
    if matches:
        yield types.Secret(
            commit=commit,
            diff=diff,
            patch=patch,
            matches=matches,
            reason=types.Reason.HighEntropy(),
        )


@listify
def collect_entropic_strings(patch: str) -> typing.Iterable[str]:
    for line in patch.split("\n"):
        for word in line[1:].split():
            for string in entropic_strings(word, BASE64_CHARS, 4.5):
                yield string
            for string in entropic_strings(word, HEX_CHARS, 3.0):
                yield string


def entropic_strings(
    word: str,
    char_set: str,
    min_entropy: float,
    min_len: int = 20
) -> Iterable[str]:
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


def shannon_entropy(data: str, iterator: str) -> float:
    """
    Borrowed from http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html
    """
    if not data:
        return 0
    entropy = 0.0
    for x in iterator:
        p_x = float(data.count(x))/len(data)
        if p_x > 0:
            entropy += - p_x*math.log(p_x, 2)
    return entropy

K = typing.TypeVar('K')
V = typing.TypeVar('V')
def without(d: typing.Dict[K, V], *keys: K) -> typing.Dict[K, V]:
    for key in keys: d.pop(key)
    return d


def format_output(secrets: Iterable[types.Secret]) -> Iterable[str]:
    for secret in secrets:
        yield json.dumps(
            indent=2,
            obj={
                "ref": secret.ref,
                "datetime": secret.datetime.isoformat(),
                "message": secret.message,
                "path": secret.path,
                "patch": secret.patch,
                "matches": secret.matches,
                "reason": str(secret.reason),
            }
        )


if __name__ == '__main__':
    sys.exit(main())

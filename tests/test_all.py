from base64 import b64encode
import os
import os.path as osp

from git import Repo
import pytest

import git_secrets_ahoy as gsa

@pytest.fixture
def git_repo(tmpdir):
    return Repo.init(tmpdir)

def git_add(git_repo, filename, contents):
    filepath = osp.join(git_repo.working_tree_dir, filename)
    with open(filepath, "wb") as f:
        f.write(contents.encode("utf-8"))
    git_repo.index.add([filepath])

def build_context(git_repo):
    return gsa.Context(git_repo=git_repo.working_tree_dir)

def test_scan(git_repo):
    """
    A file with some suspicious entropy
    """
    secret = b64encode(os.urandom(40)).decode("utf-8")
    git_add(git_repo, "secret.txt", secret)
    git_repo.index.commit("A short message")
    commit = git_repo.commit("HEAD")
    context = build_context(git_repo)

    secrets = list(gsa.scan_repo(context))

    assert len(secrets) == 1

    assert secrets[0].ref == commit.hexsha
    assert secrets[0].datetime.timestamp() == commit.committed_date
    assert secrets[0].message == "A short message"
    assert secrets[0].path == "secret.txt"
    assert secret in secrets[0].patch
    assert secrets[0].matches == [secret]
    assert secrets[0].reason == "high-entropy"

def test_scan2(git_repo):
    """
    A file that's benign
    """
    git_add(git_repo, "secret.txt", "Everything is awesome")
    git_repo.index.commit("A short message")
    context = build_context(git_repo)

    secrets = list(gsa.scan_repo(context))

    assert len(secrets) == 0


## Scenarios to cover
# multiple commits that match
# multiple commits that don't all match
# revision limiting
# deleting stuff not matching
# binary files not getting in the way
# regex matches

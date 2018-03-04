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
        f.write(contents)
    git_repo.index.add([filepath])

def build_context(git_repo):
    return gsa.Context(git_repo=git_repo.working_tree_dir)

def test_scan(git_repo):
    """
    A file with some suspicious entropy
    """
    git_add(git_repo, "secret.txt", b64encode(os.urandom(40)))
    git_repo.index.commit("A short message")
    context = build_context(git_repo)

    secrets = gsa.scan_repo(context)

    assert len(secrets) == 1

def test_scan2(git_repo):
    """
    A file that's benign
    """
    git_add(git_repo, "secret.txt", b"Everything is awesome")
    git_repo.index.commit("A short message")
    context = build_context(git_repo)

    secrets = gsa.scan_repo(context)

    assert len(secrets) == 0

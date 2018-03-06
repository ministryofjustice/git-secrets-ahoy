from base64 import b64encode
import os
import os.path as osp

from git import Repo
import pytest

import git_secrets_ahoy as gsa

def secret(length=40):
    return b64encode(os.urandom(length)).decode("utf-8")


@pytest.fixture(scope="session")
def secret1():
    return secret()


@pytest.fixture(scope="session")
def secret2():
    return secret()


@pytest.fixture(scope="session")
def secret3():
    return secret()


@pytest.fixture
def git_repo(tmpdir):
    return Repo.init(tmpdir, mkdir=False)


def git_add(git_repo, filename, contents):
    filepath = osp.join(git_repo.working_tree_dir, filename)
    os.makedirs(osp.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        try:
            f.write(contents)
        except TypeError:
            f.write(contents.encode("utf-8"))
    git_repo.index.add([filepath])


def build_context(git_repo):
    return gsa.Context(git_repo=git_repo.working_tree_dir)

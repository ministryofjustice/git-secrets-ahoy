import git_secrets_ahoy as gsa

import conftest as T

def test_empty_repo(git_repo):
    context = T.build_context(git_repo)
    secrets = list(gsa.scan_repo(context))

    assert len(secrets) == 0

def test_produces_generator(git_repo):
    # TODO: can this verify everything is streamy?
    T.git_add(git_repo, "stuff.txt", "blah")
    git_repo.index.commit("message")

    context = T.build_context(git_repo)
    result = gsa.scan_repo(context)

    from types import GeneratorType
    assert isinstance(result, GeneratorType)

def test_one_commit_with_high_entropy(git_repo, secret1):
    T.git_add(git_repo, "secret.txt", secret1)
    git_repo.index.commit("A short message")
    commit = git_repo.commit("HEAD")

    context = T.build_context(git_repo)
    secrets = list(gsa.scan_repo(context))

    assert len(secrets) == 1

    assert secrets[0].ref == commit.hexsha
    assert secrets[0].datetime.timestamp() == commit.committed_date
    assert secrets[0].message == "A short message"
    assert secrets[0].path == "secret.txt"
    assert secret1 in secrets[0].patch
    assert secrets[0].matches == [secret1]
    assert secrets[0].reason == "high-entropy"

def test_one_commit_benign(git_repo):
    T.git_add(git_repo, "secret.txt", "Everything is awesome")
    git_repo.index.commit("A short message")

    context = T.build_context(git_repo)
    secrets = list(gsa.scan_repo(context))

    assert len(secrets) == 0

def test_multiple_secrets_one_commit(git_repo, secret1, secret2):
    T.git_add(git_repo, "secret.txt", secret1)
    T.git_add(git_repo, "deeply/nested/secret.txt", secret2)
    git_repo.index.commit("Multi-fail")
    commit = git_repo.commit("HEAD")

    context = T.build_context(git_repo)
    secrets = list(gsa.scan_repo(context))

    assert len(secrets) == 2

    assert secrets[0].ref == commit.hexsha
    assert secrets[1].ref == commit.hexsha

    matches = [(s.path, s.matches) for s in secrets]
    assert ("secret.txt", [secret1]) in matches
    assert ("deeply/nested/secret.txt", [secret2]) in matches


def test_multiple_commits_all_high_entropy(git_repo, secret1, secret2):
    T.git_add(git_repo, "one.txt", secret1)
    git_repo.index.commit("Commit 1")
    commit1 = git_repo.commit("HEAD")
    T.git_add(git_repo, "subdir/two.txt", secret2)
    git_repo.index.commit("Sort of pairwise testing?")
    commit2 = git_repo.commit("HEAD")

    context = T.build_context(git_repo)
    secrets = list(gsa.scan_repo(context))

    assert len(secrets) == 2

    # Newest commit first
    assert secrets[0].ref == commit2.hexsha
    assert secrets[0].message == "Sort of pairwise testing?"
    assert secrets[0].path == "subdir/two.txt"
    assert secrets[0].matches == [secret2]

    assert secrets[1].ref == commit1.hexsha
    assert secrets[1].message == "Commit 1"
    assert secrets[1].path == "one.txt"
    assert secrets[1].matches == [secret1]

# TODO: assert secret in secrets helper

## Scenarios to cover
# multiple commits that match
# multiple commits that don't all match
# multiple secrets in different files in one commit
# secret is only part of the commit
# revision limiting
#   - A only
#   - A..B
#   - A..HEAD
# deleting stuff not matching
#   maybe this shouldn't be ok, a delete is still part of history
# binary files not getting in the way
# regex matches
# merge commits / multiple parents
# commit on a branch where search starts after branch created
#   A -- B -- C -- D -- M -- E
#    \- F -- G -- H --/
#   Range B..E, with secret in G

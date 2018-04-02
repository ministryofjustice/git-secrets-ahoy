import pytest

import git_secrets_ahoy as gsa

import conftest as T

def test_1(capsys):
    code = gsa.main([])
    assert code == 1

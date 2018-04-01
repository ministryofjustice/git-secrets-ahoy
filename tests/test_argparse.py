import pytest

import git_secrets_ahoy as gsa

import conftest as T

def test_help_exits(capsys):
    with pytest.raises(SystemExit) as exinfo:
        gsa.parse_args(["--help"])
    assert exinfo.value.code == 0
    captured = capsys.readouterr()
    assert "usage:" in captured.out

def test_default_path_is_pwd():
    context = gsa.parse_args([])
    assert context.path == "."

def test_path_can_be_set():
    context = gsa.parse_args(["/blah/blah"])
    assert context.path == "/blah/blah"

def test_target_staged():
    context = gsa.parse_args(["--staged"])
    assert context.target == ("staged",)

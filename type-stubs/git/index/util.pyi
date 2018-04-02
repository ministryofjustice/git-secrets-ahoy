# Stubs for git.index.util (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class TemporaryFileSwap:
    file_path: Any = ...
    tmp_file_path: Any = ...
    def __init__(self, file_path) -> None: ...
    def __del__(self) -> None: ...

def post_clear_cache(func): ...
def default_index(func): ...
def git_working_dir(func): ...
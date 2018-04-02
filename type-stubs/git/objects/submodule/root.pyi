# Stubs for git.objects.submodule.root (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from .base import Submodule, UpdateProgress
from typing import Any, Optional

class RootUpdateProgress(UpdateProgress):
    REMOVE: Any = ...
    PATHCHANGE: Any = ...
    BRANCHCHANGE: Any = ...
    URLCHANGE: Any = ...

class RootModule(Submodule):
    k_root_name: str = ...
    def __init__(self, repo) -> None: ...
    def update(self, previous_commit: Optional[Any] = ..., recursive: bool = ..., force_remove: bool = ..., init: bool = ..., to_latest_revision: bool = ..., progress: Optional[Any] = ..., dry_run: bool = ..., force_reset: bool = ..., keep_going: bool = ...): ...
    def module(self): ...

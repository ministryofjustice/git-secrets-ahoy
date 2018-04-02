# Stubs for git.refs.tag (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from .reference import Reference
from typing import Any, Optional

class TagReference(Reference):
    @property
    def commit(self): ...
    @property
    def tag(self): ...
    object: Any = ...
    @classmethod
    def create(cls, repo, path, ref: str = ..., message: Optional[Any] = ..., force: bool = ..., **kwargs): ...
    @classmethod
    def delete(cls, repo, *tags) -> None: ...
Tag = TagReference

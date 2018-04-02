# Stubs for git.index.base (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

import git.diff as diff
from git.exc import CheckoutError as CheckoutError
from git.objects.util import Serializable
from git.util import LazyMixin
from typing import Any, Optional

class IndexFile(LazyMixin, diff.Diffable, Serializable):
    S_IFGITLINK: Any = ...
    repo: Any = ...
    version: Any = ...
    def __init__(self, repo, file_path: Optional[Any] = ...) -> None: ...
    @property
    def path(self): ...
    def write(self, file_path: Optional[Any] = ..., ignore_extension_data: bool = ...) -> None: ...
    def merge_tree(self, rhs, base: Optional[Any] = ...): ...
    @classmethod
    def new(cls, repo, *tree_sha): ...
    @classmethod
    def from_tree(cls, repo, *treeish, **kwargs): ...
    def iter_blobs(self, predicate: Any = ...): ...
    def unmerged_blobs(self): ...
    @classmethod
    def entry_key(cls, *entry): ...
    def resolve_blobs(self, iter_blobs): ...
    def update(self): ...
    def write_tree(self): ...
    def add(self, items, force: bool = ..., fprogress: Any = ..., path_rewriter: Optional[Any] = ..., write: bool = ..., write_extension_data: bool = ...): ...
    def remove(self, items, working_tree: bool = ..., **kwargs): ...
    def move(self, items, skip_errors: bool = ..., **kwargs): ...
    def commit(self, message, parent_commits: Optional[Any] = ..., head: bool = ..., author: Optional[Any] = ..., committer: Optional[Any] = ..., author_date: Optional[Any] = ..., commit_date: Optional[Any] = ..., skip_hooks: bool = ...): ...
    def checkout(self, paths: Optional[Any] = ..., force: bool = ..., fprogress: Any = ..., **kwargs): ...
    entries: Any = ...
    def reset(self, commit: str = ..., working_tree: bool = ..., paths: Optional[Any] = ..., head: bool = ..., **kwargs): ...
    def diff(self, other: Any = ..., paths: Optional[Any] = ..., create_patch: bool = ..., **kwargs): ...

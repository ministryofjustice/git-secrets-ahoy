# Stubs for git.remote (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from git.util import Iterable, LazyMixin, RemoteProgress as RemoteProgress
from typing import Any, Optional

class PushInfo:
    NEW_TAG: Any = ...
    NEW_HEAD: Any = ...
    NO_MATCH: Any = ...
    REJECTED: Any = ...
    REMOTE_REJECTED: Any = ...
    REMOTE_FAILURE: Any = ...
    DELETED: Any = ...
    FORCED_UPDATE: Any = ...
    FAST_FORWARD: Any = ...
    UP_TO_DATE: Any = ...
    ERROR: Any = ...
    flags: Any = ...
    local_ref: Any = ...
    remote_ref_string: Any = ...
    summary: Any = ...
    def __init__(self, flags, local_ref, remote_ref_string, remote, old_commit: Optional[Any] = ..., summary: str = ...) -> None: ...
    @property
    def old_commit(self): ...
    @property
    def remote_ref(self): ...

class FetchInfo:
    NEW_TAG: Any = ...
    NEW_HEAD: Any = ...
    HEAD_UPTODATE: Any = ...
    TAG_UPDATE: Any = ...
    REJECTED: Any = ...
    FORCED_UPDATE: Any = ...
    FAST_FORWARD: Any = ...
    ERROR: Any = ...
    @classmethod
    def refresh(cls): ...
    ref: Any = ...
    flags: Any = ...
    note: Any = ...
    old_commit: Any = ...
    remote_ref_path: Any = ...
    def __init__(self, ref, flags, note: str = ..., old_commit: Optional[Any] = ..., remote_ref_path: Optional[Any] = ...) -> None: ...
    @property
    def name(self): ...
    @property
    def commit(self): ...

class Remote(LazyMixin, Iterable):
    repo: Any = ...
    name: Any = ...
    def __init__(self, repo, name) -> None: ...
    def __getattr__(self, attr): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __hash__(self): ...
    def exists(self): ...
    @classmethod
    def iter_items(cls, repo, *args, **kwargs) -> None: ...
    def set_url(self, new_url, old_url: Optional[Any] = ..., **kwargs): ...
    def add_url(self, url, **kwargs): ...
    def delete_url(self, url, **kwargs): ...
    @property
    def urls(self) -> None: ...
    @property
    def refs(self): ...
    @property
    def stale_refs(self): ...
    @classmethod
    def create(cls, repo, name, url, **kwargs): ...
    add: Any = ...
    @classmethod
    def remove(cls, repo, name): ...
    rm: Any = ...
    def rename(self, new_name): ...
    def update(self, **kwargs): ...
    def fetch(self, refspec: Optional[Any] = ..., progress: Optional[Any] = ..., **kwargs): ...
    def pull(self, refspec: Optional[Any] = ..., progress: Optional[Any] = ..., **kwargs): ...
    def push(self, refspec: Optional[Any] = ..., progress: Optional[Any] = ..., **kwargs): ...
    @property
    def config_reader(self): ...
    @property
    def config_writer(self): ...
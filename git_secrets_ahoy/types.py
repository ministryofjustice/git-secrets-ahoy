from datetime import datetime
import enum
import typing

import git


class Context(typing.NamedTuple):
    path: str
    target: "Target"


Target = typing.Union["Staged", "All", "Revisions"]


class Staged(typing.NamedTuple):
    pass


class All(typing.NamedTuple):
    pass


class Revisions(typing.NamedTuple):
    since: str
    until: str


class SecretReason(enum.Enum):
    ENTROPY = 'high-entropy'
    REGEX = 'regex-match'


class Secret(typing.NamedTuple):
    commit: git.Commit
    diff: git.Diff
    patch: str
    matches: typing.List[str]
    reason: SecretReason

    @property
    def path(self):
        return self.diff.b_path if self.diff.b_path else self.diff.a_path

    @property
    def ref(self):
        return self.commit.hexsha

    @property
    def datetime(self):
        return datetime.fromtimestamp(self.commit.committed_date)

    @property
    def message(self):
        return self.commit.message

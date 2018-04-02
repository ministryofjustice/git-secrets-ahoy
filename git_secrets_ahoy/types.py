from datetime import datetime as datetime_class
import enum
import typing

import git

class Target:
    class Staged(typing.NamedTuple):
        pass

    class All(typing.NamedTuple):
        pass

    class Revisions(typing.NamedTuple):
        since: typing.Optional[datetime_class]
        until: typing.Optional[datetime_class]

    Type = typing.Union[Staged, All, Revisions]

class Context(typing.NamedTuple):
    path: str
    target: Target.Type

class Reason:
    class HighEntropy(typing.NamedTuple):
        def __str__(self) -> str:
            return "high-entropy"

    class RegexMatch(typing.NamedTuple):
        rule: str
        def __str__(self) -> str:
            return "regex:%s" % self.rule

    Type = typing.Union[HighEntropy, RegexMatch]

class Secret(typing.NamedTuple):
    commit: git.Commit
    diff: git.Diff
    patch: str
    matches: typing.Collection[str]
    reason: Reason.Type

    @property
    def path(self) -> str:
        return self.diff.b_path if self.diff.b_path else self.diff.a_path

    @property
    def ref(self) -> str:
        return self.commit.hexsha

    @property
    def datetime(self) -> datetime_class:
        return self.commit.committed_datetime

    @property
    def message(self) -> str:
        return self.commit.message


def _namedtuple_eq(a: object, b: object) -> bool:
    """
    An equality comparison for namedtuples which
    cares about type as well as value
    """
    if type(a) != type(b):
        return False
    return tuple.__eq__(a, b)

for klass in [
    Target.Staged,
    Target.All,
    Target.Revisions,
    Context,
    Reason.HighEntropy,
    Reason.RegexMatch,
    Secret
]:
    setattr(klass, "__eq__", _namedtuple_eq)

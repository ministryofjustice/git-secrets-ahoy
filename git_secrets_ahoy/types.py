from datetime import datetime as datetime_class
import enum
import typing

from dataclasses import dataclass, asdict
import git

class Target:
    @dataclass(frozen=True)
    class Staged:
        pass

    @dataclass(frozen=True)
    class All:
        pass

    @dataclass(frozen=True)
    class Revisions:
        since: typing.Optional[datetime_class]
        until: typing.Optional[datetime_class]

    Type = typing.Union[Staged, All, Revisions]

@dataclass(frozen=True)
class Context:
    path: str
    target: Target.Type

class Reason:
    @dataclass(frozen=True)
    class HighEntropy:
        def __str__(self) -> str:
            return "high-entropy"

    @dataclass(frozen=True)
    class RegexMatch:
        rule: str
        def __str__(self) -> str:
            return "regex:%s" % self.rule

    Type = typing.Union[HighEntropy, RegexMatch]

@dataclass(frozen=True)
class Secret:
    commit: git.Commit
    diff: git.Diff
    patch: str
    matches: typing.Collection[str]
    reason: Reason

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

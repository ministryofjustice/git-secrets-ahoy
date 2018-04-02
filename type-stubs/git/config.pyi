# Stubs for git.config (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

import abc
from typing import Any, Optional

class MetaParserBuilder(abc.ABCMeta):
    def __new__(cls, name, bases, clsdict): ...

class SectionConstraint:
    def __init__(self, config, section) -> None: ...
    def __del__(self) -> None: ...
    def __getattr__(self, attr): ...
    @property
    def config(self): ...
    def release(self): ...
    def __enter__(self): ...
    def __exit__(self, exception_type, exception_value, traceback) -> None: ...

class GitConfigParser:
    t_lock: Any = ...
    re_comment: Any = ...
    optvalueonly_source: str = ...
    OPTVALUEONLY: Any = ...
    OPTCRE: Any = ...
    def __init__(self, file_or_files, read_only: bool = ..., merge_includes: bool = ...) -> None: ...
    def __del__(self) -> None: ...
    def __enter__(self): ...
    def __exit__(self, exception_type, exception_value, traceback) -> None: ...
    def release(self): ...
    def optionxform(self, optionstr): ...
    def read(self): ...
    def items(self, section_name): ...
    def write(self): ...
    def add_section(self, section): ...
    @property
    def read_only(self): ...
    def get_value(self, section, option, default: Optional[Any] = ...): ...
    def set_value(self, section, option, value): ...
    def rename_section(self, section, new_name): ...
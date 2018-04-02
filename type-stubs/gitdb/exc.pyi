# Stubs for gitdb.exc (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

class ODBError(Exception): ...
class InvalidDBRoot(ODBError): ...
class BadObject(ODBError): ...
class BadName(ODBError): ...
class ParseError(ODBError): ...
class AmbiguousObjectName(ODBError): ...
class BadObjectType(ODBError): ...
class UnsupportedOperation(ODBError): ...

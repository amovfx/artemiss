from enum import Enum, unique

@unique
class ResponseCode(Enum):

    OK = 200
    BADPASSWORD = 301
    NOUSER = 302
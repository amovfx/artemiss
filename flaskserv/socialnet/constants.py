

"""

Constants for the site

"""
from enum import Enum, unique

@unique
class PERMISSIONS(Enum):
    NONE = 0
    READ = 1
    WRITE = 3
    EXECUTE = 4

    @classmethod
    def unittest_idata_generator(cls):
        for enum_val in cls.__iter__():
            setattr(
                enum_val, "__doc__", f"{enum_val.__class__.__name__}.{enum_val.name}"
            )
            yield enum_val

@unique
class SITECONTEXTS(Enum):
    GUEST = 0
    TRIBE = 1

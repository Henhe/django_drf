from enum import Enum


class CustomEnum(Enum):
    @classmethod
    def values(cls, exclude=[]):
        return [item.value for item in cls if item not in exclude]
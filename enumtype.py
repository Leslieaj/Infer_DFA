"""enum types:
        NodeType: type of the accepting, rejecting or unknown
        NodeColor: type of the colors of the node (white, red, blue)
        WordType: type of the trainnings (positive or negative)
"""
from enum import Enum, unique

@unique
class NodeType(Enum):
    rejecting = -1
    unknown = 0
    accepting = 1

    @classmethod
    def to_str(cls, value):
        if value == cls.rejecting:
            return 'rejecting'
        elif value == cls.unknown:
            return 'unknown'
        elif value == cls.accepting:
            return 'accepting'
        else:
            return ''

@unique
class NodeColor(Enum):
    white = -1
    red = 0
    blue = 1

    @classmethod
    def to_str(cls, value):
        if value == cls.white:
            return 'white'
        elif value == cls.red:
            return 'red'
        elif value == cls.blue:
            return 'blue'
        else:
            return ''

@unique
class WordType(Enum):
    neg = -1
    unknown = 0
    pos = 1

    @classmethod
    def to_str(cls, value):
        if value == cls.neg:
            return 'neg'
        elif value == cls.unknown:
            return 'unknown'
        elif value == cls.pos:
            return 'pos'
        else:
            return ''

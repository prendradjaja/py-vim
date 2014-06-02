"""A motion is represented as a subclass of Motion as follows:

1) It has an 'execute' method that implements the motion:
   a. It takes: row, col, buffer
   b. It returns a tuple of end coordinates. (row, col)

2) It has a 'type' attribute with value INCLUSIVE, EXCLUSIVE, or LINEWISE.
(Note that, as noted in the Vim documentation, inclusive and exclusive motions
are types of characterwise motions.)
"""

from constants import *

class Motion:
    type = UNSPECIFIED # override me with: EXCLUSIVE | INCLUSIVE | LINEWISE
    def execute(row, col, buffer):
        """Override me: return end coordinates"""
        raise Exception(ABSTRACT_METHOD)

class left(Motion):
    type = EXCLUSIVE
    def execute(row, col, buffer):
        col = max(col - 1, 1)
        return row, col

class right(Motion):
    type = EXCLUSIVE
    def execute(row, col, buffer):
        col = min(col + 1, len(buffer.line(row)))
        return row, col

class up(Motion):
    type = LINEWISE
    def execute(row, col, buffer):
        row = max(row - 1, 1)
        return row, col

class down(Motion):
    type = LINEWISE
    def execute(row, col, buffer):
        row = min(row + 1, buffer.numlines())
        return row, col

class first_column(Motion):
    type = EXCLUSIVE
    def execute(row, col, buffer):
        col = 1
        return row, col

class last_column(Motion):
    type = EXCLUSIVE
    def execute(row, col, buffer):
        col = len(buffer.line(row))
        return row, col

class first_nonblank(Motion):
    type = EXCLUSIVE
    def execute(row, col, buffer):
        buf_iter = buffer.iterator(row, 1, FORWARD, True)
        for (_, col), char in buf_iter:
            if char == '\n':
                return row, col - 1
            if char not in '\t ':
                return row, col

# foo motions

class right_three_times(Motion):
    type = EXCLUSIVE
    def execute(row, col, buffer):
        col = min(col + 1, len(buffer.line(row)))
        col = min(col + 1, len(buffer.line(row)))
        col = min(col + 1, len(buffer.line(row)))
        return row, col

class down_charwise(Motion):
    type = EXCLUSIVE
    def execute(row, col, buffer):
        row = min(row + 1, buffer.numlines())
        return row, col

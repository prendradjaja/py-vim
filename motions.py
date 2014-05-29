"""A motion is represented as a subclass of Motion as follows:

1) It has an 'execute' method that implements the motion:
   a. It takes a single Editor argument.
   b. It returns a tuple of end coordinates. (row, col)
   c. It does not affect the Editor's state, (e.g. cursor position, Buffer
      contents) except possibly to save information. (e.g. for marks)

2) It has a 'type' attribute with value INCLUSIVE, EXCLUSIVE, or LINEWISE.
(Note that, as noted in the Vim documentation, inclusive and exclusive motions
are types of characterwise motions.)
"""

from constants import *

class Motion:
    type = UNSPECIFIED   # override me
    def execute(editor): # override me
        raise Exception(NOT_IMPLEMENTED)

class cursor_left(Motion):
    type = EXCLUSIVE
    def execute(editor):
        row, col = editor.row, editor.col
        col = max(col - 1, 1)
        return row, col

class cursor_right(Motion):
    type = EXCLUSIVE
    def execute(editor):
        row, col = editor.row, editor.col
        col = min(col + 1, len(editor.buffer.line(row)))
        return row, col

class cursor_up(Motion):
    type = LINEWISE
    def execute(editor):
        row, col = editor.row, editor.col
        row = max(row - 1, 1)
        return row, col

class cursor_down(Motion):
    type = LINEWISE
    def execute(editor):
        row, col = editor.row, editor.col
        row = min(row + 1, editor.buffer.numlines())
        return row, col


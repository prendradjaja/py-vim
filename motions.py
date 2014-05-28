"""A motion is represented as a function as follows:

1) It takes a single Editor argument.

2) It returns a tuple of end coordinates. (row, col)

3) It does not affect the Editor's Buffer.

4) It has a 'type' attribute with value INCLUSIVE, EXCLUSIVE, or LINEWISE.
(Note that, as noted in the Vim documentation, inclusive and exclusive motions
are types of characterwise motions.)
"""

from constants import *

def cursor_left(editor):
    row, col = editor.row, editor.col
    col = max(col - 1, 1)
    return row, col
cursor_left.type = EXCLUSIVE

def cursor_right(editor):
    row, col = editor.row, editor.col
    col = min(col + 1, len(editor.buffer.line(row)))
    return row, col
cursor_right.type = EXCLUSIVE

def cursor_up(editor):
    row, col = editor.row, editor.col
    row = max(row - 1, 1)
    return row, col
cursor_right.type = LINEWISE

def cursor_down(editor):
    row, col = editor.row, editor.col
    row = min(row + 1, editor.buffer.numlines())
    return row, col
cursor_right.type = LINEWISE


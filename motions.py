"""A motion is represented as a function as follows:

It should take an Editor and return a tuple of end coordinates. (row, col)

It should also have an 'type' attribute with value INCLUSIVE, EXCLUSIVE, or
LINEWISE.
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


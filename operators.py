"""An operator is represented as a function as follows:

1) It should take these arguments:
  - an Editor
  - a tuple of start coordinates (row, col)
  - a tuple of end coordinates (row, col)
  - the type of motion, one of: LINEWISE, CHARACTERWISE, BLOCKWISE

2) As a side effect, it should modify the Editor's Buffer, doing whatever
operation it's for. (i.e., "delete" should actually delete the relevant text)

3) It should return a tuple of:
  - a tuple (start, end) describing an inclusive range of lines that need to
    be redrawn in the display, or False if no lines need to be redrawn
  - a tuple of coordinates (row, col) where the cursor should be placed after
    the operation

Note: This works similarly to Vim's g@. See :help g@
"""

from constants import *

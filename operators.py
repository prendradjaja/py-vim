"""An operator is represented as a subclass of Operator as follows:

1) It has an 'execute' method that implements the operation:
   a. It takes these arguments:
       - an Editor
       - a tuple of lines of text to operate on (This is affected by the
         'optype' attribute -- see below)
       - the type of motion, with value LINEWISE, CHARACTERWISE, or BLOCKWISE
   b. It returns a modified version of the second argument, if necessary.
   c. It can modify the state of the editor as well, if necessary. This is
      used by operators like 'yank' and 'fold'.

2) It has a mandatory 'optype' attribute and an optional 'cursorpos'
attribute.

 - optype can be: LINEWISE or CHARACTERWISE.
      Note that operators are not mentioned as having types like this in the
      Vim documentation; only motions are.

      Linewise operators affect whole lines. Characterwise operators can
      affect partial lines. Accordingly, there are the following two
      distinctions in the API for operators based on operator type:

         a. After the operation, the cursor is placed in different places
            relative to the text operated on:
             - For a LINEWISE operator, it is placed at the first non-blank
               character on the first line of the text.
             - For a CHARACTERWISE operator, it is placed at the first
               character in the text.
            This behavior occurs with 'cursorpos' set to the default, START.
            Setting it to END places the cursor at the end of the text
            instead, either at the last character of the text or the first
            non-blank character on the last line of the text.

         b. The second argument supplied to a linewise operator consists of
            whole lines. For example, consider this example text. With the
            cursor on the "i" in "ipsum," the "2w" motion will place the
            cursor on the "s" in "sit."

               Lorem ipsum
               dolor sit
               amet

            Using a linewise operator supplies both full lines to the operator
            function, so the tuple ('Lorem ipsum', 'dolor sit') is given.

            In contrast, a characterwise operator does not need all of those
            characters, so the tuple ('ipsum', 'dolor ') is given. Note that
            the second string has a space at the end, but does not have an
            "s". Since "w" is an exclusive motion, the endpoint of the motion
            is not included. If it were inclusive, this tuple would be given
            instead: ('ipsum', 'dolor s')

 - cursorpos is by default set to START. If it's set to end, the cursor is
   placed at the end of the text operated on.
"""

from constants import *

class Operator:
    optype = UNSPECIFIED # override me
    cursorpos = START # default value
    def execute(editor, text, motion_type): # override me
        raise Exception(NOT_IMPLEMENTED)

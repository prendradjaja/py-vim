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

2) It has two optional attributes:
 - optype is by default set to CHARACTERWISE. It can be set to LINEWISE
   instead.
      Note that operators are not mentioned as having types like this in the
      Vim documentation; only motions are.

      Most operators are characterwise, like "d" and "c". Linewise operators
      like ">" are special in that they affect whole lines. For example, using
      ">w" doesn't just indent a word. Indentation affects an entire line.
      There are the following two distinctions in the API for operators based
      on operator type:

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

            However, a characterwise operator acts as a linewise operator when
            used with a linewise motion, so using the "j" motion gives both
            linewise and characterwise operators the tuple ('Lorem ipsum',
            'dolor sit') as the second argument.

 - cursorpos is by default set to START. It can be set to END instead, which
   affects cursor placement after the operation. See details above.
"""

from constants import *

class Operator:
    optype = CHARACTERWISE # default. can also be LINEWISE
    cursorpos = START # default. can also be END
    def execute(editor, text, motion_type):
        """Override me: return result text"""
        raise Exception(ABSTRACT_METHOD)

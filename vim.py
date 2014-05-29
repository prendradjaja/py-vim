import curses

import motions
import operators
import util
from constants import *

class Buffer: # {{{
    """A one-indexed buffer of text (top left corner is row 1, column 1)"""
    def __init__(self, lines):
        self._contents = lines

    def line(self, row):
        """Return string: the contents of a specified line"""
        return self._contents[row-1]

    def lines(self, start, end):
        """Return tuple of strings: the specified lines (inclusive)"""
        return tuple(self._contents[start-1:end])

    def replace_lines(self, start, end, new_text):
        """Replace the specified lines (inclusive) with new text (a tuple or
        list of strings)"""
        self._contents[start-1:end] = new_text

    def all_lines(self):
        """Return tuple of strings: all lines"""
        return tuple(self._contents)

    def numlines(self):
        """Return the number of lines."""
        return len(self._contents)

    def insertchar(self, row, col, char):
        """Insert a character at the specified position"""
        s = self._contents[row-1]
        s = s[:col-1] + char + s[col-1:]
        self._contents[row-1] = s

    def deletechar(self, row, col):
        """Delete a character at the specified position"""
        s = self._contents[row-1]
        s = s[:col-1] + s[col:]
        self._contents[row-1] = s

    def dump(self):
        """Return string: the whole buffer contents"""
        return '\n'.join(self._contents) + '\n'

# }}}

class Editor: # {{{
    def __init__(self, win):
        self.mode = NORMAL
        self.buffer = Buffer(["Lorem ipsum dolor sit amet,",
                              "consectetur adipisicing elit",
                              "ed do eiusmod"])
        self.win = win
        self.bindings = self.defaultbindings()
        self.winpos = 1
        self.col = 1
        self.row = 1
        self.showbuffer()
        self.positioncursor()
        self.pending_operator = None

    def mainloop(self):
        try:
            while True:
                self.processkey(self.win.getkey())
        except KeyboardInterrupt:
            return

    def processkey(self, key):
        if self.mode is NORMAL:
            if key in self.bindings[OPERATOR]:
                self.mode = OPERATOR_PENDING
                self.pending_operator = self.bindings[OPERATOR][key]
            elif key in self.bindings[MOTION]:
                self.row, self.col = self.bindings[MOTION][key].execute(self)
                self.positioncursor()
            elif key in self.bindings[NORMAL]:
                self.bindings[NORMAL][key]()
        elif self.mode is INSERT:
            if key in self.bindings[INSERT]:
                self.bindings[INSERT][key]()
            elif key in SELF_INSERTABLE_CHARS:
                self.insertchar(key)
        elif self.mode is OPERATOR_PENDING:
            if key in self.bindings[MOTION]:
                operator, self.pending_operator = self.pending_operator, None
                self.mode = NORMAL
                self.execute_command(operator, self.bindings[MOTION][key])


    def execute_command(self, operator, motion):
        # my responsibilities:
        #   1. extract the text by executing the motion
        #   2. execute the operator
        #   3. replace the text
        #   4. place the cursor
        #   5. redraw
        command_is_linewise = (motion.type is LINEWISE or
                              operator.optype is LINEWISE)

        # 1. extract text
        if command_is_linewise:
            row_now = self.row
            row_after_motion, _ = motion.execute(self)
            firstrow, lastrow = sorted((row_now, row_after_motion))
            old_text = self.buffer.lines(firstrow, lastrow)
        else:
            pos_now = self.row, self.col
            pos_after_motion = motion.execute(self)
            (firstrow, firstcol), (lastrow, lastcol) = sorted((pos_now, pos_after_motion))
            if motion.type is EXCLUSIVE:
                # TODO this is a hack for "if exclusive, cut last char"
                # use an iterator on coordinates instead? this will fail at SOL
                lastcol -= 1
            old_text = list(self.buffer.lines(firstrow, lastrow))
            old_text[-1], back = util.split_at(lastcol, old_text[-1])
            front, old_text[0] = util.split_at(firstcol-1, old_text[0])
            old_text = tuple(old_text)

        # 2. execute operator
        motion_type = motion.type
        if motion_type in (EXCLUSIVE, INCLUSIVE):
            motion_type = CHARACTERWISE
        new_text = operator.execute(self, old_text, motion_type)

        # 3. replace text
        if command_is_linewise:
            self.buffer.replace_lines(firstrow, lastrow, new_text)
        else:
            new_text = list(new_text)
            new_text[0] = front + new_text[0]
            new_text[-1] = new_text[-1] + back
            self.buffer.replace_lines(firstrow, lastrow, new_text)

        # 4. place cursor (TODO)
        # default works for a lot of stuff but fails for (at least):
        #  - backwards motions
        #  - linewise operators

        # 6. redraw
        # TODO? this redraws everything
        self.showbuffer()
        self.positioncursor()
        self.print(self.buffer.numlines())

    # Display {{{
    def positioncursor(self):
        """Move the terminal cursor to match the editor cursor"""
        x = self.col - 1
        y = self.row - self.winpos
        self.win.move(y, x)

    def showbuffer(self):
        self.win.clear()
        for y, line in enumerate(self.buffer.all_lines()):
            self.win.addstr(y, 0, line)
        self.win.refresh()

    # }}}

    # For changing modes {{{
    def insert(self):
        self.mode = INSERT

    def normal(self):
        self.mode = NORMAL

    # }}}

    # Editor commands {{{
    def insertchar(self, char):
        # Add to buffer and display
        self.buffer.insertchar(self.row, self.col, char)
        self.win.insch(self.row-1, self.col-1, char)
        # Move cursor
        self.col += 1
        self.positioncursor()
        # Show buffer (debug)
        self.show_debugging_buffer()

    def delete_char(self):
        self.buffer.deletechar(self.row, self.col)
        self.win.delch(self.row-1, self.col-1)

    # }}}

    # Other {{{
    def defaultbindings(self):
        return {
                NORMAL: {
                    'i': self.insert,
                    'x': self.delete_char,
                    '\\': self.show_debugging_buffer,
                    },
                OPERATOR: {
                    },
                MOTION: {
                    'h': motions.left,
                    'l': motions.right,
                    'k': motions.up,
                    'j': motions.down,
                    },
                INSERT: {
                    '\\': self.normal,
                    },
                }

    def show_debugging_buffer(self):
        self.print(self.buffer.dump())

    def print(self, *s, y=20):
        """Print some text (for debugging)"""
        pos = self.win.getyx()
        WIDTH = 40
        HEIGHT = 8
        self.win.addstr(y-1, 0, ('`'*WIDTH+'\n')*HEIGHT)
        self.win.addstr(y, 0, ' '.join(str(each) for each in s))
        self.win.move(*pos)
        self.win.refresh()

    # }}}

# }}}

def main(win):
    editor = Editor(win)
    editor.mainloop()

if __name__ == '__main__':
    # This runs main, supplying it with a window
    curses.wrapper(main)

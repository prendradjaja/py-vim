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

    def char(self, row, col):
        # TODO figure out behavior for invalid row or invalid col
        if col == len(self._contents[row-1]) + 1:
            return '\n'
        return self._contents[row-1][col-1]

    def all_lines(self):
        """Return tuple of strings: all lines"""
        return tuple(self._contents)

    def num_lines(self):
        """Return the number of lines."""
        return len(self._contents)

    def insert_char(self, row, col, char):
        """Insert a character at the specified position"""
        s = self._contents[row-1]
        s = s[:col-1] + char + s[col-1:]
        self._contents[row-1] = s

    def delete_char(self, row, col):
        """Delete a character at the specified position"""
        s = self._contents[row-1]
        s = s[:col-1] + s[col:]
        self._contents[row-1] = s

    # should this yield linebreaks?
    def coords_iterator(self, row, col, direction, include_start=False):
        if include_start:
            yield row, col
        while row <= self.num_lines():
            while col <= len(self._contents[row-1]):
                col += 1
                yield row, col
            col = 0
            row += 1

    def iterator(self, row, col, direction, include_start=False):
        for each in self.coords_iterator(row, col, direction, include_start):
            yield each, self.char(*each)

    def dump(self):
        """Return string: the whole buffer contents"""
        return '\n'.join(self._contents) + '\n'

# }}}

class InputSource:
    """Gives input to an editor"""
    pass

class UserInputHandler(InputSource):
    """Gives input from a user (through a curses window) to an editor"""
    def __init__(self, win, editor):
        self.win = win
        self.editor = editor

    def main_loop(self):
        try:
            while True:
                self.editor.process_key(self.win.getkey())
        except KeyboardInterrupt:
            return

class NoDisplay:
    def position_cursor(self, *args):
        pass

    def show(self, *args):
        pass

    def print(self, *args):
        pass

class Display:
    def __init__(self, win):
        self.win = win

    def position_cursor(self, editor):
        """Move the terminal cursor to match the editor cursor"""
        x = editor.col - 1
        y = editor.row - editor.winpos
        self.win.move(y, x)

    def show(self, editor):
        self.win.clear()
        for y, line in enumerate(editor.buffer.all_lines()):
            self.win.addstr(y, 0, line)
        self.position_cursor(editor)
        self.win.refresh()

    def print(self, *s, y=20):
        """Print some text (for debugging)"""
        pos = self.win.getyx()
        WIDTH = 40
        HEIGHT = 8
        self.win.addstr(y-1, 0, ('`'*WIDTH+'\n')*HEIGHT)
        self.win.addstr(y, 0, ' '.join(str(each) for each in s))
        self.win.move(*pos)
        self.win.refresh()

class Editor: # {{{
    def __init__(self, display=None):
        if display is None:
            self.display = NoDisplay()
        else:
            self.display = display
        self.mode = NORMAL
        self.buffer = Buffer(["Lorem ipsum dolor sit amet,",
                              "consectetur adipisicing elit",
                              "ed do eiusmod"])
        self.bindings = self.default_bindings()
        self.winpos = 1
        self.col = 1
        self.row = 1
        self.pending_operator = None
        self.display.show(self)

    def process_key(self, key):
        if self.mode is NORMAL:
            if key in self.bindings[OPERATOR]:
                self.mode = OPERATOR_PENDING
                self.pending_operator = self.bindings[OPERATOR][key]
            elif key in self.bindings[MOTION]:
                self.row, self.col = self.execute_motion(self.bindings[MOTION][key])
                self.display.position_cursor(self)
            elif key in self.bindings[NORMAL]:
                self.bindings[NORMAL][key]()
        elif self.mode is INSERT:
            if key in self.bindings[INSERT]:
                self.bindings[INSERT][key]()
            elif key in SELF_INSERTABLE_CHARS:
                self.insert_char(key)
        elif self.mode is OPERATOR_PENDING:
            if key in self.bindings[MOTION]:
                operator, self.pending_operator = self.pending_operator, None
                self.mode = NORMAL
                self.execute_command(operator, self.bindings[MOTION][key])

    def execute_motion(self, motion):
        return motion.execute(self.row, self.col, self.buffer)

    def execute_command(self, operator, motion):
        # my responsibilities:
        #   1. extract the text by executing the motion
        #   2. execute the operator
        #   3. replace the text
        #   4. place the cursor
        #   5. tell the display to redraw
        command_is_linewise = (motion.type is LINEWISE or
                              operator.optype is LINEWISE)

        # 1. extract text
        if command_is_linewise:
            row_now = self.row
            row_after_motion, _ = self.execute_motion(motion)
            firstrow, lastrow = sorted((row_now, row_after_motion))
            old_text = self.buffer.lines(firstrow, lastrow)
        else:
            pos_now = self.row, self.col
            pos_after_motion = self.execute_motion(motion)
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

        # 5. tell display to redraw
        # TODO? this redraws everything
        self.display.show(self)
        self.display.print(self.buffer.num_lines())

    # For changing modes {{{
    def insert(self):
        self.mode = INSERT

    def normal(self):
        self.mode = NORMAL

    # }}}

    # Editor commands {{{
    def insert_char(self, char):
        # Add to buffer and display
        self.buffer.insert_char(self.row, self.col, char)
        self.display.win.insch(self.row-1, self.col-1, char)
        # Move cursor
        self.col += 1
        self.display.position_cursor(self)
        # Show buffer (debug)
        self.show_debugging_buffer()

    def delete_char(self):
        self.buffer.delete_char(self.row, self.col)
        self.display.win.delch(self.row-1, self.col-1)

    # }}}

    # Other {{{
    def default_bindings(self):
        return {
                NORMAL: {
                    'i': self.insert,
                    'x': self.delete_char,
                    '\\': self.show_debugging_buffer,
                    },
                OPERATOR: {
                    'd': operators.delete,
                    'g': operators.uppercase,
                    '>': operators.increase_indent,
                    },
                MOTION: {
                    'h': motions.left,
                    'l': motions.right,
                    'k': motions.up,
                    'j': motions.down,
                    's': motions.right_three_times,
                    'J': motions.down_charwise,
                    '0': motions.first_column,
                    '$': motions.last_column,
                    '^': motions.first_nonblank,
                    },
                INSERT: {
                    '\\': self.normal,
                    },
                }

    def show_debugging_buffer(self):
        self.display.print(self.buffer.dump())

    # }}}

# }}}

def main(win):
    display = Display(win)
    editor = Editor(display)
    input_source = UserInputHandler(win, editor)
    input_source.main_loop()

if __name__ == '__main__':
    # This runs main, supplying it with a window
    curses.wrapper(main)

import curses

NORMAL, INSERT, OPERATOR = range(3)

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

    def numlines(self):
        """Return the number of lines."""
        return len(self._contents)

    def insertchar(self, row, col, char):
        """Insert a character at the specified position"""
        s = self._contents[row-1]
        s = s[:col-1] + char + s[col-1:]
        self._contents[row-1] = s

    def dump(self):
        """Return string: the whole buffer contents"""
        return '\n'.join(self._contents)

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

    def mainloop(self):
        try:
            while True:
                self.processkey(self.win.getkey())
        except KeyboardInterrupt:
            return

    def processkey(self, key):
        if key in self.bindings[self.mode]:
            self.bindings[self.mode][key]()
        elif self.mode is INSERT:
            self.insertchar(key)

    # Display {{{
    def positioncursor(self):
        """Move the terminal cursor to match the editor cursor"""
        x = self.col - 1
        y = self.row - self.winpos
        self.win.move(y, x)

    def showbuffer(self):
        self.win.clear()
        for y, line in enumerate(self.buffer.lines(self.row, self.buffer.numlines())):
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
    def cursor_left(self):
        if self.col > 1:
            self.col -= 1
            self.positioncursor()
    def cursor_right(self):
        if True:
            self.col += 1
            self.positioncursor()
    def cursor_down(self):
        if True:
            self.row += 1
            self.positioncursor()
    def cursor_up(self):
        if self.row > 1:
            self.row -= 1
            self.positioncursor()

    def insertchar(self, char):
        # Add to buffer and display
        self.buffer.insertchar(self.row, self.col, char)
        self.win.insch(self.row-1, self.col-1, char)
        # Move cursor
        self.col += 1
        self.positioncursor()
        # Show buffer (debug)
        self.print(self.buffer.dump())

    # }}}

    # Other {{{
    def defaultbindings(self):
        return {
                NORMAL: {
                    'h': self.cursor_left,
                    'l': self.cursor_right,
                    'j': self.cursor_down,
                    'k': self.cursor_up,
                    'i': self.insert,
                    },
                INSERT: {
                    '\\': self.normal,
                    },
                }

    def print(self, s, y=20):
        """Print some text (for debugging)"""
        pos = self.win.getyx()
        self.win.addstr(y, 0, s)
        self.win.move(*pos)
        self.win.refresh()

    # }}}

# }}}

def main(win):
    editor = Editor(win)
    editor.mainloop()

# This runs main, supplying it with a window
curses.wrapper(main)

import time

ESCAPE_CHARACTER = "\x1B"

ENUM_CLEAR_MODE_TO_START = 0
ENUM_CLEAR_MODE_TO_END = 1
ENUM_CLEAR_MODE_ALL = 2
ENUM_CLEAR_MODE_HISTORY = 3

ENUM_KEY_ESCAPE = ESCAPE_CHARACTER
ENUM_KEY_UP = ESCAPE_CHARACTER + "[A"
ENUM_KEY_DOWN = ESCAPE_CHARACTER + "[B"
ENUM_KEY_LEFT = ESCAPE_CHARACTER + "[D"
ENUM_KEY_RIGHT = ESCAPE_CHARACTER + "[C"
ENUM_KEY_F1 = ESCAPE_CHARACTER + "[OP"
ENUM_KEY_F2 = ESCAPE_CHARACTER + "[OQ"
ENUM_KEY_F3 = ESCAPE_CHARACTER + "[OR"
ENUM_KEY_F4 = ESCAPE_CHARACTER + "[OS"
ENUM_KEY_F5 = ESCAPE_CHARACTER + "[15~"
ENUM_KEY_F6 = ESCAPE_CHARACTER + "[17~"
ENUM_KEY_F7 = ESCAPE_CHARACTER + "[18~"
ENUM_KEY_F8 = ESCAPE_CHARACTER + "[19~"
ENUM_KEY_F9 = ESCAPE_CHARACTER + "[20~"
ENUM_KEY_F10 = ESCAPE_CHARACTER + "[21~"
ENUM_KEY_F11 = ESCAPE_CHARACTER + "[23~"
ENUM_KEY_F12 = ESCAPE_CHARACTER + "[24~"

KEY_TIMEOUT_RATE = 0.5

class CharacterReader_Windows:
    def __init__(self):
        import msvcrt
    
    def __call__(self, blocking = False):
        import msvcrt

        if msvcrt.kbhit() or blocking:
            return msvcrt.getch()
        else:
            return None

class CharacterReader_Unix:
    def __init__(self):
        import tty, sys

    def __call__(self, blocking = False):
        import sys, tty, termios, select

        file = sys.stdin.fileno()
        old = termios.tcgetattr(file)

        try:
            tty.setraw(sys.stdin.fileno())

            if blocking:
                return sys.stdin.read(1)
            else:
                while select.select([sys.stdin], [], [], KEY_TIMEOUT_RATE)[0]:
                    return sys.stdin.read(1)
                
                return None
        finally:
            termios.tcsetattr(file, termios.TCSADRAIN, old)
        
        return character

class CharacterReader:
    def __init__(self):
        try:
            self.implementation = CharacterReader_Windows()
        except ImportError:
            self.implementation = CharacterReader_Unix()
        
    """
    Gets a single character from stdin.
    
    If `blocking` is `True`, this waits until a character is pressed.
    If `blocking` is `False`, this does not wait until a charcater is pressed.
    If no character is pressed, then `None` is returned. Otherwise, a string
    containing the chracter is returned.
    """
    def __call__(self, blocking = False):
        character = self.implementation(blocking)

        if character == "\x03":
            raise KeyboardInterrupt
        elif character == "\x04":
            raise EOFError
        else:
            return character

"""
Writes the contents of `contents` to the screen, without a newline.
"""
def write(contents = ""):
    print(contents, end = "", flush = True)

"""
Gets a single character from stdin.

If `blocking` is `True`, this waits until a character is pressed.
If `blocking` is `False`, this does not wait until a character is pressed.
If no character is pressed, then `None` is returned. Otherwise, a string
containing the character is returned.
"""
def getCharacter(blocking = False):
    return CharacterReader()(blocking)

"""
Gets a single keypress from stdin.

If `blocking` is `True`, this waits until a key is pressed.
If `blocking` is `False`, this does not wait until a key is pressed.
If no key is pressed, then `None` is returned. Otherwise, a string containing
the key is returned.
"""
def getKey(blocking = False):
    firstCharacter = getCharacter(blocking)

    if firstCharacter == ESCAPE_CHARACTER:
        secondCharacter = getCharacter(True)

        if secondCharacter == "[":
            thirdCharacter = getCharacter(True)

            if thirdCharacter == "A":
                return ENUM_KEY_UP
            elif thirdCharacter == "B":
                return ENUM_KEY_DOWN
            elif thirdCharacter == "D":
                return ENUM_KEY_LEFT
            elif thirdCharacter == "C":
                return ENUM_KEY_RIGHT
            elif thirdCharacter == "1":
                fourthCharacter = getCharacter(True)

                getCharacter(True) # For skipping `~`

                if fourthCharacter == "4":
                    return ENUM_KEY_F4
                elif fourthCharacter == "5":
                    return ENUM_KEY_F5
                elif fourthCharacter == "7":
                    return ENUM_KEY_F6
                elif fourthCharacter == "8":
                    return ENUM_KEY_F7
                elif fourthCharacter == "9":
                    return ENUM_KEY_F8
            elif thirdCharacter == "2":
                fourthCharacter = getCharacter(True)

                getCharacter(True) # For skipping `~`

                if fourthCharacter == "0":
                    return ENUM_KEY_F9
                elif fourthCharacter == "1":
                    return ENUM_KEY_F10
                elif fourthCharacter == "3":
                    return ENUM_KEY_F11
                elif fourthCharacter == "4":
                    return ENUM_KEY_F12
        elif secondCharacter == "O":
            thirdCharacter = getCharacter(True)

            if thirdCharacter == "P":
                return ENUM_KEY_F1
            elif thirdCharacter == "Q":
                return ENUM_KEY_F2
            elif thirdCharacter == "R":
                return ENUM_KEY_F3
            elif thirdCharacter == "S":
                return ENUM_KEY_F4
        elif secondCharacter == ESCAPE_CHARACTER:
            return ENUM_KEY_ESCAPE
    else:
        return firstCharacter

"""
Moves the cursor up by `cells` cells.
"""
def moveCursorUp(cells = 1):
    write("{}[{}A".format(ESCAPE_CHARACTER, cells))

"""
Moves the cursor down by `cells` cells.
"""
def moveCursorDown(cells = 1):
    write("{}[{}B".format(ESCAPE_CHARACTER, cells))

"""
Moves the cursor left by `cells` cells.
"""
def moveCursorLeft(cells = 1):
    write("{}[{}D".format(ESCAPE_CHARACTER, cells))

"""
Moves the cursor right by `cells` cells.
"""
def moveCursorRight(cells = 1):
    write("{}[{}C".format(ESCAPE_CHARACTER, cells))

"""
Moves the cursor to cell `x` on the current line (starting at `0`).
"""
def moveCursorInLine(x = 0):
    write("{}[{}G".format(ESCAPE_CHARACTER, x + 1))

"""
Moves the cursor to the cell at the `x` and `y` coordinates (starting at `0`).
"""
def moveCursorTo(x = 0, y = 0):
    write("{}[{};{}H".format(ESCAPE_CHARACTER, y + 1, x + 1))

"""
Clears the screen with the specified mode.

Mode options:
* `ENUM_CLEAR_MODE_TO_START` clears the screen from the cursor to the start of
  the screen.
* `ENUM_CLEAR_MODE_TO_END` clears the screen from the cursor to the end of the
  screen.
* `ENUM_CLEAR_MODE_ALL` clears the entire screen (excluding the scrollback
  buffer).
* `ENUM_CLEAR_MODE_HISTORY` clears the entire screen, including the
  scrollback buffer.
"""
def clearScreen(mode = ENUM_CLEAR_MODE_ALL):
    if mode == ENUM_CLEAR_MODE_TO_START:
        write("{}[1J".format(ESCAPE_CHARACTER))
    elif mode == ENUM_CLEAR_MODE_TO_END:
        write("{}[0J".format(ESCAPE_CHARACTER))
    elif mode == ENUM_CLEAR_MODE_ALL:
        write("{}[2J".format(ESCAPE_CHARACTER))
    elif mode == ENUM_CLEAR_MODE_HISTORY:
        write("{}[3J".format(ESCAPE_CHARACTER))
    else:
        raise ValueError("Mode value does not exist")

"""
Clears the current line with the specified mode.

Mode options:
* `ENUM_CLEAR_MODE_TO_START` clears the screen from the cursor to the start of
  the line.
* `ENUM_CLEAR_MODE_TO_END` clears the screen from the cursor to the end of the
  line.
* `ENUM_CLEAR_MODE_ALL` clears the entire line.
"""
def clearLine(mode = ENUM_CLEAR_MODE_ALL):
    if mode == ENUM_CLEAR_MODE_TO_START:
        write("{}[1K".format(ESCAPE_CHARACTER))
    elif mode == ENUM_CLEAR_MODE_TO_END:
        write("{}[0K".format(ESCAPE_CHARACTER))
    elif mode == ENUM_CLEAR_MODE_ALL:
        write("{}[2K".format(ESCAPE_CHARACTER))
    else:
        raise ValueError("Mode value does not exist")

"""
Scrolls the screen up by `lines` lines.
"""
def scrollUp(lines = 1):
    write("{}[{}S".format(ESCAPE_CHARACTER, cells))

"""
Scrolls the screen down by `lines` lines.
"""
def scrollDown(lines = 1):
    write("{}[{}T".format(ESCAPE_CHARACTER, cells))

"""
Gets the current cursor position. A dictionary containing the `x` and `y`
coordinates of the cursor position is returned.

The `x` and `y` coordinates start at `0`.
"""
def getCursorPosition():
    write("{}[6n".format(ESCAPE_CHARACTER))

    output = ""
    lastCharacter = None

    while lastCharacter != "R":
        lastCharacter = getCharacter(True)
        output += lastCharacter
    
    x = int(output.split("R")[0].split(";")[1]) - 1
    y = int(output.split("[")[1].split(";")[0]) - 1

    return {
        "x": x,
        "y": y
    }

"""
Shows the cursor indicator.
"""
def showCursor():
    write("{}[?25h".format(ESCAPE_CHARACTER))

"""
Hides the cursor indicator.
"""
def hideCursor():
    write("{}[?25l".format(ESCAPE_CHARACTER))
import vtk.term as term

class Style:
    def __init__(self):
        self.code = 0
    
    def _render(self):
        return "{}[{}m".format(term.ESCAPE_CHARACTER, self.code)

class Style_Reset(Style):
    def __init__(self):
        super()

        self.code = 0

class Style_Bold(Style):
    def __init__(self):
        super()

        self.code = 1

class Style_Faint(Style):
    def __init__(self):
        super()

        self.code = 2

class Style_Italic(Style):
    def __init__(self):
        super()

        self.code = 3

class Style_Underline(Style):
    def __init__(self):
        super()

        self.code = 4

class Style_Invert(Style):
    def __init__(self):
        super()

        self.code = 7

class Style_Strikethrough(Style):
    def __init__(self):
        super()

        self.code = 9

class Colour(Style):
    def __init__(self):
        super()

    def _render(self, isForeground = True):
        if isForeground:
            return "{}[{}m".format(term.ESCAPE_CHARACTER, self.code)
        else:
            return "{}[{}m".format(term.ESCAPE_CHARACTER, self.code + 10)

class Colour_Transparent(Colour):
    def _render(self, isForeground = True):
        return ""

class Colour_Black(Colour):
    def __init__(self):
        super()

        self.code = 30

class Colour_DarkRed(Colour):
    def __init__(self):
        super()

        self.code = 31

class Colour_DarkGreen(Colour):
    def __init__(self):
        super()

        self.code = 32

class Colour_DarkYellow(Colour):
    def __init__(self):
        super()

        self.code = 33

class Colour_DarkBlue(Colour):
    def __init__(self):
        super()

        self.code = 34

class Colour_DarkMagenta(Colour):
    def __init__(self):
        super()

        self.code = 35

class Colour_DarkCyan(Colour):
    def __init__(self):
        super()

        self.code = 36

class Colour_Grey(Colour):
    def __init__(self):
        super()

        self.code = 37

class Colour_DarkGrey(Colour):
    def __init__(self):
        super()

        self.code = 90

class Colour_Red(Colour):
    def __init__(self):
        super()

        self.code = 91

class Colour_Green(Colour):
    def __init__(self):
        super()

        self.code = 92

class Colour_Yellow(Colour):
    def __init__(self):
        super()

        self.code = 93

class Colour_Blue(Colour):
    def __init__(self):
        super()

        self.code = 94

class Colour_Magenta(Colour):
    def __init__(self):
        super()

        self.code = 95

class Colour_Cyan(Colour):
    def __init__(self):
        super()

        self.code = 96

class Colour_White(Colour):
    def __init__(self):
        super()

        self.code = 97
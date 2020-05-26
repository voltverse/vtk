import vtk.term
import vtk.styles

vtk.term.clearScreen()
vtk.term.moveCursorTo(0, 0)
vtk.term.hideCursor()
vtk.term.write(vtk.styles.Style_Bold().render() + "Terminal Test" + vtk.styles.Style_Reset().render())

topRow = [
    vtk.styles.Colour_Black,
    vtk.styles.Colour_DarkRed,
    vtk.styles.Colour_DarkGreen,
    vtk.styles.Colour_DarkYellow,
    vtk.styles.Colour_DarkBlue,
    vtk.styles.Colour_DarkMagenta,
    vtk.styles.Colour_DarkCyan,
    vtk.styles.Colour_Grey,
]

bottomRow = [
    vtk.styles.Colour_DarkGrey,
    vtk.styles.Colour_Red,
    vtk.styles.Colour_Green,
    vtk.styles.Colour_Yellow,
    vtk.styles.Colour_Blue,
    vtk.styles.Colour_Magenta,
    vtk.styles.Colour_Cyan,
    vtk.styles.Colour_White
]

cursorX = 0
cursorY = 0

try:
    while True:
        for i in range(0, len(topRow)):
            vtk.term.moveCursorTo(i * 2, 2)

            if cursorX == i and cursorY == 0:
                vtk.term.write(topRow[i]().render(False) + vtk.styles.Colour_White().render() + "[]" + vtk.styles.Style_Reset().render())
            else:
                vtk.term.write(topRow[i]().render(False) + vtk.styles.Colour_White().render() + "  " + vtk.styles.Style_Reset().render())
        
        for i in range(0, len(bottomRow)):
            vtk.term.moveCursorTo(i * 2, 3)
            
            if cursorX == i and cursorY == 1:
                vtk.term.write(bottomRow[i]().render(False) + vtk.styles.Colour_Black().render() + "[]" + vtk.styles.Style_Reset().render())
            else:
                vtk.term.write(bottomRow[i]().render(False) + vtk.styles.Colour_Black().render() + "  " + vtk.styles.Style_Reset().render())
        
        vtk.term.moveCursorTo(cursorX * 2, cursorY + 2)
        
        nextAction = vtk.term.getKey(True)

        if nextAction == vtk.term.ENUM_KEY_UP:
            cursorY = 0
        elif nextAction == vtk.term.ENUM_KEY_DOWN:
            cursorY = 1
        elif nextAction == vtk.term.ENUM_KEY_LEFT:
            cursorX -= 1

            if cursorX < 0:
                cursorX = 0
        elif nextAction == vtk.term.ENUM_KEY_RIGHT:
            cursorX += 1

            if cursorX > max(len(topRow) - 1, len(bottomRow) - 1):
                cursorX = max(len(topRow) - 1, len(bottomRow) - 1)
except KeyboardInterrupt:
    vtk.term.write(vtk.styles.Style_Reset().render())
    vtk.term.clearScreen()
    vtk.term.moveCursorTo(0, 0)
    vtk.term.showCursor()
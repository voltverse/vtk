import math
import textwrap

import vtk.term
import vtk.theming

PLACE_DIRECTION_FREE = -1
PLACE_DIRECTION_NEXT_TO = 0
PLACE_DIRECTION_UNDER = 1

class Event:
    def __init__(self):
        pass

class KeyPressEvent(Event):
    def __init__(self, key):
        super().__init__()

        self.key = key

class EventListener:
    def __init__(self, event, action):
        self.event = event
        self.action = action

class Measurement:
    def __init__(self, percentageLength, deltaLength, relativeMeasurement = None):
        self.percentageLength = percentageLength
        self.deltaLength = deltaLength
        self.relativeMeasurement = relativeMeasurement
    
    def measure(self):
        absoluteMeasurementValue = 0

        if self.relativeMeasurement != None:
            absoluteMeasurementValue = math.floor(self.relativeMeasurement.measure() * self.percentageLength)
        
        return absoluteMeasurementValue + self.deltaLength

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Component:
    def __init__(self, parent):
        self.parent = parent
        self.children = []
        self.eventListeners = []
    
    def place(self):
        self.parent.children.append(self)
    
    def on(self, event, action):
        self.eventListeners.append(EventListener(event, action))
    
    def off(self, event):
        newEventListeners = []

        for eventListener in self.eventListeners:
            if eventListener.event != event:
                newEventListeners.append(eventListener)
        
        self.eventListeners = newEventListeners
    
    def handleEvent(self, event):
        for eventListener in self.eventListeners:
            if eventListener.event == type(event):
                eventListener.action(event = event)
    
    def emitEvent(self, event, captured = None, sender = None):
        if sender == None:
            sender = self

        self.handleEvent(event)

        for child in children:
            child.emitEvent(event, True, sender)
        
        parent.emitEvent(event, False, sender)

class Application(Component):
    def __init__(self):
        super().__init__(None)

        self.running = False
        self.currentFocussedElement = None
        self.x = Measurement(0, 0)
        self.y = Measurement(0, 0)
        self.width = Measurement(0, vtk.term.getTerminalSize()["width"])
        self.height = Measurement(0, vtk.term.getTerminalSize()["height"])
        self.innerWidth = Measurement(0, vtk.term.getTerminalSize()["width"])
        self.innerHeight = Measurement(0, vtk.term.getTerminalSize()["height"])
        self.padding = Measurement(0, 0)
        self.paddingTop = Measurement(0, 0)
        self.paddingBottom = Measurement(0, 0)
        self.paddingLeft = Measurement(0, 0)
        self.paddingRight = Measurement(0, 0)
    
    def _render(self, forceChange = False):
        for child in self.children:
            child._render()

    def place(self):
        raise AttributeError("Application is the root, and has no parent")

    def start(self):
        self.running = True

        try:
            vtk.term.hideCursor()

            self._render(True)

            forceNextRender = False

            while self.running: # Render loop
                self._render(forceNextRender)

                forceNextRender = False
                waitingForEvent = True

                while waitingForEvent: # Event loop
                    try:
                        keyPressed = vtk.term.getKey()

                        if keyPressed != None:
                            if self.currentFocussedElement != None:
                                self.currentFocussedElement.emitEvent(KeyPressEvent(keyPressed))

                            waitingForEvent = False
                    except:
                        vtk.term.write(vtk.styles.Style_Reset()._render())
                        vtk.term.clearScreen()
                        vtk.term.moveCursorTo(0, 0)
                        vtk.term.showCursor()

                        self.running = False
                        waitingForEvent = False
                    
                    if self.width.measure() != vtk.term.getTerminalSize()["width"] or self.height.measure() != vtk.term.getTerminalSize()["height"]:
                        self.width = Measurement(0, vtk.term.getTerminalSize()["width"])
                        self.height = Measurement(0, vtk.term.getTerminalSize()["height"])

                        waitingForEvent = False
                        forceNextRender = True
        except Exception as e:
            vtk.term.write(vtk.styles.Style_Reset()._render())
            vtk.term.clearScreen()
            vtk.term.moveCursorTo(0, 0)
            vtk.term.showCursor()

            # TODO: Add more info for errors
            if type(e) != KeyboardInterrupt:
                print(e)

class Widget(Component):
    def __init__(self, parent):
        super().__init__(parent)

        self._hasChanges = False
        self._x = Measurement(0, 0, self.parent.innerWidth)
        self._y = Measurement(0, 0, self.parent.innerHeight)
        self._width = Measurement(1, 0, self.parent.innerWidth)
        self._height = Measurement(1, 0, self.parent.innerHeight)
        self._paddingTop = Measurement(0, 0, self.parent.innerHeight)
        self._paddingBottom = Measurement(0, 0, self.parent.innerHeight)
        self._paddingLeft = Measurement(0, 0, self.parent.innerWidth)
        self._paddingRight = Measurement(0, 0, self.parent.innerWidth)
        self._backgroundColour = vtk.theming.backgroundColour
        self._foregroundColour = vtk.theming.foregroundColour

    def _render(self):
        for child in self.children:
            if self._hasChanges:
                child._hasChanges = True

            child._render()
    
    def place(self, placeDirection = PLACE_DIRECTION_NEXT_TO, placeMargin = Measurement(0, 1)):
        if len(self.parent.children) > 0:
            if placeDirection == PLACE_DIRECTION_NEXT_TO:
                self.x = Measurement(0, self.parent.children[-1].x.measure() + self.parent.children[-1].width.measure() + placeMargin.measure())
                self.y = Measurement(0, self.parent.children[-1].y.measure())

                if self.getAbsolutePosition().x + self.width.measure() > vtk.term.getTerminalSize()["width"]:
                    self.x = 0
                    self.y = Measurement(0, self.parent.children[-1].y.measure() + self.parent.children[-1].height.measure() + placeMargin.measure())
            elif placeDirection == PLACE_DIRECTION_UNDER:
                self.x = 0
                self.y = Measurement(0, self.parent.children[-1].y.measure() + self.parent.children[-1].height.measure() + placeMargin.measure())

        super().place()
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._hasChanges = True

        if type(value) == Measurement:
            self._x = value
        else:
            if value >= 0:
                self._x = Measurement(0, value, self.parent.innerWidth)
            else:
                self._x = Measurement(1, value, self.parent.innerWidth)
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._hasChanges = True

        if type(value) == Measurement:
            self._y = value
        else:
            if value >= 0:
                self._y = Measurement(0, value, self.parent.innerHeight)
            else:
                self._y = Measurement(1, value, self.parent.innerHeight)
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._hasChanges = True

        if type(value) == Measurement:
            self._width = value
        else:
            self._width = Measurement(0, value, self.parent.innerWidth)
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._hasChanges = True

        if type(value) == Measurement:
            self._height = value
        else:
            self._height = Measurement(0, value, self.parent.innerHeight)

    @property
    def innerWidth(self):
        return Measurement(0, self.width.measure() - self.paddingLeft.measure() - self.paddingRight.measure(), self.parent.innerWidth)
    
    @innerWidth.setter
    def innerWidth(self, value):
        self._hasChanges = True

        if type(value) == Measurement:
            self._width = Measurement(0, value.measure() - self.paddingLeft.measure() - self.paddingRight.measure(), self.parent.innerWidth)
        else:
            self._width = Measurement(0, value - self.paddingLeft.measure() - self.paddingRight.measure(), self.parent.innerWidth)

    @property
    def innerHeight(self):
        return Measurement(0, self.height.measure() - self.paddingTop.measure() - self.paddingBottom.measure(), self.parent.innerHeight)
    
    @innerHeight.setter
    def innerHeight(self, value):
        self._hasChanges = True

        if type(value) == Measurement:
            self._width = Measurement(0, value.measure() - self.paddingTop.measure() - self.paddingBottom.measure(), self.parent.innerHeight)
        else:
            self._width = Measurement(0, value - self.paddingTop.measure() - self.paddingBottom.measure(), self.parent.innerHeight)

    @property
    def padding(self):
        return Measurement(0, max(self._paddingTop.measure(), self._paddingBottom.measure(), self._paddingLeft.measure(), self._paddingRight.measure()))
    
    @padding.setter
    def padding(self, value):
        self._hasChanges = True

        padding = 0

        if type(value) == Measurement:
            padding = value
        else:
            padding = Measurement(0, value, self.parent.padding)

        self._paddingTop = padding
        self._paddingBottom = padding
        self._paddingLeft = padding
        self._paddingRight = padding
    
    @property
    def paddingTop(self):
        return self._paddingTop

    @paddingTop.setter
    def paddingTop(self, value):
        self._hasChanges = True

        if type(value) == Measurement:
            self._paddingTop = value
        else:
            self._paddingTop = Measurement(0, value, self.parent.paddingTop)
    
    @property
    def paddingBottom(self):
        return self._paddingBottom
    
    @paddingBottom.setter
    def paddingTop(self, value):
        self._hasChanges = True

        if type(value) == Measurement:
            self._paddingBottom = value
        else:
            self._paddingBottom = Measurement(0, value, self.parent.paddingBottom)

    @property
    def paddingLeft(self):
        return self._paddingLeft
    
    @paddingLeft.setter
    def paddingLeft(self, value):
        self._hasChanges = True

        if type(value) == Measurement:
            self._paddingLeft = value
        else:
            self._paddingLeft = Measurement(0, value, self.parent.paddingLeft)

    @property
    def paddingRight(self):
        return self._paddingRight

    @paddingRight.setter
    def paddingRight(self, value):
        self._hasChanges = True

        if type(value) == Measurement:
            self._paddingRight = value
        else:
            self._paddingRight = Measurement(0, value, self.parent.paddingRight)

    @property
    def backgroundColour(self):
        return self._backgroundColour
    
    @backgroundColour.setter
    def backgroundColour(self, value):
        self._hasChanges = True
        self._backgroundColour = value
    
    @property
    def foregroundColour(self):
        return self._foregroundColour
    
    @foregroundColour.setter
    def foregroundColour(self, value):
        self._hasChanges = True
        self._foregroundColour = value

    def getAbsolutePosition(self):
        absoluteX = 0
        absoluteY = 0
        currentElement = self

        while type(currentElement) != Application:
            if currentElement == self:
                absoluteX += currentElement.x.measure()
                absoluteY += currentElement.y.measure()
            else:
                absoluteX += currentElement.x.measure() + currentElement.paddingLeft.measure()
                absoluteY += currentElement.y.measure() + currentElement.paddingTop.measure()

            currentElement = currentElement.parent
        
        return Point(absoluteX, absoluteY)

class Screen(Widget):
    def __init__(self, parent):
        super().__init__(parent)

        self.padding = 1

    def _render(self):
        vtk.term.write(
            vtk.styles.Style_Reset()._render() +
            self.backgroundColour._render(False) +
            self.foregroundColour._render(True)
        )
        vtk.term.clearScreen()
        vtk.term.moveCursorTo(0, 0)

        super()._render()

class Box(Widget):
    def _render(self):        
        for i in range(0, self.height.measure()):
            vtk.term.moveCursorTo(self.getAbsolutePosition().x, self.getAbsolutePosition().y + i)
            vtk.term.write(
                self.backgroundColour._render(False) +
                self.foregroundColour._render(True) +
                " " * self.width.measure()
            )
        
        super()._render()
        
class Label(Box):
    def __init__(self, parent, text = ""):
        super().__init__(parent)

        self.backgroundColour = vtk.styles.Colour_Transparent()
        self.text = text

    def _render(self):
        super()._render()

        textWrapper = textwrap.TextWrapper(width = self.innerWidth.measure())
        wrappedTextLines = textWrapper.wrap(text = self.text)

        for i in range(0, min(len(wrappedTextLines), self.innerHeight.measure())):
            vtk.term.moveCursorTo(self.getAbsolutePosition().x + self.paddingLeft.measure(), self.getAbsolutePosition().y + self.paddingTop.measure() + i)
            vtk.term.write(
                self.backgroundColour._render(False) +
                self.foregroundColour._render(True) +
                wrappedTextLines[i]
            )
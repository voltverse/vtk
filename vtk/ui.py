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
            absoluteMeasurementValue = self.relativeMeasurement.measure() * self.percentageLength
        
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

            while self.running: # Render loop
                if self.width != Measurement(0, vtk.term.getTerminalSize()["width"]) or self.height != Measurement(0, vtk.term.getTerminalSize()["height"]):
                    self.width = Measurement(0, vtk.term.getTerminalSize()["width"])
                    self.height = Measurement(0, vtk.term.getTerminalSize()["height"])

                    self._render(True)
                else:
                    self._render()
                
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
        self._x = Measurement(0, 0, self.parent.x)
        self._y = Measurement(0, 0, self.parent.y)
        self._width = Measurement(1, 0, self.parent.width)
        self._height = Measurement(1, 0, self.parent.height)
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
            elif placeDirection == PLACE_DIRECTION_UNDER:
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
                self._x = Measurement(0, value, self.parent.x)
            else:
                self._x = Measurement(1, value, self.parent.width)
    
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
                self._y = Measurement(0, value, self.parent.y)
            else:
                self._y = Measurement(1, value, self.parent.height)
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._hasChanges = True

        if type(value) == Measurement:
            self._width = value
        else:
            self._width = Measurement(0, value, self.parent.width)
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._hasChanges = True

        if type(value) == Measurement:
            self._height = value
        else:
            self._height = Measurement(0, value, self.parent.height)

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
            absoluteX += currentElement.x.measure()
            absoluteY += currentElement.y.measure()

            currentElement = currentElement.parent
        
        return Point(absoluteX, absoluteY)

class Screen(Widget):
    def _render(self):
        vtk.term.write(
            vtk.styles.Style_Reset()._render() +
            self.backgroundColour._render(False) +
            self.foregroundColour._render(True)
        )
        vtk.term.clearScreen()
        vtk.term.moveCursorTo(0, 0)

        super()._render()

class Label(Widget):
    def __init__(self, parent, text = ""):
        super().__init__(parent)

        self.backgroundColour = vtk.styles.Colour_Transparent()
        self.text = text

    def _render(self):
        vtk.term.moveCursorTo(self.getAbsolutePosition().x, self.getAbsolutePosition().y)
        vtk.term.write(
            self.backgroundColour._render(False) +
            self.foregroundColour._render(True) +
            self.text[:self.width.measure()]
        )

        super()._render()
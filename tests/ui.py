import vtk.ui
import vtk.styles

application = vtk.ui.Application()
screen = vtk.ui.Screen(application)
label = vtk.ui.Label(screen, text = "Hello!")

screen.backgroundColour = vtk.styles.Colour_DarkBlue()

label.x = 1
label.y = 1

screen.place()
label.place()

application.start()
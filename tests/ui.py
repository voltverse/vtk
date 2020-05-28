import vtk.ui
import vtk.styles

application = vtk.ui.Application()
screen = vtk.ui.Screen(application)
label = vtk.ui.Label(screen, text = "Hello!")
label2 = vtk.ui.Label(screen, text = "Testing!")

screen.backgroundColour = vtk.styles.Colour_DarkBlue()

screen.padding = 10

label.width = 10
label2.width = 10

label.width = vtk.ui.Measurement(0.5, 0, screen.innerWidth)

screen.place()
label.place()
label2.place()

application.start()
import vtk.ui
import vtk.styles

application = vtk.ui.Application()
screen = vtk.ui.Screen(application)
label = vtk.ui.Label(screen, text = "Hello!")
label2 = vtk.ui.Label(screen, text = "Testing!")

screen.backgroundColour = vtk.styles.Colour_DarkBlue()

label.x = 1
label.y = 1
label.width = 10

screen.place()
label.place()
label2.place()

application.start()
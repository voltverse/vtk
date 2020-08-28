import vtk.ui
import vtk.styles

application = vtk.ui.Application()
screen = vtk.ui.Screen(application)
label = vtk.ui.Label(screen, text = "Hello! Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur congue, purus eget placerat vulputate, nisi justo ornare erat, ut vehicula risus ante at nunc. Pellentesque lobortis fermentum ornare. Sed elementum vestibulum velit, eu molestie dui fermentum in. Etiam at viverra lorem. Vivamus pellentesque urna ut faucibus consequat. Sed ultricies eu sapien quis ullamcorper. Vivamus et nisi interdum, vehicula purus in, blandit arcu.")
label2 = vtk.ui.Label(screen, text = "Testing! Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur congue, purus eget placerat vulputate, nisi justo ornare erat, ut vehicula risus ante at nunc. Pellentesque lobortis fermentum ornare. Sed elementum vestibulum velit, eu molestie dui fermentum in. Etiam at viverra lorem. Vivamus pellentesque urna ut faucibus consequat. Sed ultricies eu sapien quis ullamcorper. Vivamus et nisi interdum, vehicula purus in, blandit arcu.")
button = vtk.ui.Button(screen, text = "Hello,\nbig world!")

screen.padding = 10
screen.backgroundColour = vtk.styles.Colour_DarkBlue()

label.width = vtk.ui.Measurement(0.5, 0, screen.innerWidth)

label2.width = 30
label2.height = 20
label2.padding = 2
label2.backgroundColour = vtk.styles.Colour_Red()

button.x = 50
button.y = 20
button.backgroundColour = vtk.styles.Colour_Yellow()
button.foregroundColour = vtk.styles.Colour_Black()

screen.place()
label.place()
label.resizeToContent()
label2.place(placeDirection = vtk.ui.PLACE_DIRECTION_UNDER)
button.place(placeDirection = vtk.ui.PLACE_DIRECTION_FREE)

application.start()
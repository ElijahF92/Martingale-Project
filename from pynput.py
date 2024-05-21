from pynput.mouse import Button, Controller

mouse = Controller()

mouse.position = (50,60)
print('Current mouse position −> {0}'.format(mouse.position))
mouse.move(70,45)
print('Current mouse position −> {0}'.format(mouse.position))

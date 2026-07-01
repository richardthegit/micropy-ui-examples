from rb.core.color import hsv_to_rgb
from rb.dev.neo_led import NeoPin
from rb.ui.menu import Menu, MenuItem


colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 255, 255),
    (255, 0, 255),
    (255, 255, 0),
]

class LEDMenu(Menu):
    def __init__(self, display, btns, back):
        items = [
            MenuItem('Off'),
            MenuItem('Red'),
            MenuItem('Green'),
            MenuItem('Blue'),
            MenuItem('Cyan'),
            MenuItem('Magenta'),
            MenuItem('Yellow'),
        ]
        super().__init__(display, btns, 'LED Colors', items, back = back)

        self.led = NeoPin()
        self.led.set(colors[0])

    def selection_changed(self):
        self.led.set(colors[self.selection])

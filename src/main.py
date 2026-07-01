import asyncio, machine

from rb.core import Rebooter
from rb.core.store import store
from rb.core.wifi import Wifi
from rb.dev.display import Display
from rb.ui.menu import MenuItem, Menu
from rb.ui.nav import NavBtns

from clock_screen import ClockScreen
from led_menu import LEDMenu
from life_screen import LifeScreen
from wifi_menu import WifiMenu

wifi = Wifi()
if wifi.on():
    wifi.ntp()

display = Display()
btns = NavBtns(9, 8, 7, 6)
clock = ClockScreen(display, btns, lambda: to_top())
life = LifeScreen(display, btns, lambda: to_top())

top_menu = Menu(display, btns, None, [
    MenuItem('Scroll Test', lambda: to_sub()),
    MenuItem('Wifi', lambda: to_wifi()),
    MenuItem('Clock', lambda: to_clock()),
    MenuItem('LED Color', lambda: to_led()),
    MenuItem('Life', lambda: to_life()),
])

sub_menu = Menu(display, btns, 'Sub Menu', [
    MenuItem('Sub 1', None),
    MenuItem('Sub 2', None),
    MenuItem('Sub 3', None),
    MenuItem('Sub 4', None),
    MenuItem('Sub 5', None),
    MenuItem('Sub 6', None),
    MenuItem('Sub 7', None),
], lambda: to_top())

wifi_menu = WifiMenu(display, btns, wifi, lambda: to_top())
led_menu = LEDMenu(display, btns, lambda: to_top())

def to_top():
    top_menu.enter()

def to_sub():
    sub_menu.enter(True)

def to_clock():
    clock.enter()

def to_wifi():
    wifi_menu.enter()

def to_led():
    led_menu.enter()

def to_life():
    life.enter()

async def main():
    to_top()

    # Keep the main loop alive
    while True:
        if btns.listener == life:
            life.step()
        if btns.listener == clock:
            clock.step()

        await asyncio.sleep(0.01)

if __name__ == '__main__':
    # Run the event loop
    asyncio.run(main())

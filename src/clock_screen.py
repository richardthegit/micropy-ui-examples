import asyncio, time
from machine import Pin

from rb.core import ScreenContext
from rb.core.constants import MONTHS, DAYS
from rb.core.richtext import rt
from rb.core.tz import get_tz, local_secs

from fonts import ezFBfont_helvR08_latin_13, ezFBfont_helvB24_nums_32
from fonts.ezFBfont import ezFBfont


class ClockScreen:
    """
    Time/date display on a 128*64 screen.
    """
    def __init__(self, display, btns, back):
        self.fb = display.fb
        self.btns = btns
        self.back = back

        self.last_update = 0

        self.font_md = ezFBfont(self.fb, ezFBfont_helvR08_latin_13)
        self.font_xl = ezFBfont(self.fb, ezFBfont_helvB24_nums_32)

    def enter(self):
        self.btns.set_listener(self)

    def nav_left(self):
        self.back()

    def set_brightness(self, hour):
        """
        Dim the display at night.
        """
        if hour >= 22 or hour < 6:
            self.fb.contrast(1)
        else:
            self.fb.contrast(255)

    def layout(self):
        y = 0
        right = self.fb.width

        # Time
        year, month, day, h, m, s, weekday, yearday = time.localtime(local_secs())
        tz, offset = get_tz()
        self.set_brightness(h)

        self.font_md.write(f'{DAYS[weekday]}', 0, y)
        self.font_md.write(tz, right, 0, halign = 'right')
        y += 20

        self.font_xl.write(f'{h:02d}:{m:02d}:{s:02d}', 0, y)

        y = self.fb.height
        self.font_md.write(f'{day} {MONTHS[month - 1]}', right, y, 
                           halign = 'right', valign = 'bottom')

    def step(self):
        """
        Call this regularly - at least every second.
        """
        now = int(time.time())
        if now != self.last_update:
            with ScreenContext(self.fb):
                self.layout()
            self.last_update = now

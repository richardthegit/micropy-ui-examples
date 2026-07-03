import asyncio, time
from machine import Pin
from random import randint

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

    def time_tz(self, y, h, m, s, tz):
        right = self.fb.width
        self.font_xl.write(f'{h:02d}:{m:02d}', 0, y)
        self.font_md.write(tz, right, y, halign = 'right')
        self.font_md.write(f'{s:02d}', right, y + 13, halign = 'right')

    def day_date(self, y, weekday, day, month):
        right = self.fb.width
        self.font_md.write(f'{DAYS[weekday]}', 0, y)
        self.font_md.write(f'{day} {MONTHS[month - 1]}', right, y, halign = 'right')

    def layout(self):
        secs = local_secs()
        year, month, day, h, m, s, weekday, yearday = time.localtime(secs)
        tz, offset = get_tz()
        self.set_brightness(h)

        offset = s
        if offset >= 30:
            offset = 60 - offset

        md_h = 13
        xl_h = 30

        if offset < 15:
            offset = min(offset, 13)
            self.time_tz(offset, h, m, s, tz)
            self.day_date(self.fb.height - offset - md_h, weekday, day, month)
        else:    
            offset = min(29 - offset, 10)        
            self.time_tz(self.fb.height - offset - xl_h, h, m, s, tz)
            self.day_date(offset, weekday, day, month)

    def step(self):
        """
        Call this regularly - at least every second.
        """
        now = int(time.time())
        if now != self.last_update:
            with ScreenContext(self.fb):
                self.layout()
            self.last_update = now

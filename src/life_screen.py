from rb.core.color import hsv_to_rgb
from rb.core.store import store

from life2 import Life2


class LifeScreen:
    """
    The Game of Life on a 128*64 screen.
    """
    def __init__(self, display, btns, back):
        self.fb = display.fb
        self.btns = btns
        self.back = back

        self.life = Life2(self.fb, store.get('life_scale', 2))
        self.pixel_multiplier = 1 if self.life.scale == 2 else 4
        self.age = 0
        self.genesis()

    def enter(self):
        self.btns.set_listener(self)

    def nav_left(self):
        self.back()

    def cycle(self):
        self.life.draw()
        self.fb.show()

    def genesis(self):
        """
        Create an initial world with small lumps.
        """
        for i in range(100):
            self.life.spawn(self.pixel_multiplier)

        for i in range(100):
            self.life.radiation(self.pixel_multiplier)

    def step(self):
        alive = self.life.update()

        if alive < 1: 
            self.genesis()
        else:
            self.life.radiation(1)

        self.age += 1
        self.cycle()

import random

class Life2:
    """
    The Game of Life optimized for MicroPython on the ESP32-C3.
    """
    def __init__(self, fb, scale = 4):
        self.fb = fb
        self.w = fb.width // scale
        self.h = fb.height // scale
        self.scale = scale

        # Flattened 1D bytearrays are vastly faster than lists-of-lists
        self.grid = bytearray(self.w * self.h)
        self.working_grid = bytearray(self.w * self.h)

    def spawn(self, count = 100):
        added = 0
        total_cells = self.w * self.h
        while added < count:
            idx = random.randint(0, total_cells - 1)
            if not self.grid[idx]:
                self.grid[idx] = 1
                added += 1

    def radiation(self, events = 1):
        """
        A random 'radiation' event; this will set a cell to live but only if 
        it isn't already live, and is next to a living cell.

        Use this to peturb the fixed patterns that often establish themselves.
        """
        w, h = self.w, self.h
        grid = self.grid

        for i in range(events):
            x = random.randint(0, self.w - 1)
            y = random.randint(0, self.h - 1)
            y_curr = y * w

            if not grid[y_curr + x]:
                x_left = (x - 1 + w) % w
                x_right = (x + 1) % w
                y_up = ((y - 1 + h) % h) * w
                y_down = ((y + 1) % h) * w

                living_neighbours = (
                    grid[x_left + y_up]   + grid[x + y_up]   + grid[x_right + y_up] +
                    grid[x_left + y_curr]                    + grid[x_right + y_curr] +
                    grid[x_left + y_down] + grid[x + y_down] + grid[x_right + y_down]
                )
                if living_neighbours > 0:
                    grid[y_curr + x] = 1

    @micropython.native
    def update(self):
        """
        Update the whole grid. Returns total living cells.
        Compiled directly to machine code for speed.
        """
        w, h = self.w, self.h
        curr = self.grid
        nxt = self.working_grid
        total_alive = 0

        for y in range(h):
            # Pre-calculate Y coordinates for wrapping up and down
            y_up = ((y - 1 + h) % h) * w
            y_curr = y * w
            y_down = ((y + 1) % h) * w

            for x in range(w):
                x_left = (x - 1 + w) % w
                x_right = (x + 1) % w

                # Inline neighbor count: No function calls, pure array access
                living_neighbours = (
                    curr[x_left + y_up]   + curr[x + y_up]   + curr[x_right + y_up] +
                    curr[x_left + y_curr]                    + curr[x_right + y_curr] +
                    curr[x_left + y_down] + curr[x + y_down] + curr[x_right + y_down]
                )

                idx = x + y_curr
                cell = curr[idx]

                if cell == 1:
                    if living_neighbours <= 1 or living_neighbours >= 4:
                        nxt[idx] = 0
                    else:
                        nxt[idx] = 1
                        total_alive += 1
                else:
                    if living_neighbours == 3:
                        nxt[idx] = 1
                        total_alive += 1
                    else:
                        nxt[idx] = 0

        # Swap the buffers (atomic switch)
        self.grid, self.working_grid = nxt, curr
        return total_alive

    @micropython.native
    def draw(self):
        """
        Draw the grid in a single pass after calculations are done.
        """
        # Clear the frame buffer first
        self.fb.fill(0)
        
        w = self.w
        h = self.h
        s = self.scale
        grid = self.grid
        rect = self.fb.rect

        # Draw only active cells to minimize drawing overhead
        for y in range(h):
            y_off = y * w
            for x in range(w):
                if grid[x + y_off]:
                    rect(x * s, y * s, s, s, 1, True)

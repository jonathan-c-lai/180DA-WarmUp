from Grid import Grid
import time

DELAY_PER_FRAME = 1 # s

# initialize board
my_grid = Grid()

# keep printing grid every DELAY_PER_FRAME s for now
while (True):
    my_grid.print_grid()
    time.sleep(DELAY_PER_FRAME)

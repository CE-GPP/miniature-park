import displayio
import board
import terminalio
from adafruit_display_text import label
from adafruit_st7789 import ST7789
import time

# Set up the display
spi = board.SPI()
tft_cs = board.D8
tft_dc = board.D27
tft_rst = board.D22
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(display_bus, width=170, height=320, colstart=35, rotation=0)

# Create a display group
group = displayio.Group()
display.show(group)

# Set up the label
text_area = label.Label(
    terminalio.FONT,
    text = "Miniature\nQEOP",
    color=0xFFFF00,
    scale=3,
    anchor_point=(0.5, 0.5),
    anchored_position=(display.width // 2, display.height),
)
group.append(text_area)

# Define scrolling behavior
scroll_speed = 7  # Increase this value to scroll faster
scroll_range = display.height - text_area.bounding_box[3]

# Double buffering variables
buffer1 = displayio.Bitmap(display.width, display.height, 1)
buffer2 = displayio.Bitmap(display.width, display.height, 1)
buffer1_sprite = displayio.TileGrid(buffer1, pixel_shader=displayio.ColorConverter())
buffer2_sprite = displayio.TileGrid(buffer2, pixel_shader=displayio.ColorConverter())
buffer1_group = displayio.Group(scale=1)
buffer2_group = displayio.Group(scale=1)
buffer1_group.append(buffer1_sprite)
buffer2_group.append(buffer2_sprite)

# Add the buffer groups to the main group
group.append(buffer1_group)
group.append(buffer2_group)

# Scroll the text
move = 0
move_rate = 0.1
while True:
    move += move_rate
    if move >= scroll_range:
        move -= scroll_range
    buffer1_sprite.y = int(move)
    buffer2_sprite.y = buffer1_sprite.y - buffer2.height
    display.refresh()
    time.sleep(0.05 * scroll_speed)
    buffer1, buffer2 = buffer2, buffer1
    buffer1_sprite.bitmap = buffer1
    buffer2_sprite.bitmap = buffer2

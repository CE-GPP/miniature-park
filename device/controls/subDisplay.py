# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import board
import terminalio
import displayio
import time
from adafruit_display_text import label
from adafruit_st7789 import ST7789

BORDER_WIDTH = 20
VERTICAL_BORDER_HEIGHT = 4
TEXT_SCALE = 3

text= ['Wind', 'Temp', 'Bicycle', 'Shadow']


def drawBoxes(items):
    items.append('Finish')
    itemNumber = len(items)
    boxHeight = int((display.height / itemNumber) - 5)
    elements = []
    print(boxHeight)
    for index, item in enumerate(items):
        # Boxes
        inner_bitmap = displayio.Bitmap(
            display.width - (BORDER_WIDTH * 2), boxHeight, index+1
        )
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0xFFB30F if index == itemNumber -1 else 0x01295F
        yCoord = ((index * boxHeight) + (0 if index == 0 else 5*index))
        inner_sprite = displayio.TileGrid(
            inner_bitmap, pixel_shader=inner_palette, x=BORDER_WIDTH, y=yCoord+(VERTICAL_BORDER_HEIGHT)
        )
        elements.append(inner_sprite)

        #Texts
        text_area = label.Label(
            terminalio.FONT,
            text = item,
            color=0xFFFF00,
            scale=TEXT_SCALE,
            anchor_point=(0.5, 0.5),
            anchored_position=(display.width // 2, yCoord + (boxHeight/2)),
        )
        elements.append(text_area)

    return elements

def focusBox(items, focusIndex):
    itemNumber = len(items) + 1
    boxHeight = int((display.height / itemNumber) - 5)
    yCoords = []

    for index, item in enumerate(items):
        yCoord = ((index * boxHeight) + (0 + VERTICAL_BORDER_HEIGHT if index == 0 else 5*index))
        yCoords.append(yCoord)
    inner_bitmap = displayio.Bitmap(
            display.width - (BORDER_WIDTH * 2) + VERTICAL_BORDER_HEIGHT, boxHeight+ VERTICAL_BORDER_HEIGHT, 1
        )
    print(boxHeight)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0xFD151B
    inner_sprite = displayio.TileGrid(
            inner_bitmap, pixel_shader=inner_palette, x=BORDER_WIDTH - (VERTICAL_BORDER_HEIGHT/2), y= yCoords[focusIndex] - (VERTICAL_BORDER_HEIGHT / 2)
        )
    return inner_sprite

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D8
tft_dc = board.D27
tft_rst = board.D22

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)

display = ST7789(display_bus, width=170, height=320, colstart=35, rotation=0)

# Make the display context
menu = displayio.Group()
display.show(menu)

menu.append(focusBox(text, 1))
# Draw a smaller inner rectangle
for box in drawBoxes(text):
    menu.append(box)




while True:
    # for i in range(5):
    #     menu.pop(0)
    #     menu.insert(0,focusBox(text, i) )
    #     time.sleep(1)
    pass

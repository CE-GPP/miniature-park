# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import sys
sys.path.append('/home/DYpi/QEOP/utils')
import board
import terminalio
import displayio
import time
import RPi.GPIO as GPIO
import json
import paho.mqtt.client as mqtt
import utils as utils
from adafruit_display_text import label
from adafruit_st7789 import ST7789

BORDER_WIDTH = 20
VERTICAL_BORDER_HEIGHT = 4
TEXT_SCALE = 3
FOCUS = 0
NORMAL_COLOUR = 0x01295F
SELECTED_COLOUR = 0x437F97
FINISH_COLOUR = 0xFFB30F
SECRETE_ADDRESS = 'QEOP/secrete.txt'

encoderPinA = 23
encoderPinB = 24
buttonPin = 25

encoderValue = 0
previousValue = 0
lastEncoded = 0

spi = board.SPI()
tft_cs = board.D8
tft_rst = board.D5
tft_dc = board.D6

text= ['Wind', 'Temp', 'Bicycle', 'Shadow']
selectedLayers = {key: False for key in text}
text.append('Finish')

def drawBoxes(items, topOffset = 0):
    itemNumber = len(items)
    boxHeight = int(((display.height - topOffset) / itemNumber) - 5)
    elements = []
    for index, item in enumerate(items):
        # Boxes
        inner_bitmap = displayio.Bitmap(
            display.width - (BORDER_WIDTH * 2), boxHeight, index+1
        )
        inner_palette = displayio.Palette(1)
        inner_palette[0] = FINISH_COLOUR if index == itemNumber -1 else NORMAL_COLOUR
        yCoord = topOffset + ((index * boxHeight) + (0 if index == 0 else 5*index))
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

def focusBox(items, focusIndex, topOffset = 0):
    itemNumber = len(items)
    boxHeight = int(((display.height - topOffset) / itemNumber) - 5)
    yCoords = []

    for index, item in enumerate(items):
        yCoord = ((index * boxHeight) + (0 + VERTICAL_BORDER_HEIGHT if index == 0 else 5*index))
        yCoords.append(yCoord)
    inner_bitmap = displayio.Bitmap(
            display.width - (BORDER_WIDTH * 2) + VERTICAL_BORDER_HEIGHT, boxHeight+ VERTICAL_BORDER_HEIGHT, 1
        )
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0xFD151B
    inner_sprite = displayio.TileGrid(
            inner_bitmap, 
            pixel_shader=inner_palette, 
            x=BORDER_WIDTH - (VERTICAL_BORDER_HEIGHT/2), 
            y= yCoords[focusIndex] - (VERTICAL_BORDER_HEIGHT / 2) if focusIndex == 0 else yCoords[focusIndex] + (VERTICAL_BORDER_HEIGHT/2)
        )
    return inner_sprite

def moveFocus(direction):
    global FOCUS
    itemNumber = len(text)
    if direction == True:
        FOCUS = FOCUS + 1 if FOCUS + 1 < itemNumber else 0
    else:
        FOCUS = itemNumber - 1 if FOCUS - 1 < 0 else FOCUS - 1

def read_encoder_value():
    global encoderValue, previousValue
    value = encoderValue // 4
    change = (value - previousValue)
    if change > 0:
        moveFocus(True)
    elif change < 0:
        moveFocus(False)
    previousValue = value
    return value

def update_encoder(channel):
    global encoderValue, lastEncoded
    MSB = GPIO.input(encoderPinA)
    LSB = GPIO.input(encoderPinB)

    encoded = (MSB << 1) | LSB
    sum = (lastEncoded << 2) | encoded

    if sum == 0b1101 or sum == 0b0100 or sum == 0b0010 or sum == 0b1011:
        encoderValue += 1
    if sum == 0b1110 or sum == 0b0111 or sum == 0b0001 or sum == 0b1000:
        encoderValue -= 1

    lastEncoded = encoded

def is_button_push_down():
    if not GPIO.input(buttonPin):
        time.sleep(0.005)
        if not GPIO.input(buttonPin):
            return True
    return False

# Release any resources currently in use for the displays
displayio.release_displays()

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)

display = ST7789(display_bus, width=170, height=320, colstart=35, rotation=0)

# Make the display context
menu = displayio.Group()
display.show(menu)

menu.append(focusBox(text, 0))
# Draw a smaller inner rectangle
for box in drawBoxes(text):
    menu.append(box)


try:
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(encoderPinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(encoderPinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(encoderPinA, GPIO.BOTH, callback=update_encoder)
    GPIO.add_event_detect(encoderPinB, GPIO.BOTH, callback=update_encoder)
except:
    GPIO.cleanup()
    print("Set Up Connection Failed.")


while True:
    value = read_encoder_value()
    menu[0] = focusBox(text, FOCUS)
    if is_button_push_down():
        print("Focus is {}".format(FOCUS))
        print(text[FOCUS])
        boxIndex = (FOCUS * 2) + 1
        if FOCUS == len(text)-1:
            json_str = json.dumps(selectedLayers)
            with open(SECRETE_ADDRESS, "r") as f:
                utils.publishMQTT('mqtt.cetools.org',
                                 1884,
                                 'student',
                                 f.read().strip(),
                                 "student/ucfnimx/QEOPMap/json",
                                 json_str
                                 )
            display_bus.reset()
            break
        elif selectedLayers[text[FOCUS]] == True:
            selectedLayers[text[FOCUS]] = False
            menu._layers[boxIndex].pixel_shader._colors[0]['rgba'] = utils.hexToRGBA(NORMAL_COLOUR)
        else:
            selectedLayers[text[FOCUS]] = True
            menu._layers[boxIndex].pixel_shader._colors[0]['rgba'] = utils.hexToRGBA(SELECTED_COLOUR)
    print(selectedLayers)

    time.sleep(0.1)
    pass

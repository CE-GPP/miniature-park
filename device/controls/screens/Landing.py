import sys
sys.path.append('/home/DYpi/QEOP/utils')
import time
import RPi.GPIO as GPIO
import json
import utils as utils
import ui as ui
import colors as colors

FOCUS = 0

encoderPinA = 23
encoderPinB = 24
buttonPin = 25
encoderValue = 0
previousValue = 0
lastEncoded = 0
topOffset = 80

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

def moveFocus(direction, layers):
    global FOCUS
    itemNumber = len(layers)
    if direction == True:
        FOCUS = FOCUS + 1 if FOCUS + 1 < itemNumber else 0
    else:
        FOCUS = itemNumber - 1 if FOCUS - 1 < 0 else FOCUS - 1

def read_encoder_value(layers):
    global encoderValue, previousValue
    value = encoderValue // 4
    change = (value - previousValue)
    if change > 0:
        moveFocus(True, layers)
    elif change < 0:
        moveFocus(False, layers)
    previousValue = value
    return value

def is_button_push_down():
    if not GPIO.input(buttonPin):
        time.sleep(0.05)
        if not GPIO.input(buttonPin):
            return True
    return False

class LandingScreen:
    def __init__(self, display, diaply_io, layers):
        self.display = display
        self.displayio = diaply_io
        self.layers = layers
        self.colour = colors.Colors()


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

    def runScreen(self):
        global FOCUS
        uiGen = ui.Generator(self.display, self.displayio)
        menu = self.displayio.Group()

        self.display.show(menu)
        menu.append(uiGen.addText("QEOP", (self.display.width//2, topOffset//2), scale = 4))
        menu.append(uiGen.focusBox(self.layers, 0, topOffset = topOffset))
        # Draw a smaller inner rectangle
        for box in uiGen.drawBoxes(self.layers,topOffset):
            menu.append(box)
        
        while True:
            value = read_encoder_value(self.layers)
            menu[1] = uiGen.focusBox(self.layers, FOCUS, topOffset)
            if is_button_push_down():
                GPIO.remove_event_detect(encoderPinA)
                GPIO.remove_event_detect(encoderPinB)
                return FOCUS
            time.sleep(0.1)
            pass
import sys
sys.path.append('/home/DYpi/QEOP/utils')
import time
import RPi.GPIO as GPIO
import json
import utils as utils
import ui as ui
import colors as colors

FOCUS = 0
SECRETE_ADDRESS = 'QEOP/secrete.txt'

encoderPinA = 23
encoderPinB = 24
buttonPin = 25

encoderValue = 0
previousValue = 0
lastEncoded = 0


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
        time.sleep(0.005)
        if not GPIO.input(buttonPin):
            return True
    return False

class SelectLayers:
    def __init__(self, display, diaply_io, layers):
        self.display = display
        self.displayio = diaply_io
        self.menu = self.displayio.Group()
        self.layers = layers
        self.colour = colors.Colors()
        self.selectedLayers = {key: False for key in self.layers}

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
        FOCUS = 1
        self.uiGen = ui.Generator(self.display, self.displayio)

        self.display.show(self.menu)
        self.menu.append(self.uiGen.focusBox(self.layers, 0))
        # Draw a smaller inner rectangle
        for box in self.uiGen.drawBoxes(self.layers):
            self.menu.append(box)

        while True:
            value = read_encoder_value(self.layers)
            self.menu[0] = self.uiGen.focusBox(self.layers, FOCUS)
            if is_button_push_down():
                # print("Focus is {}".format(FOCUS))
                # print(self.layers[FOCUS])
                boxIndex = (FOCUS * 2) + 1
                if FOCUS == len(self.layers)-1:
                    json_str = json.dumps(self.selectedLayers)
                    with open(SECRETE_ADDRESS, "r") as f:
                        result = utils.publishMQTT('mqtt.cetools.org',
                                        1884,
                                        'student',
                                        f.read().strip(),
                                        "student/ucfnimx/QEOPMap/json",
                                        json_str
                                        )
                    GPIO.remove_event_detect(encoderPinA)
                    GPIO.remove_event_detect(encoderPinB)
                    return result.is_published()
                elif self.selectedLayers[self.layers[FOCUS]] == True:
                    self.selectedLayers[self.layers[FOCUS]] = False
                    self.menu._layers[boxIndex].pixel_shader._colors[0]['rgba'] = utils.hexToRGBA(self.colour.NORMAL_COLOUR)
                else:
                    self.selectedLayers[self.layers[FOCUS]] = True
                    self.menu._layers[boxIndex].pixel_shader._colors[0]['rgba'] = utils.hexToRGBA(self.colour.SELECTED_COLOUR)
            # print(self.selectedLayers)

            time.sleep(0.1)
            pass

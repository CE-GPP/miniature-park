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
    debounce_time = 50  # set the debounce time in milliseconds
    if not GPIO.input(buttonPin):
        time.sleep(debounce_time/1000.0)  # wait for the debounce time
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
        layersDict = self.layers
        displayLayer = list(layersDict.keys())
        valueLayer = list(layersDict.values())

        displayLayer.append('Finish')
        
        selectedLayers = {layers: False for layers in displayLayer}

        self.uiGen = ui.Generator(self.display, self.displayio)

        self.display.show(self.menu)
        
        self.menu.append(self.uiGen.focusBox(displayLayer, 0))
        # Draw a smaller inner rectangle
        for box in self.uiGen.drawBoxes(displayLayer):
            self.menu.append(box)

        while True:
            value = read_encoder_value(displayLayer)
            self.menu[0] = self.uiGen.focusBox(displayLayer, FOCUS)
            if is_button_push_down():
                boxIndex = (FOCUS * 2) + 1
                if FOCUS == len(displayLayer) - 1:
                    selectedLayers.popitem()
                    selectedLayers = {valueLayer[i]: list(selectedLayers.values())[i] for i in range(len(selectedLayers))}
                    json_str = json.dumps(selectedLayers)
                    with open(SECRETE_ADDRESS, "r") as f:
                        result = utils.publishMQTT('mqtt.cetools.org',
                                        1884,
                                        'student',
                                        f.read().strip(),
                                        "student/ucfnimx/QEOPMap/layer",
                                        json_str
                                        )
                    GPIO.remove_event_detect(encoderPinA)
                    GPIO.remove_event_detect(encoderPinB)
                    print(json_str)
                    return result.is_published()
                elif selectedLayers[displayLayer[FOCUS]] == True:
                    selectedLayers[displayLayer[FOCUS]] = False
                    self.menu._layers[boxIndex].pixel_shader._colors[0]['rgba'] = utils.hexToRGBA(self.colour.NORMAL_COLOUR)
                else:
                    selectedLayers[displayLayer[FOCUS]] = True
                    self.menu._layers[boxIndex].pixel_shader._colors[0]['rgba'] = utils.hexToRGBA(self.colour.SELECTED_COLOUR)

            time.sleep(0.1)
            pass

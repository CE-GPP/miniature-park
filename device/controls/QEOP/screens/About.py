import sys
sys.path.append('/home/DYpi/QEOP/utils')
import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_st7789 import ST7789
import ui as ui
import time
import textwrap
import RPi.GPIO as GPIO


buttonPin = 25

def is_button_push_down():
    if not GPIO.input(buttonPin):
        time.sleep(0.005)
        if not GPIO.input(buttonPin):
            return True
    return False

class AboutScreen:
    def __init__(self, display, diaply_io):
        self.display = display
        self.displayio = diaply_io
    
    def runScreen(self):
        display = self.display
        
        # Create a display group
        group = displayio.Group()
        display.show(group)


        # Set up the label
        text = "Miniature QEOP        We are creating a device that can visualise vital real-time data on a miniature version of the Olympic Park in London."
        wrapped_text = textwrap.wrap(text, width=display.width // (terminalio.FONT.get_bounding_box()[0] * 3))
        wrapped_text = "\n".join(wrapped_text)
        text = wrapped_text

        text_height = []

        text_lines = text.splitlines()
        text_scale = 3
        text_height.append(len(text_lines) * terminalio.FONT.get_bounding_box()[1] * text_scale)

        # Set up the label
        overviewText = label.Label(
            terminalio.FONT,
            text = text,
            color=0xFFFF00,
            scale=text_scale,
            anchor_point=(0.5, 0),
            anchored_position=(display.width // 2, display.height),
        )

        group.append(overviewText)

        text = "Miniature\nQEOP\n\nDY\nLim\n\nJingqi\nCheng\n\nPatrick\nWhyte\n\nYining\nAN"
        text_lines = text.splitlines()
        text_scale = 3
        text_height.append(len(text_lines) * terminalio.FONT.get_bounding_box()[1] * text_scale)

        # Set up the label
        projectText = label.Label(
            terminalio.FONT,
            text = text,
            color=0xFFFF00,
            scale=text_scale,
            anchor_point=(0.5, 0),
            anchored_position=(display.width // 2, display.height),
        )

        group.append(projectText)


        for index, text in enumerate(group):
            # Define scrolling behavior
            if index == 1:
                group.pop(0)
            scroll_speed = 0.5
            scroll_range = text_height[index] * 1.5

            # Scroll the text
            move = 0
            moveRate = 1
            while True:
                move = move + moveRate
                if move >= scroll_range:
                    break
                text.y = text.y - moveRate
                display.refresh()
                time.sleep(0.05 * scroll_speed)
                if is_button_push_down():
                    break


import terminalio
from adafruit_display_text import label

class Generator:
    def __init__(self, display, displayio):
        self.display = display
        self.displayio = displayio
        self.NORMAL_COLOUR = 0x01295F
        self.SELECTED_COLOUR = 0x437F97
        self.FINISH_COLOUR = 0xFFB30F

    def addText(self, text,position,scale = 3,anchor_point=(0.5, 0.5)):
        text_area = label.Label(
            terminalio.FONT,
            text = text,
            color=0xFFFF00,
            scale=scale,
            anchor_point=anchor_point,
            anchored_position=position,
        )
        return text_area
    
    def drawBoxes(self, items, topOffset = 0, BORDER_WIDTH = 20, VERTICAL_BORDER_HEIGHT=4, TEXT_SCALE=3) :
        itemNumber = len(items)
        boxHeight = int(((self.display.height - topOffset) / itemNumber) - 5)
        elements = []
        for index, item in enumerate(items):
            # Boxes
            inner_bitmap = self.displayio.Bitmap(
                self.display.width - (BORDER_WIDTH * 2), boxHeight, index+1
            )
            inner_palette = self.displayio.Palette(1)
            inner_palette[0] = self.FINISH_COLOUR if index == itemNumber -1 else self.NORMAL_COLOUR
            yCoord = topOffset + ((index * boxHeight) + (0 if index == 0 else 5*index))
            inner_sprite = self.displayio.TileGrid(
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
                anchored_position=(self.display.width // 2, yCoord + (boxHeight/2)),
            )
            elements.append(text_area)
        return elements

    def focusBox(self, items, focusIndex, topOffset = 0, BORDER_WIDTH = 20, VERTICAL_BORDER_HEIGHT=4):
        itemNumber = len(items)
        boxHeight = int(((self.display.height - topOffset) / itemNumber) - 5)
        yCoords = []

        for index, item in enumerate(items):
            yCoord = topOffset + ((index * boxHeight) + (0 + VERTICAL_BORDER_HEIGHT if index == 0 else 5*index))
            yCoords.append(yCoord)
        inner_bitmap = self.displayio.Bitmap(
                self.display.width - (BORDER_WIDTH * 2) + VERTICAL_BORDER_HEIGHT, boxHeight+ VERTICAL_BORDER_HEIGHT, 1
            )
        inner_palette = self.displayio.Palette(1)
        inner_palette[0] = 0xFD151B
        inner_sprite = self.displayio.TileGrid(
                inner_bitmap, 
                pixel_shader=inner_palette, 
                x=BORDER_WIDTH - (VERTICAL_BORDER_HEIGHT/2), 
                y= yCoords[focusIndex] - (VERTICAL_BORDER_HEIGHT / 2) if focusIndex == 0 else yCoords[focusIndex] + (VERTICAL_BORDER_HEIGHT/2)
            )
        return inner_sprite
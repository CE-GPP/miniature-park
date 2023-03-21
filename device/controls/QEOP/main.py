import sys
sys.path.append('/home/DYpi/QEOP/screens')
sys.path.append('/home/DYpi/QEOP/utils')
import board
import displayio
import utils as utils
import SelectLayers as SelectLayers
import SelectStyle as SelectStyle
import Landing as Landing
import About as About
from adafruit_st7789 import ST7789

spi = board.SPI()
tft_cs = board.D8
tft_rst = board.D5
tft_dc = board.D6

baseLayers = {'Satellite' : 'Satellite', 
              'GreyCanvas' : 'Grey'
              }
overLayers= {
    'Weather' : 'weather', 
    'Network':'heatmapLayer', 
    '3D':'osmb', 
    'Shadow':'shadeMap', 
    'Bycycle':'markerLayer',
    'Wind':"Wind"
    }

menu = ['Layers','Style','About']

# Release any resources currently in use for the displays
displayio.release_displays()
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(display_bus, width=170, height=320, colstart=35, rotation=0, brightness = 1, backlight_pin = board.D13)


while True:
    landingPage = Landing.LandingScreen(display, displayio, menu)
    menuIndex = landingPage.runScreen()
    if menuIndex == 0:
        selectLayersScreen = SelectLayers.SelectLayers(display, displayio, overLayers)
        print(selectLayersScreen.runScreen())
    elif menuIndex == 1:
        selectStyleScreen = SelectStyle.SelectStyle(display, displayio, baseLayers)
        print(selectStyleScreen.runScreen())
    elif menuIndex == 2:
        aboutScreen = About.AboutScreen(display, displayio)
        aboutScreen.runScreen()
    else:
        print(menuIndex)
# selectLayersScreen = SelectLayers.SelectLayers(display, displayio, layers)
# print(selectLayersScreen.runScreen())

# display_bus.reset()

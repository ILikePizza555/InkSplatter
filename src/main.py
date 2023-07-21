from led import NETWORK_LED, WARN_LED
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY 

import gc
import logging
import time
import sys
import useful

def boot():
    # A short delay to give USB chance to initialise
    time.sleep(0.5)

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("1.log")
    ])

    # Setup for the display.
    graphics = PicoGraphics(DISPLAY)
    WIDTH, HEIGHT = graphics.get_bounds()
    graphics.set_font("bitmap8")

    # Reset LEDs
    NETWORK_LED.stop()
    WARN_LED.stop()
    useful.clear_button_leds()

boot()
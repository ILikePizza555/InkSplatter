from led import NETWORK_LED, WARN_LED
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY 

import gc
import logging
import time
import sys
import useful

data = None

def boot():
    # A short delay to give USB chance to initialise
    time.sleep(0.5)

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    # Setup for the display.
    graphics = PicoGraphics(DISPLAY)
    WIDTH, HEIGHT = graphics.get_bounds()
    graphics.set_font("bitmap8")

    # Reset LEDs
    NETWORK_LED.stop()
    WARN_LED.stop()
    useful.clear_button_leds()

    global data
    data = useful.load_json()

    if "wlan" in data:
        useful.select_network(data["wlan"])

    logging.info("Initialized")

boot()
from led import NETWORK_LED, WARN_LED
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY 

import gc
import logging
import time
import sys
import useful
import wlan

# Length of time between updates in minutes.
# Frequent updates will reduce battery life!
UPDATE_INTERVAL = 240

data = None

def setup_display():
    # Setup for the display.
    graphics = PicoGraphics(DISPLAY)
    WIDTH, HEIGHT = graphics.get_bounds()
    graphics.set_font("bitmap8")
    return graphics, WIDTH, HEIGHT

def boot():
    # A short delay to give USB chance to initialise
    time.sleep(0.5)

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format="%(msecs)d:%(levelname)s - %(message)s")
    logging.debug("Mem alloc: %d. Mem free: %d", gc.mem_alloc(), gc.mem_free())

    # Reset LEDs
    NETWORK_LED.stop()
    WARN_LED.stop()
    useful.clear_button_leds()

    global data
    data = useful.load_json()

    if "wlan" in data:
        wlan.find_and_connect_network(data["wlan"])

    logging.debug("Mem alloc: %d. Mem free: %d", gc.mem_alloc(), gc.mem_free())
    gc.collect()
    logging.debug("Mem alloc: %d. Mem free: %d", gc.mem_alloc(), gc.mem_free())

def app(api_url: str):
    global UPDATE_INTERVAL
    logging.info("Starting app")
    api_response = useful.load_json_from_url(api_url)
    logging.debug("Mem alloc: %d. Mem free: %d", gc.mem_alloc(), gc.mem_free())
    img_url = api_response["url"]
    title = api_response["title"]
    logging.info("Downloading image titled \"%s\" from %s", title, img_url)
    

boot()
app(data["api_url"])
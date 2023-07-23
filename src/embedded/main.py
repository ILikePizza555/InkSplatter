from led import NETWORK_LED, WARN_LED
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY 

import gc
import logging
import time
import sys
import useful
import wlan
import jpegdec

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
    useful.log_mem_stats()

    # Reset LEDs
    NETWORK_LED.stop()
    WARN_LED.stop()
    useful.clear_button_leds()

    global data
    data = useful.load_json()

    if "wlan" in data:
        wlan.find_and_connect_network(data["wlan"])

    useful.collect_and_log_mem_stats()

def app(api_url: str):
    global UPDATE_INTERVAL
    logging.info("Starting app")
    api_response = useful.load_json_from_url(api_url)
    useful.log_mem_stats()

    img_url = api_response["url"]
    title = api_response["title"]

    useful.save_image_from_url(img_url, "images/image.jpg")
    useful.collect_and_log_mem_stats()

    logging.debug("Beginning draw")
    graphics, WIDTH, HEIGHT = setup_display()
    jpeg = jpegdec.JPEG(graphics)
    useful.collect_and_log_mem_stats()

    graphics.set_pen(1)
    graphics.clear()

    jpeg.open_file("images/image.jpg")
    jpeg.decode()

    graphics.set_pen(0)
    graphics.rectangle(0, HEIGHT - 25, WIDTH, 25)
    graphics.set_pen(1)
    graphics.text(title, 5, HEIGHT - 20, WIDTH, 2)

    useful.collect_and_log_mem_stats()

    graphics.update()
    graphics.info("Done")
    

boot()
app(data["api_url"])
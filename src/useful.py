from binascii import hexlify
from machine import Pin, PWM
from pimoroni_i2c import PimoroniI2C
from pcf85063a import PCF85063A
import mrequests as requests

import gc
import inky_frame
import json
import logging
import network
import time

HOLD_VSYS_EN_PIN = 2

I2C_SDA_PIN = 4
I2C_SCL_PIN = 5

# Pin setup for VSYS_HOLD needed to sleep and wake.
hold_vsys_en_pin = None
if hold_vsys_en_pin is None:
    hold_vsys_en_pin = Pin(HOLD_VSYS_EN_PIN, Pin.OUT)

# intialise the pcf85063a real time clock chip
real_time_chip = None

def setup_real_time_chip():
    global real_time_chip
    if real_time_chip is None:
        i2c = PimoroniI2C(I2C_SDA_PIN, I2C_SCL_PIN, 100000)
        real_time_chip = PCF85063A(i2c)

setup_real_time_chip()

# Turns off the button LEDs
def clear_button_leds():
    inky_frame.button_a.led_off()
    inky_frame.button_b.led_off()
    inky_frame.button_c.led_off()
    inky_frame.button_d.led_off()
    inky_frame.button_e.led_off()


def load_json(file = "/data.json"):
    try:
        logging.debug("Loading data from %s. Mem alloc: %d. Mem free: %d", file, gc.mem_alloc(), gc.mem_free())
        with open(file) as f:
            data = json.loads(f.read())
    
        if type(data) is dict:
            logging.debug("Successfully loaded data. Mem alloc: %d. Mem free: %d", gc.mem_alloc(), gc.mem_free())
            return data
        else:
            logging.error("Couldn't load data.json due to invalid type.")
    except OSError as e:
        logging.error("Couldn't load data.json: %s", e)
        return


def load_json_from_url(url):
    try:
        logging.debug("Loading url %s", url)
        response = requests.get(url, headers = {"Accept": "application/json"})
        return response.json()
    except Exception as e:
        logging.error("Error getting url: %s", e)
    finally:
        if response is not None:
            response.close()
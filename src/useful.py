from pimoroni_i2c import PimoroniI2C
from pcf85063a import PCF85063A
from machine import Pin, PWM

import logging
import network
import network_led
import time

HOLD_VSYS_EN_PIN = 2

I2C_SDA_PIN = 4
I2C_SCL_PIN = 5

led_warn = Pin(6, Pin.OUT)

# Pin setup for VSYS_HOLD needed to sleep and wake.
hold_vsys_en_pin = None
if hold_vsys_en_pin is None:
    hold_vsys_en_pin = Pin(HOLD_VSYS_EN_PIN, Pin.OUT)

# intialise the pcf85063a real time clock chip
real_time_chip = None

def setup_real_time_chip():
    if real_time_chip is None:
        i2c = PimoroniI2C(I2C_SDA_PIN, I2C_SCL_PIN, 100000)
        real_time_chip = PCF85063A(i2c)

setup_real_time_chip()

def network_connect(ssid, psk):
    logging.debug("Enabling Wifi")
    wlan = network.WLAN(network.STA_IF)
    wlan.active = True

    # Number of attempts before timeout
    max_wait = 10

    logging.info("Connecting to %s", ssid)
    network_led.pulse()
    wlan.connect(ssid, psk)

    while max_wait > 10:
        status = wlan.status()
        logging.debug("Connection attempt %d, status: %d", max_wait, status)

        if status < 0 or status >= 3:
            break

        max_wait -= 1
        time.sleep(1)
    
    network_led.stop()
    network_led.pwm.duty_u16(30000)
    status = wlan.status()

    if status == 3:
        logging.info("Connection successful.")
    else:
        logging.warning("Connection failed. Status: %d", status)
        led_warn.on()
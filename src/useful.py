from pimoroni_i2c import PimoroniI2C
from pcf85063a import PCF85063A
from machine import Pin, PWM

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
    if real_time_chip is None:
        i2c = PimoroniI2C(I2C_SDA_PIN, I2C_SCL_PIN, 100000)
        real_time_chip = PCF85063A(i2c)

setup_real_time_chip()
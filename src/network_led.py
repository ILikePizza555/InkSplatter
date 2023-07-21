import math
import time

from machine import Pin, PWM, Timer

NETWORK_LED_PIN = 7

pwm = PWM(Pin(7), freq=1000, duty_u16=0)
timer = Timer(-1)
pulse_speed_hz = 2

def _timer_callback(t):
    # updates the network led brightness based on a sinusoid seeded by the current time
    brightness = (math.sin(time.ticks_ms() * math.pi * 2 / (1000 / pulse_speed_hz)) * 40) + 60
    value = int(pow(brightness / 100.0, 2.8) * 65535.0 + 0.5)
    pwm.duty_u16(value)

def set_brightness(brightness):
    brightness = max(0, min(100, brightness))  # clamp to range
    # gamma correct the brightness (gamma 2.8)
    value = int(pow(brightness / 100.0, 2.8) * 65535.0 + 0.5)
    pwm.duty_u16(value)

def pulse(speed_hz):
    global pulse_speed_hz
    pulse_speed_hz = speed_hz
    timer.deinit()
    timer.init(period=50, mode=Timer.PERIODIC, callback=_timer_callback)

def stop():
    timer.deinit()
    pwm.duty_u16(0)
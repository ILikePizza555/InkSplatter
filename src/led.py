import math
import time

from machine import Pin, PWM, Timer

WARN_LED_PIN = 6
NETWORK_LED_PIN = 7

class BaseLED:
    def __init__(self, pin: Pin, pulse_speed_hz: int, **pwm_args) -> None:
        self.pwm = PWM(pin, **pwm_args)
        self.pulse_speed_hz = pulse_speed_hz
        self.pulse_timer = Timer(-1)

    def get_brightness(self):
        return self.pwm.duty_u16()
    
    def set_brightness(self, brightness: int):
        brightness = max(0, min(100, brightness))
        # gamma correct the brightness (gamma 2.8)
        value = int(pow(brightness / 100.0, 2.8) * 65535.0 + 0.5)
        self.pwm.duty_u16(value)

    brightness = property(get_brightness, set_brightness)

    def _timer_callback(self, t):
        # updates the network led brightness based on a sinusoid seeded by the current time
        self.brightness = (math.sin(time.ticks_ms() * math.pi * 2 / (1000 / self.pulse_speed_hz)) * 40) + 60
    
    def pulse(self, pulse_speed = None):
        if pulse_speed is not None:
            self.pulse_speed_hz = pulse_speed

        self.pulse_timer.deinit()
        self.pulse_timer.init(period=50, mode=Timer.PERIODIC, callback=self._timer_callback)

    def stop(self):
        self.pulse_timer.deinit()
        self.pwm.duty_u16(0)

WARN_LED =  BaseLED(Pin(WARN_LED_PIN), pulse_speed_hz=1, freq=1000, duty_u16=0)
NETWORK_LED = BaseLED(Pin(NETWORK_LED_PIN), pulse_speed_hz=2, freq=1000, duty_u16=0)
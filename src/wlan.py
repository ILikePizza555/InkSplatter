from binascii import hexlify
from collections import namedtuple
from led import NETWORK_LED, WARN_LED
from network import WLAN, STAT_IDLE, STAT_GOT_IP, STA_IF

import logging
import time

class WLANNetwork(namedtuple("WLANNetwork", ("ssid", "bssid", "channel", "RSSI", "security", "hidden"))):
    @property
    def ssid_str(self):
        return self.ssid.decode("ascii")

    @property
    def bssid_str(self):
        return hexlify(self.bssid)
    
def connect_network(wlan: WLAN, ssid, psk, max_wait = 10):
    logging.info("Connecting to %s", ssid)
    NETWORK_LED.pulse()
    wlan.connect(ssid, psk)

    while max_wait > 10:
        status = wlan.status()
        logging.debug("Connection attempt %d, status: %d", max_wait, status)

        if status < STAT_IDLE or status >= STAT_GOT_IP:
            break

        max_wait -= 1
        time.sleep(1)
    
    NETWORK_LED.stop()
    NETWORK_LED.pwm.duty_u16(30000)
    status = wlan.status()

    if status == STAT_GOT_IP:
        logging.info("Successfully connected to network %s", ssid)
        return True
    else:
        logging.warning("Failed to connect to network %s. Status: %d", ssid, status)
        WARN_LED.on()
        return False


def network_scan(wlan: WLAN):
    logging.info("Scanning for networks...")
    return [WLANNetwork(*n) for n in wlan.scan()]


def find_and_connect_network(wlan_data: dict):
    logging.debug("Enabling Wifi")
    wlan = WLAN(STA_IF)
    wlan.active(True)

    network_list = network_scan(wlan)
    logging.debug("Found networks %s", network_list)

    for n in network_list:
        if n.ssid_str in wlan_data:
            logging.info("Found known network %s. Attempting to connect.", n.ssid_str)
            success = connect_network(wlan, n.ssid, wlan_data[n.ssid_str])
            
            if success:
                return success
    
    return False
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
    wlan.connect(ssid, psk)

    for attempt in range(max_wait):
        status = wlan.status()
        logging.debug("Connection attempt %d, status: %d", attempt, status)
        if status < STAT_IDLE or status >= STAT_GOT_IP:
            break

        time.sleep(1)

    status = wlan.status()

    if status == STAT_GOT_IP:
        logging.info("Successfully connected to network %s", ssid)
        return True
    else:
        logging.warning("Failed to connect to network %s. Status: %d", ssid, status)
        return False


def network_scan(wlan: WLAN):
    logging.info("Scanning for networks...")
    return [WLANNetwork(*n) for n in wlan.scan()]


def find_and_connect_network(wlan_data: dict, max_scan_attempts = 10):
    logging.debug("Enabling Wifi")
    NETWORK_LED.pulse()
    wlan = WLAN(STA_IF)
    wlan.active(True)

    scanned_networks = {}
    for scan_attempt in range(max_scan_attempts):
        logging.debug("WLAN network scan attempt %d", scan_attempt)

        scanned_networks |= {n.ssid_str: n for n in network_scan(wlan)}
        logging.debug("Found networks %s", scanned_networks)

        for ssid, psk in wlan_data.items():
            if ssid in scanned_networks:
                logging.info("Found known network %s. Attempting to connect.", ssid)
                success = connect_network(wlan, ssid, psk)
            
                if success:
                    NETWORK_LED.stop()
                    NETWORK_LED.pwm.duty_u16(30000)
                    return success
        
        time.sleep(1) 
    
    NETWORK_LED.stop()
    NETWORK_LED.pwm.duty_u16(30000)
    WARN_LED.set_brightness(100)
    return False
# Weather sensor

The weather sensor provides a HTTP endpoint to read NAVTEX and BME680 sensor data.

`http://esp32-weather` 

After reset main.py:
- connects to WIFI
- checks if the BME680 sensor is present
- enters the main loop

The main loop can be exited by a short (jumper) between P15 and GND.

Sensors:
- [BME680](https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme680/) 
  sensor measuring relative humidity, barometric pressure, ambient temperature and gas over
  [I2C](https://docs.micropython.org/en/latest/esp32/quickref.html#hardware-i2c-bus)
- [NAVTEX](https://en.wikipedia.org/wiki/NAVTEX) messages over 
  [UART](https://docs.micropython.org/en/latest/esp32/quickref.html#uart-serial-bus)
  

## Hardware

ESP WROOM 32 (2MB)

UART rx=32
I2C scl=18 sda=19 - BME680

Micropython firmware: ESP32_GENERIC-20240222-v1.22.2.bin


## config

The file `config.py` contains
```
# The Wifi network.
WLAN_SSID="foo"
WLAN_KEY="bar"
# The mDNS name of this device.
HOSTNAME="esp32-weather"
```


# Misc

SDR Navtex https://github.com/fventuri/navtex
Navtex live http://navtex.lv
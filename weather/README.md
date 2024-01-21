# Weather sensor

The weather sensor provides a HTTP endpoint to read NAVTEX and BME680 sensor data.

Sensors:
- [BME680](https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme680/) 
  sensor measuring relative humidity, barometric pressure, ambient temperature and gas over
  [I2C](https://docs.micropython.org/en/latest/esp32/quickref.html#hardware-i2c-bus)
- [NAVTEX](https://en.wikipedia.org/wiki/NAVTEX) messages over 
  [UART](https://docs.micropython.org/en/latest/esp32/quickref.html#uart-serial-bus)
  

## Hardware

ESP WROOM 32 (2MB)

UART rx=32
I2C scl=18 sda=19

Micropython firmware: ESP32_GENERIC-20240105-v1.22.1.bin


# Misc

SDR Navtex https://github.com/fventuri/navtex
Navtex live http://navtex.lv
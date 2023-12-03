# NMEA Sensor for motor

nmea-sensor-motor reads temperature sensors, motor RPM and periodically transmits a 
[NMEA0183 XDR](https://gitlab.com/gpsd/gpsd/-/blob/master/www/NMEA.adoc#user-content-xdr-transducer-measurement)
sentence to a TCP endpoint.

| Type  | Data   | Unit   | Name     |   |
|-------|--------|--------|----------|---|
| M     |        | C      | Exhaust  | Exhaust  |
| M     |        | C      | In       | Heat exchanger in  |
| M     |        | C      | Out      | Heat exchanger out |
| M     |        | R      | RPM      | Motor RPM |
| M     |        | C      | Oil      | Oil temperature |
| M     |        | P      | Oil      | Oil presure |


Units of measurement
A = Amperes
B = Bars
B = Binary
C = Celsius
D = Degrees
H = Hertz
I = liters/second
K = Kelvin
K = kg/m3
M = Meters
M = cubic Meters
N = Newton
P = % of full range
P = Pascal
R = RPM
S = Parts per thousand
V = Volts


Sensors:
- [DS18B20](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf) One-Wire temperature
- [ESP32 ADC](https://docs.micropython.org/en/latest/esp32/quickref.html#adc-analog-to-digital-conversion)
- [Time pulse](https://micropython-tve.readthedocs.io/en/counter/library/machine.html#machine.time_pulse_us)


## Hardware

ESP WROOM 32 (2MB)

Micropython firmware: ESP32_GENERIC-20231005-v1.21.0.bin

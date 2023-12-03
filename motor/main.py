import machine
import time
import config, nmea, snsr, wifi

print("nmea-sensor-motor v0.0.0")

# Sensors
sensors = [
    snsr.OneWire("M", "Exhaust", machine.Pin(23)),
    snsr.Rpm("M", "RPM", machine.Pin(22)),
    snsr.ADC("M", "Xyz", machine.Pin(32))
]

# NMEA multiplexer connection
connection = wifi.connection(config.WLAN_SSID, config.WLAN_KEY, config.NMEA_MULTIPLEXER_HOST, config.NMEA_MULTIPLEXER_PORT)

# Status led
led = machine.Pin(2, machine.Pin.OUT)


# Main
while True:
    time.sleep(1)

    sentence = "$MSXDR"
    for s in sensors:
       v = s.measure()
       sentence += ',' + v

    # calc checksum 
    cs = nmea.checksum(sentence)
    sentence = f"{sentence:s}*{cs:02X}\r\n"
    
    if len(sentence) > 80:
        print('warning: sentence too long:', sentence)
    else:
        print(sentence)
        
    # send to multiplexer
    connection.send(sentence)
    
    # show status
    led.value(not led.value())

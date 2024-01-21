import machine
import errno, time
import bme680, config, navtex, wifi

version = "v0.0.1"

print(config.HOSTNAME, version)
print("mem free: ", gc.mem_free())

# WIFI connection
connection = wifi.connection(config.WLAN_SSID, config.WLAN_KEY, config.HOSTNAME, '', 80)
connection.wlan_connect()
sock = connection.listen()

# Status led
led = machine.Pin(2, machine.Pin.OUT)

# Serial port
uart = machine.UART(1, baudrate=9600, tx=33, rx=32)

# RTC
rtc = machine.RTC()

# BME
i2c = machine.I2C(0) # 0 scl=18 sda=19
bme = bme680.BME680_I2C(i2c=i2c)


### Web requests

def resp_ok(conn):
    """
    :param conn: a socket connection
    """
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')

def resp_notfound(conn):
    """
    :param conn: a socket connection
    """
    conn.send('HTTP/1.1 404 Not Found\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')

def resp_internalservererror(conn):
    """
    :param conn: a socket connection
    """
    conn.send('HTTP/1.1 500 Internal Server Error\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')

def parse_req(b):
    s = 0
    i = 0
    while i < len(b) and b[i] != 32:
        i += 1
    verb = b[s:i].decode()
    i += 1
    s = i
    while i < len(b) and b[i] != 32:
        i += 1    
    path = b[s:i].decode()
    return verb, path

def homepage(conn):
    """
    """
    html = """<html><head><title>{hostname}</title></head><body>
    <p>{hostname} {version}</p>
    <a href="bme">BME sensor data</a>
    <a href="navtex">NAVTEX messages</a>
    </body></html>"""
    conn.sendall(html.format(hostname=config.HOSTNAME, version=version))
    
    
def handle_reqresp(conn, request):
    """
    :param conn: a socket connection
    :param request: bytebuffer container a request like: GET / HTTP/1.1\r\n
    """
    try: 
        verb, path = parse_req(request)
        if path == "/":
            resp_ok(conn)
            homepage(conn)
        elif path == "/navtex":
            resp_ok(conn)
            navtex.send_to(conn)
        elif path == "/bme":
            resp_ok(conn)
            bme680.send_to(conn, bme)
        else:
            resp_notfound(conn)
    finally:
        conn.close()
    

i = 0
tx = ""
def navtex_test_tx_ch():
    """
    Send a test navtex message, one char at a time.
    The navtex msg number changes each minute.
    """
    global i, tx
    if i == 0:
        t = rtc.datetime()
        tx = "ZCZC XX{5:02d}\n{0:04d}-{1:02d}-{2:02d} {4:02d}:{5:02d}:{6:02d}\nNNNN\n".format(*t)
    uart.write(tx[i])
    i += 1
    if i >= len(tx):
        i = 0


### Main
        
while True:
    # Test data 
    navtex_test_tx_ch()
    navtex_test_tx_ch()
    
    # Read NAVTEX messages
    n = uart.any()
    if n > 0:
        navtex.rx(uart.read(n))
    
    
    # Check for incoming web request
    # happy path timeouts at 0.3s
    try:
        sock.settimeout(0.3)
        conn, addr = sock.accept()
        conn.settimeout(1.0)
        request = conn.recv(1024)
        print(str(request), str(addr))
        handle_reqresp(conn, request)
    except OSError as e:
        if e.errno != errno.ETIMEDOUT:
            print(e)        
            conn.close()
    
    # Show status
    led.value(not led.value())

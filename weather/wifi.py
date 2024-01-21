import machine, network, usocket


# The maximum number of failures before reconnecting to the WLAN. 
MAX_CONSECUTIVE_SEND_FAILURES=3

class connection:
    """
    Connection can send data over TCP to a host in the WiFi network
    or receive data.
    
    :param ssid: Wifi network
    :param key: Wifi network
    :param hostname: mDNS name
    :param ip: ip address to connect to or bind to (empty string bind to all interfaces)
    :param port: port to connect to
    """
    def __init__(self, ssid, key, hostname, ip, port):
        self._ssid = ssid
        self._key = key
        self._hostname = hostname
        self._ip = ip
        self._port = port
        self._wlan = network.WLAN(network.STA_IF)
        self._wlan.active(True)
        self._consecutive_send_failures = 0

    def wlan_connect(self) -> bool:
        """
        Connect to the WLAN, return true on succesful connect.
        """
        if self._wlan.isconnected():
            return True
        print('WLAN scan')
        nets = self._wlan.scan()
        for net in nets:
            print(net)
            ssid = net[0].decode()
            if ssid == self._ssid:
                print('WLAN found')
                self._wlan.config(dhcp_hostname=self._hostname)
                self._wlan.connect(self._ssid, self._key)
                while not self._wlan.isconnected():
                    machine.idle()
                print('WLAN connected:', ssid, self._wlan.config('dhcp_hostname'), self._wlan.ifconfig())
                self._consecutive_send_failures = 0
                return True
        return False

    def send(self, data:str) -> bool:
        """
        Send a string to the destination over TCP.
        """
        if not self.wlan_connect():
            return False

        n = 0
        try:
            addr = usocket.getaddrinfo(self._ip, self._port)[0][-1]
            s = usocket.socket()
            s.connect(addr)
            n = s.send(data)
        except OSError as e:
            print('error: send:', e)
        finally:
            s.close()

        if n == len(data):
            self._consecutive_send_failures = 0
        else:
            self._consecutive_send_failures += 1
        if self._consecutive_send_failures > MAX_CONSECUTIVE_SEND_FAILURES:
            print('too many errors, reset WLAN')
            self._wlan.disconnect()

        return n == len(data)
    
    def listen(self):
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        s.bind((self._ip, self._port))
        s.listen()
        
        return s
    
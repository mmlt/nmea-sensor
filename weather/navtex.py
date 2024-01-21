# For live examples see http://navtex.lv/

buffer = bytearray(40000)
ind = 0
wrap = False

def put(b):
    global buffer, ind, wrap
    buffer[ind] = b
    ind += 1
    if ind >= len(buffer):
        wrap = True
        ind = 0

def rx(bytes):
    print(bytes.decode(), end="")    
    for i in range(len(bytes)):
        put(bytes[i])

def send_to(conn):
    global buffer, ind, wrap
    if wrap:
        conn.sendall(buffer[ind:])
        conn.sendall(buffer[:ind-1])
    else:
        conn.sendall(buffer[0:ind])
    
    
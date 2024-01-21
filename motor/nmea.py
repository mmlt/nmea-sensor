
def checksum(s:str) -> byte:
    if s[0] != "$":
        raise ValueError("Should start with '$'")
    
    last = len(s) 
    try:
        last = s.index('*')
    except:
        pass
    
    # mixing unicode and byte indices 
    cs = 0
    b = str.encode(s)
    for i in range(1, last):
        cs ^= b[i]
        
    return cs

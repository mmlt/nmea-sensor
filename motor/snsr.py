import machine, onewire, ds18x20


class OneWire:
    def __init__(self, type, name, pin):
        self._type = type
        self._name = name
        self._wire = onewire.OneWire(pin)
        self._ds = ds18x20.DS18X20(self._wire)
        self._roms = self._ds.scan()
        for rom in self._roms:
            print(name, 'ds18x20:', hex(int.from_bytes(rom, 'little')))

    def measure(self) -> str:
        """
        Measure returns a Type,Data,Unit,Name string.
        Call cycle time >750mS
        """
        zero_kelvin = 273.15
        v = self._ds.read_temp(self._roms[0]) #TODO single sensor expected
        self._ds.convert_temp()
        return f"{self._type:s},{v:3.1f},C,{self._name:s}"


class Counter:
    def __init__(self, type, name, pin):
        self._type = type
        self._name = name
        self._counter = machine.Counter(pin)

    def measure(self) -> str:
        """
        Measure returns a Type,Data,Unit,Name string.
        Call cycle time does not matter, more time increases precision.
        TODO not tested yet
        """
        c = this._counter.value()
        t = time.ticks_ms()
        if c < this.count:
            c = c + 2 << 16
        dc = c - this._count
        dt = time.ticks_diff(this._time, t)

        this._count = c and 2<<16 - 1
        this._time = t

        v = dc * 60000 / dt
        return f"{self._type:s},{v:.0f},C,{self._name:s}"


class Rpm:
    def __init__(self, type, name, pin):
        self._type = type
        self._name = name
        self._pin = pin

    def measure(self) -> str:
        """
        Measure returns a Type,Data,Unit,Name string.
        Call cycle time does not matter.
        """
        samples = []
        timeout = 100000 # uS
        n = 3
        # the first time_pulse_us result is discarded
        # https://micropython-tve.readthedocs.io/en/counter/library/machine.html#machine.time_pulse_us
        for _ in range(n):
            machine.time_pulse_us(self._pin, 1, timeout)
            v = machine.time_pulse_us(self._pin, 1, timeout)
            machine.time_pulse_us(self._pin, 0, timeout)
            v += machine.time_pulse_us(self._pin, 0, timeout)
            samples.append(v)
        samples.sort()
        US_IN_MIN = 60*1000*1000
        v = US_IN_MIN / samples[n//2]
        if v < 0:
            v = 0
        return f"{self._type:s},{v:.0f},R,{self._name:s}"


class ADC:
    def __init__(self, type, name, pin):
        self._type = type
        self._name = name
        self._adc = machine.ADC(pin)

    def measure(self) -> str:
        """
        Measure returns a Type,Data,Unit,Name string.
        Call cycle time does not matter.
        Use pin 32-39 (ADC block 1)
        https://docs.micropython.org/en/latest/esp32/quickref.html#adc-analog-to-digital-conversion
        """
        samples = []
        n = 3
        for _ in range(n):
            v = self._adc.read_uv()
            samples.append(v)
        samples.sort()
        UV_IN_V = 1000*1000
        v = samples[n//2] / UV_IN_V
        return f"{self._type:s},{v:.3f},V,{self._name:s}"


import machine

class Mux:
    def __init__(self, S0, S1, S2, S3, E, signal=0):
        self.S0 = machine.Pin(S0, machine.Pin.OUT)
        self.S1 = machine.Pin(S1, machine.Pin.OUT)
        self.S2 = machine.Pin(S2, machine.Pin.OUT)
        self.S3 = machine.Pin(S3, machine.Pin.OUT)
        self.E = machine.Pin(E, machine.Pin.OUT)
        self.signal = machine.ADC(signal)
        self._reset()
        self.current_bits = "0000"
        self.state = False

    def _reset(self):
        self.S0.off()
        self.S1.off()
        self.S2.off()
        self.S3.off()
        self.E.off()

    def switch_state(self):
        if self.state:
            self.E(0)
            self.state = False
        else:
            self.E(1)
            self.state = True

    def _bits_to_channel(self, bits):
        return int("0000" + "".join([str(x) for x in "".join(reversed(bits))]), 2)

    def _channel_to_bits(self, channel_id):
        return "".join(reversed("{:0>{w}}".format(bin(channel_id)[2:], w=4)))

    def _switch_pins_with_bits(self, bits):
        s0, s1, s2, s3 = [int(x) for x in tuple(bits)]
        self.S0(s0)
        self.S1(s1)
        self.S2(s2)
        self.S3(s3)

    def switch_channel(self, channel_id):
        bits = self._channel_to_bits(channel_id)
        self._switch_pins_with_bits(bits)
        self.current_bits = bits

mux = Mux(16, 5, 4, 0, 2)	# this is according to the GPIO wiring used. D0, D1, D2, D3,D4
mux.switch_state()			# turns on the reading
# print(mux.signal.read())	# reads the signal from channel 0 (default channel → “0000”)
# mux.switch_channel(15)	# switches to channel 12
# print(mux.signal.read())	# reads from channel 12


def sens_data(data):
    mux.switch_channel(14)
    print('Mux signal 15: ',mux.signal.read())
    mux.switch_channel(15)
    print('Mux signal 16: ',mux.signal.read())
    
    
timer = machine.Timer(0)
timer.init(period=1000, mode=machine.Timer.PERIODIC, callback = sens_data)



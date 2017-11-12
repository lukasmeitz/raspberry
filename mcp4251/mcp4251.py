# @author lukasmeitz

# imports
import spidev
import RPi.GPIO as gpio

# This class represents a mcp4215 digital potentiometer
class MCP4251:

    # constant definitions
    wiperAmask = 0
    wiperBmask = 32

    # constructor
    def __init__(self, bus, device, shutdown=-1):
        # SPI channel
        self.bus = bus

        # SPI chip for CS bit
        self.device = device

        # optional low active shutdown pin
        # this pin is set to high to power on the potentiometer
        self.shutdown = int(shutdown)

        # keep track of connectivity
        self.initialized = False

    def enable(self):
        # initialize SPI connection
        if not self.initialized:
            self.spi = spidev.SpiDev()
            self.spi.open(self.bus, self.device)
            self.spi.max_speed_hz = 7629

            self.initialized = True

        # check if shutdown pin is specified
        if not self.shutdown == -1:
            # ignore warnings in gpio setup
            try:
                gpio.setmode(gpio.BCM)
                gpio.setup(self.shutdown, gpio.OUT)
            except:
                pass

            # set shutdown pin to high
            gpio.output(self.shutdown, gpio.HIGH)

    def disable(self):
        # check status
        if self.initialized:

            # check if shutdown pin is specified
            if not self.shutdown == -1:

                # set shutdown pin to low
                gpio.output(self.shutdown, gpio.LOW)

    def close(self):
        # close SPI connection
        if self.initialized:

            self.spi.close()
            self.initialized = False

    def setA(self, value):
        #check value bounds
        _setWiper(value, 'A')

    def setB(self, value):
        #check value bounds
        _setWiper(value, 'B')

    def setBoth(self, value):
        # set value to both wipers
        setA(value)
        setB(value)

    def _setWiper(self, value, wiper):
        # check bounds
        value = int(value)
        if value < 0 or value > 1023:
            return

        # byte array
        # the most significant byte contains the first two bits of value
        msb = value >> 8

        # as well as the wiper adress
        if wiper == 'A':
            msb = msb | MCP4251.wiperAmask
        else if wiper == 'B':
            msb = msb | MCP4251.wiperBmask
        else:
            return

        # the less significant byte contains the remaining 8 bits of value
        lsb = value & 0xFF

        # send byte array to device
        self.spi.xfer([msb, lsb])

# end of class

# @author lukasmeitz

# imports
import mcp4251

# parameters
spibus = 0
spidevice = 0

# create object
poti = MCP4251(spibus, spidevice)

# initialize the object
poti.enable()

# set the resistance to min
poti.setBoth(1023)

# close the connection
poti.disable()
poti.close()

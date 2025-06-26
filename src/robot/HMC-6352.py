#!/usr/bin/env python3
import smbus
import time

# Initialize I2C (bus 1 is usually used on recent Raspberry Pi boards)
bus = smbus.SMBus(1)

# HMC-6352 default I2C address
DEVICE_ADDRESS = 0x21
GET_HEADING_COMMAND = 0x41

#Some important considerations about this Digital Compass Readings:
#0 degrees = North
#90 degrees = East
#180 degrees = South
#270 degrees = West
  

def read_compass_heading():
    """
    This function triggers a measurement on the HMC-6352 digital compass.
    It sends the command 0x41 (ASCII 'A') to the sensor, waits for the
    conversion (about 70-100ms recommended by the datasheet), and then reads
    two bytes of data. The heading is returned in degrees.
    """
    # Trigger the measurement; 0x41 is the command to take a measurement
    bus.write_byte(DEVICE_ADDRESS, 0x41)
    # Wait for conversion to complete
    time.sleep(0.1)
    
    # Read two bytes from the device starting at register 0
    data = bus.read_i2c_block_data(DEVICE_ADDRESS, 0, 2)
    
    # Combine the MSB and LSB into a single number (16-bit unsigned integer)
    heading_raw = (data[0] << 8) | data[1]
    # Convert the raw value (in tenths of a degree) into degrees
    heading_deg = heading_raw / 10.0
    return heading_deg

if __name__ == '__main__':
    print("Testing HMC-6352 Digital Compass Sensor...")
    try:
        while True:
            heading = read_compass_heading()
            print("Heading: {:.1f}°".format(heading))
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nExiting...")

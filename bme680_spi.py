import spidev
import time
import RPi.GPIO as GPIO

class BME688_SPI:
    def __init__(self, spi_bus=0, spi_device=0, cs_pin=24):
        self.spi = spidev.SpiDev()
        self.cs_pin = cs_pin
        self.spi_bus = spi_bus
        self.spi_device = spi_device
        
        # Setup CS pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.cs_pin, GPIO.OUT)
        GPIO.output(self.cs_pin, GPIO.HIGH)
        
        # SPI setup
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = 10000000  # 10MHz
        self.spi.mode = 0b00  # SPI mode 0
        
    def read_register(self, register):
        """Read from a BME688 register"""
        GPIO.output(self.cs_pin, GPIO.LOW)
        
        # Send register address with read bit
        tx_data = [register | 0x80, 0x00]
        rx_data = self.spi.xfer2(tx_data)
        
        GPIO.output(self.cs_pin, GPIO.HIGH)
        return rx_data[1]
    
    def write_register(self, register, value):
        """Write to a BME688 register"""
        GPIO.output(self.cs_pin, GPIO.LOW)
        
        # Send register address with write bit (cleared)
        tx_data = [register & 0x7F, value]
        self.spi.xfer2(tx_data)
        
        GPIO.output(self.cs_pin, GPIO.HIGH)
    
    def read_chip_id(self):
        """Read BME688 chip ID (should be 0x61)"""
        chip_id = self.read_register(0xD0)
        return chip_id
    
    def cleanup(self):
        self.spi.close()
        GPIO.cleanup()

# Test the connection
if __name__ == "__main__":
    try:
        # Try SPI bus 0 first (pins 19, 21, 23, 24)
        sensor = BME688_SPI(spi_bus=0, spi_device=0, cs_pin=24)
        
        chip_id = sensor.read_chip_id()
        print(f"BME688 Chip ID: 0x{chip_id:02X}")
        
        if chip_id == 0x61:
            print("✅ BME688 detected successfully!")
        else:
            print("❌ BME688 not found or wrong chip ID")
            
        sensor.cleanup()
        
    except Exception as e:
        print(f"Error: {e}")

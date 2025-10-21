#!/usr/bin/env python3
import spidev

# Check if SPI0 is working
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI0.0
spi.max_speed_hz = 1000000
spi.mode = 0

# Simple test
test_data = [0xD0 | 0x80, 0x00]  # Read chip ID
result = spi.xfer2(test_data)
print(f"SPI test - Sent: {[hex(x) for x in test_data]}")
print(f"SPI test - Received: {[hex(x) for x in result]}")
print(f"Chip ID should be at index 1: 0x{result[1]:02X}")

spi.close()

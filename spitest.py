#!/usr/bin/env python3
import spidev
import time

def test_bme688_spi():
    # Try different SPI configurations
    configs = [
        (0, 0),  # SPI bus 0, device 0
        (0, 1),  # SPI bus 0, device 1  
        (1, 0),  # SPI bus 1, device 0
        (1, 1),  # SPI bus 1, device 1
    ]
    
    for bus, device in configs:
        try:
            print(f"Testing SPI bus {bus}, device {device}...")
            spi = spidev.SpiDev()
            spi.open(bus, device)
            spi.max_speed_hz = 1000000  # 1MHz
            spi.mode = 0  # SPI mode 0
            
            # Try to read chip ID (register 0xD0)
            # Send: [Register with read bit, dummy byte]
            tx_data = [0xD0 | 0x80, 0x00]
            rx_data = spi.xfer2(tx_data)
            
            print(f"  Sent: {[hex(x) for x in tx_data]}")
            print(f"  Received: {[hex(x) for x in rx_data]}")
            print(f"  Chip ID (should be at index 1): 0x{rx_data[1]:02X}")
            
            if rx_data[1] == 0x61:
                print("  ✅ BME688 FOUND!")
                return (bus, device)
                
            spi.close()
            time.sleep(0.1)
            
        except Exception as e:
            print(f"  Error: {e}")
    
    return None

if __name__ == "__main__":
    print("Testing all SPI configurations for BME688...")
    result = test_bme688_spi()
    
    if result:
        print(f"\n🎉 SUCCESS! Use SPI bus {result[0]}, device {result[1]}")
    else:
        print("\n❌ No BME688 detected. Check wiring and power!")

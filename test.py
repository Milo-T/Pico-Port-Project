# test.py - Comprehensive system test
from port_data import get_real_weather, generate_rotterdam_data
import network
import time

def run_system_test():
    """Comprehensive test of all system components"""
    print("🧪 Rotterdam Dashboard System Test")
    print("=" * 50)

    # Test 1: WiFi Status
    print("\n📡 WiFi Status:")
    try:
        wlan = network.WLAN(network.STA_IF)
        if wlan.isconnected():
            print("✅ WiFi: CONNECTED")
            print(f"   IP: {wlan.ifconfig()[0]}")
        else:
            print("❌ WiFi: NOT CONNECTED")
    except:
        print("❌ WiFi: Pico W required")

    # Test 2: Weather API
    print("\n🌤️  Weather API:")
    try:
        weather = get_real_weather()
        print("✅ Weather: REAL-TIME WORKING"        print(f"   {weather['temperature']}, {weather['condition']}")
    except Exception as e:
        print(f"❌ Weather: FAILED - {e}")

    # Test 3: Data Generation
    print("\n🏭 Data Generation:")
    try:
        data = generate_rotterdam_data()
        print("✅ Data: GENERATED SUCCESSFULLY"        print(f"   Ships: {data['total_ships']}, Status: {data['port_status']}")
        print(f"   Source: {data['data_source']}")
    except Exception as e:
        print(f"❌ Data: FAILED - {e}")

    # Test 4: LCD Hardware
    print("\n📺 LCD Hardware:")
    try:
        from machine import Pin, I2C
        from lcd_simple import LCD1602
        i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
        lcd = LCD1602(i2c, 0x27)
        print("✅ LCD: DETECTED AND READY")
    except Exception as e:
        print(f"❌ LCD: NOT DETECTED - {e}")

    print("\n" + "=" * 50)
    print("🎯 TEST COMPLETE")
    print("\n💡 To run dashboard: import main")
    print("💡 For WiFi setup: import wifi_setup")

if __name__ == "__main__":
    run_system_test()

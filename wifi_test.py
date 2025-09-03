# wifi_test.py - Test WiFi connectivity and real-time data
import network
import time

def test_network():
    """Test network connectivity and attempt real-time data fetch"""
    try:
        # Check if we have network module
        wlan = network.WLAN(network.STA_IF)

        if wlan.isconnected():
            print("✅ WiFi is connected!")
            print("IP Address:", wlan.ifconfig()[0])
            print("Testing real-time data fetch...")

            # Test HTTP request to weather API
            try:
                import urequests
                print("Fetching weather data...")
                response = urequests.get("https://api.open-meteo.com/v1/forecast?latitude=51.92&longitude=4.48&current=temperature_2m", timeout=10)
                if response.status_code == 200:
                    print("✅ HTTP requests working!")
                    print("🌐 Real-time data is available!")
                    return True
                else:
                    print(f"❌ HTTP request failed: {response.status_code}")
            except Exception as e:
                print(f"❌ HTTP test failed: {e}")

        else:
            print("❌ WiFi is NOT connected")
            print("Available WiFi networks:")
            wlan.active(True)
            networks = wlan.scan()
            for net in networks:
                ssid = net[0].decode('utf-8')
                rssi = net[3]
                print(f"  - {ssid} (Signal: {rssi}dB)")

            print("\n📝 To connect:")
            print("1. Edit wifi_setup.py with your WiFi credentials")
            print("2. Run: import wifi_setup")
            print("3. Then restart the dashboard")

        return False

    except ImportError:
        print("❌ No network module found!")
        print("   This appears to be a regular Raspberry Pi Pico (not Pico W)")
        print("   Real-time data requires Pico W with WiFi capability")
        print("   Current setup uses simulation mode")
        return False
    except Exception as e:
        print(f"❌ Network test failed: {e}")
        return False

if __name__ == "__main__":
    print("WiFi Connectivity Test")
    print("=" * 30)
    test_network()

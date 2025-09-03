# wifi_setup.py - WiFi connection setup for Raspberry Pi Pico W
import network
import time

# WiFi credentials - UPDATE THESE!
WIFI_SSID = "YOUR_WIFI_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

def connect_wifi():
    """Connect to WiFi and return connection status"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        # Wait for connection with timeout
        timeout = 20  # 20 seconds timeout
        start_time = time.time()

        while not wlan.isconnected():
            if time.time() - start_time > timeout:
                print('WiFi connection timeout!')
                return False
            time.sleep(0.5)
            print('.', end='')

    if wlan.isconnected():
        print('\n✅ WiFi connected successfully!')
        print('IP address:', wlan.ifconfig()[0])
        return True
    else:
        print('\n❌ WiFi connection failed!')
        return False

# Test the connection
if __name__ == "__main__":
    print("Testing WiFi connection...")
    success = connect_wifi()
    if success:
        print("🎉 Your Pico W is now connected to the internet!")
        print("Real-time Rotterdam data should now work!")
    else:
        print("❌ WiFi setup failed. Check your credentials.")

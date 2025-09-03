# main.py - Consolidated Rotterdam Port Dashboard
from machine import Pin, I2C
import time
import network
from lcd_simple import LCD1602
from display_manager import DisplayManager
from port_data import generate_rotterdam_data
from config import LCD_I2C_ADDRESS, BUTTON_PIN

# WiFi Configuration - UPDATE THESE!
WIFI_SSID = "Hyperoptic Fibre B413"
WIFI_PASSWORD = "uJejL8X4MeafaK"

def connect_wifi():
    """Connect to WiFi network"""
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
            print("WiFi already connected:", wlan.ifconfig()[0])
            return True

        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        # Wait for connection
        timeout = 15
        for i in range(timeout):
            if wlan.isconnected():
                print("✅ WiFi connected!")
                print("IP:", wlan.ifconfig()[0])
                return True
            time.sleep(1)
            print(".", end="")

        print("\n❌ WiFi connection failed!")
        return False
    except Exception as e:
        print(f"❌ WiFi error: {e}")
        print("Note: This requires a Raspberry Pi Pico W")
        return False

def get_display_data():
    """Generate port data for display"""
    data = generate_rotterdam_data()
    # Add timestamp for logging
    t = time.localtime()
    data["timestamp"] = f"{t[3]:02d}:{t[4]:02d}"
    return data



# Configuration for auto-advance and debouncing
AUTO_ADVANCE_MS = 5000  # Auto-advance every 5 seconds
DEBOUNCE_MS = 250       # Debounce button presses

# Connect to WiFi first
wifi_connected = connect_wifi()

# Initialize hardware
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = LCD1602(i2c, LCD_I2C_ADDRESS)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# Initialize display manager and data
display = DisplayManager(lcd)
current_data = get_display_data()

print("Rotterdam Port Display Ready!")
if wifi_connected:
    print("🌐 WiFi connected - Real-time data available!")
else:
    print("📶 No WiFi - Using simulation mode")
    print("   To enable real-time data: Update WIFI_SSID and WIFI_PASSWORD")
print("Auto-advancing through 7 views every 5 seconds (or press button)")
display.next_view(current_data)

# Button handling with debouncing
button_pressed_flag = False
last_press_ms = 0
last_auto_ms = time.ticks_ms()

def on_button(pin):
    global button_pressed_flag, last_press_ms
    now = time.ticks_ms()
    if time.ticks_diff(now, last_press_ms) > DEBOUNCE_MS:
        button_pressed_flag = True
        last_press_ms = now

button.irq(trigger=Pin.IRQ_FALLING, handler=on_button)

# Main loop with auto-advance
while True:
    now = time.ticks_ms()
    auto_due = time.ticks_diff(now, last_auto_ms) >= AUTO_ADVANCE_MS

    if button_pressed_flag or auto_due:
        button_pressed_flag = False
        last_auto_ms = now
        current_data = get_display_data()
        display.next_view(current_data)
        source_indicator = "REAL" if current_data.get('data_source') == "REAL" else "SIMULATION"
        print(f"Advanced at {current_data['timestamp']} [{source_indicator}]")

    time.sleep(0.05)

from machine import Pin, SPI
import max7219
from time import sleep

# --- CONFIGURE YOUR PINS HERE ---
# Create an SPI object on SPI channel 0 (GP2, GP3, GP4, GP5, GP6, GP7)
# sck=GP2, mosi=GP3, cs=GP5
spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
# Initialize the display
display = max7219.Matrix8x8(spi, Pin(5), 4) # 4 means we have 4 matrices in series
# ---------------------------------

# Set the brightness (a value between 0 and 15)
display.brightness(5)

# Clear the display
display.fill(0)
display.show()

try:
    # Example 1: Scrolling Text
    print("Starting scroll text")
    text = "Hello Pico! "
    while True:
        # Show a scrolling text message
        display.fill(0)
        display.text(text, 0, 0, 1)
        display.show()
        sleep(0.1)
        # Shift the text one pixel to the left
        text = text[1:] + text[0]
        
except KeyboardInterrupt:
    # Example 2: Clear and show a static smiley when you stop the script (Ctrl+C)
    display.fill(0)
    # Draw a smiley face (8x8)
    # Eyes
    display.pixel(1, 1, 1)
    display.pixel(1, 2, 1)
    display.pixel(2, 1, 1)
    display.pixel(2, 2, 1)
    
    display.pixel(5, 1, 1)
    display.pixel(5, 2, 1)
    display.pixel(6, 1, 1)
    display.pixel(6, 2, 1)
    
    # Mouth
    display.pixel(2, 5, 1)
    display.pixel(3, 6, 1)
    display.pixel(4, 6, 1)
    display.pixel(5, 5, 1)
    
    display.show()
    print("Done!")
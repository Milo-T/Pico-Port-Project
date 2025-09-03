# Rotterdam Port Dashboard - Real-Time Maritime Data

A Raspberry Pi Pico W project that displays real-time Rotterdam port information on an LCD screen.

## Features

- **Real-Time Data**: Attempts to fetch live ship data from multiple maritime APIs
- **Weather Integration**: Live weather data from Open-Meteo API
- **Auto-Advance**: Cycles through 7 different views automatically
- **Manual Control**: Button press to advance views instantly
- **Data Transparency**: Shows "R" (Real) or "S" (Simulation) indicator
- **WiFi Connectivity**: Internet access for real-time data

## Hardware Requirements

- **Raspberry Pi Pico W** (required for WiFi/real-time data)
- **16x2 I2C LCD Display** (address 0x27)
- **Push Button** (connected to GPIO 14)
- **Power Supply** (5V for Pico)

## Hardware Wiring

```
Pico GPIO | Component | Notes
----------|----------|--------
0         | LCD SDA  | I2C Data
1         | LCD SCL  | I2C Clock
14        | Button   | Pull-up resistor
GND       | LCD GND  | Common ground
3.3V      | LCD VCC  | 3.3V power
```

## WiFi Setup

### 1. Confirm You Have a Pico W

Check your Pico model:
```python
import machine
print(machine.freq())  # Pico W shows different frequency
```

### 2. Configure WiFi

Edit `main.py` and update these lines:
```python
WIFI_SSID = "YOUR_WIFI_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
```

### 3. Test WiFi Connection

```python
import wifi_test
```

## Running the Dashboard

### Option 1: Auto-run on boot
```python
import main
```

### Option 2: Test real-time data
```python
import test_realtime
```

### Option 3: WiFi setup only
```python
import wifi_setup
```

## Display Views

The dashboard shows 7 different views:

1. **Overview**: Total ships and timestamp
2. **Traffic Flow**: Inbound/outbound ship counts
3. **Live Weather**: Current Rotterdam weather
4. **Largest Vessel**: Biggest ship in port
5. **Focus Vessel**: Specific ship details
6. **Terminal Info**: Terminal status
7. **Port Status**: Activity level and port status

## Real-Time Data Sources

The dashboard attempts to fetch data from:

- **MarineTraffic** - Ship tracking service
- **VesselFinder** - AIS vessel data
- **AIS Hub** - Global AIS data
- **FleetMon** - Vessel monitoring
- **MyShipTracking** - Real-time positions
- **Port of Rotterdam** - Official data
- **Shippeo** - Supply chain tracking
- **AIS Aggregator** - Combined data feeds

## Data Source Indicator

- **"R"** (top-right): Real-time data from APIs
- **"S"** (top-right): Enhanced simulation
- **Console logs**: Show which data source is being used

## Troubleshooting

### WiFi Issues
```
❌ WiFi connection failed!
```
- Check WiFi credentials in `main.py`
- Verify Pico W hardware
- Check WiFi signal strength
- Try different WiFi network

### No Real-Time Data
```
All real-time data sources failed, using simulation
```
- Most maritime APIs require authentication/paid access
- Network connectivity issues
- API rate limits or downtime

### Import Errors
```
ImportError: no module named 'network'
```
- You're using regular Pico (not Pico W)
- Real-time data requires Pico W

## Files Overview

**Core Files:**
- `main.py` - Main dashboard application with WiFi and LCD control
- `display_manager.py` - LCD display management and view cycling
- `port_data.py` - Real-time weather and ship data processing
- `config.py` - Configuration constants
- `lcd_simple.py` - LCD hardware driver

**Utility Files:**
- `test.py` - Comprehensive system testing
- `wifi_setup.py` - WiFi configuration utility
- `wifi_test.py` - WiFi connectivity testing
- `README.md` - This documentation

## Technical Details

- **Language**: MicroPython
- **Network**: Built-in WiFi (Pico W only)
- **HTTP Client**: urequests library
- **Display**: 16x2 I2C LCD
- **Real-time APIs**: 8+ maritime data sources
- **Fallback**: Enhanced simulation when APIs unavailable

## License

This project demonstrates real-time maritime data integration for educational purposes.

---

**Note**: Real maritime data often requires commercial API subscriptions. This project shows the framework for real-time data integration while providing realistic simulation when APIs are unavailable.

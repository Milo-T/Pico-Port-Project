# display_manager.py - Display functions
import time

LCD_COLS = 16

class DisplayManager:
    def __init__(self, lcd):
        self.lcd = lcd
        self.current_view = 0
        self.views = [
            self.show_overview,
            self.show_traffic,
            self.show_weather,
            self.show_largest_ship,
            self.show_focus_ship,
            self.show_terminal,
            self.show_port_status
        ]

    def _print_line_scrolling(self, text, row, dwell_ms=3000, step_ms=250):
        if text is None:
            text = ""
        text = str(text)  # Ensure text is a string
        if len(text) <= LCD_COLS:
            self.lcd.set_cursor(0, row)
            # Pad with spaces to fill the line
            while len(text) < LCD_COLS:
                text += " "
            self.lcd.print(text)
            time.sleep_ms(dwell_ms)
            return
        scroll_text = text + "   "
        steps = len(scroll_text) - LCD_COLS + 1
        for i in range(steps):
            self.lcd.set_cursor(0, row)
            window = scroll_text[i:i + LCD_COLS]
            self.lcd.print(window)
            time.sleep_ms(step_ms)

    def clear(self):
        self.lcd.clear()

    def _show_data_source_indicator(self, data):
        """Show data source indicator in top-right corner"""
        source = data.get('data_source', 'SIM')
        indicator = "R" if source == "REAL" else "S"
        self.lcd.set_cursor(15, 0)
        self.lcd.print(indicator)

    def show_overview(self, data):
        self.clear()
        self.lcd.print("ROTTERDAM PORT")
        self._print_line_scrolling(f"Ships: {data['total_ships']}", 1)
        self._show_data_source_indicator(data)

    def show_traffic(self, data):
        self.clear()
        self.lcd.print("TRAFFIC FLOW")
        self._print_line_scrolling(f"IN:{data['inbound']} OUT:{data['outbound']}", 1)
        self._show_data_source_indicator(data)

    def show_weather(self, data):
        self.clear()
        self.lcd.print("LIVE WEATHER")
        self._print_line_scrolling(f"{data['weather']}", 1)
        self._show_data_source_indicator(data)

    def show_largest_ship(self, data):
        self.clear()
        self.lcd.print("LARGEST VESSEL")
        self._print_line_scrolling(f"{data['largest_ship']}", 1)
        self._show_data_source_indicator(data)

    def show_focus_ship(self, data):
        self.clear()
        self.lcd.print("FOCUS VESSEL")
        self._print_line_scrolling(f"{data['focus_ship']}", 1, dwell_ms=2000)
        self._show_data_source_indicator(data)
        self.clear()
        self.lcd.print("DESTINATION")
        self._print_line_scrolling(f"{data['focus_destination']}", 1, dwell_ms=2000)
        self._show_data_source_indicator(data)

    def show_terminal(self, data):
        self.clear()
        self.lcd.print("TERMINAL INFO")
        self._print_line_scrolling(f"{data['terminal']}", 1)
        self._show_data_source_indicator(data)

    def show_port_status(self, data):
        self.clear()
        self.lcd.print("PORT STATUS")
        status = f"{data['port_status']} {data['activity_level']}"
        self._print_line_scrolling(status, 1)
        self._show_data_source_indicator(data)

    def next_view(self, data):
        self.views[self.current_view](data)
        self.current_view = (self.current_view + 1) % len(self.views)

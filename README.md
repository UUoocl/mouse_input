# Mouse Input Monitor

An OBS Studio Python script to monitor mouse position, clicks, and scroll events, visualizing them in real-time via a Browser Source.

created with Google Gemini CLI
## Usage

### Prerequisites
- **OBS Studio** (Windows or macOS recommended).
- **Python 3.11+** installed and configured in OBS (Tools -> Settings -> Scripts -> Python Settings).
- **pynput** library installed in your Python environment:
  ```bash
  pip install pynput
  ```

### Setup in OBS
1. **Add the Browser Source:**
   - Create a new Browser Source in your OBS scene.
   - Check "Local file" and select `mouse_monitor.html`.
   - Set the width and height as desired (e.g., 300x600).
2. **Load the Script:**
   - Go to `Tools` -> `Scripts`.
   - Click the `+` button and select `mouse_monitor_browserSource.py`.
3. **Configure the Script:**
   - In the Scripts window, select the `mouse_monitor_browserSource` script.
   - Toggle the checkboxes for the events you want to monitor (Clicks, Position, Scroll).
   - For each event, select the Browser Source you created in step 1 from the dropdown list.
4. **Interact:**
   - The monitor will now update in real-time as you move your mouse, click, or scroll.

## Developer Overview

This project follows a producer-consumer architecture designed to bridge system-level input with web-level visualization:

1.  **Producer (Python):** `mouse_monitor_browserSource.py` uses `pynput` to capture global mouse events. It uses the OBS `javascript_event` API to dispatch these events into the Browser Source context.
2.  **Bridge (HTML/JS):** `mouse_monitor.html` listens for these custom DOM events. It updates its own UI and simultaneously broadcasts the data using the **BroadcastChannel API**.
3.  **Consumer (External):** `listener.html` demonstrates how any other page on the same origin can subscribe to these channels (`mouse_click`, `mouse_move`, `mouse_scroll`) to react to mouse input independently of the main visualization.

## Documentation

Full API documentation and technical details are available at:
[http://uuoocl.github.io/python_mouse_input](http://uuoocl.github.io/python_mouse_input)

Building documentation locally:
```bash
cd docs
make html
```
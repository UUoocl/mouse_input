.. Mouse Input Monitor documentation master file, created by
   sphinx-quickstart on Sun Jan  4 08:20:41 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Mouse Input Monitor documentation
=================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   frontend
   listener

Project Overview
================

The **Mouse Input Monitor** is a tool designed to visualize mouse interactions within OBS Studio. It consists of a Python script that runs within OBS and an HTML/JavaScript frontend that displays the captured events.

Functionality
-------------

1. **Python Script (`mouse_monitor_browserSource.py`):**
   - Uses the `pynput` library to listen for global mouse events (clicks, movement, scrolling).
   - Integrates with the OBS Studio API (`obspython`) to create a script interface.
   - Allows users to select specific OBS Browser Sources to receive event data.
   - Dispatches custom `javascript_event` calls to the selected Browser Sources containing event details (coordinates, button state, scroll delta).
   - **New:** Implements a smoothing algorithm for scroll value resets to provide a more natural visual decay when scrolling stops.

2. **Frontend (`mouse_monitor.html`):**
   - A styled HTML page intended to be loaded as a Browser Source in OBS.
   - Listens for the custom events dispatched by the Python script.
   - Parses the event data and updates the UI in real-time.
   - Visualizes clicks with button indicators, movement with coordinate displays, and scroll actions.

Usage
-----

1. Load `mouse_monitor.html` as a Browser Source in your OBS scene.
2. Load the `mouse_monitor_browserSource.py` script in the OBS Scripts window.
3. Configure the script to target your created Browser Source.
4. Enable the monitoring toggles to start visualizing input.

Frontend Monitor (mouse_monitor.html)
=====================================

The frontend component is a standalone HTML page designed to be used as an OBS Browser Source. It serves two primary purposes:
1. **Visualization**: Providing real-time visual feedback of mouse actions.
2. **Relay**: Broadcasting event data to other browser contexts via the ``BroadcastChannel`` API.

HTML Structure
--------------

The UI is organized into three "cards," each dedicated to a specific mouse event type:

*   **Mouse Click Card** (``#click-card``): Displays the button pressed (MB1, MB2, MB3), the coordinates, and the current state (DOWN/UP).
*   **Mouse Position Card** (``#move-card``): Displays the live X and Y coordinates of the cursor.
*   **Mouse Scroll Card** (``#scroll-card``): Displays the scroll delta (dx, dy) and the cursor position during the scroll.

Event Listeners
---------------

The page listens for custom DOM events dispatched by the OBS environment (via the Python script).

MouseClick
~~~~~~~~~~
Triggered when a mouse button is pressed or released.
*   **Data Source**: ``event.detail``
*   **Logic**: Updates the click card and flashes the border red.

MouseMove
~~~~~~~~~
Triggered on every pixel movement of the mouse.
*   **Data Source**: ``event.detail``
*   **Logic**: Updates the coordinate display. To maintain performance and reduce visual noise, this card does not flash on update.

MouseScroll
~~~~~~~~~~~
Triggered when the scroll wheel is moved.
*   **Data Source**: ``event.detail``
*   **Logic**: Updates the delta values and flashes the border green.

Inter-tab Communication (BroadcastChannel)
------------------------------------------

To allow other overlays or tools to react to mouse input without being direct OBS Browser Sources, this page implements the ``BroadcastChannel`` API. 

When an event is received, the data is posted to one of the following channels:

*   ``mouse_click``
*   ``mouse_move``
*   ``mouse_scroll``

**Example Usage in another page:**

.. code-block:: javascript

   const clickChannel = new BroadcastChannel('mouse_click');
   clickChannel.onmessage = (event) => {
       console.log('Click detected at:', event.data.x, event.data.y);
   };

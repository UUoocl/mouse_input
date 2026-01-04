import obspython as obs
from pynput import mouse
import json

script_settings = None  # OBS settings

click_source_name = ""
click_monitor = None

position_source_name = ""
position_monitor = None

scroll_source_name = ""
scroll_monitor = None

# Defaults
DEFAULT_SOURCE_NAME = ""


def on_click(x, y, button, pressed):
    if pressed:
        btn_code = ""
        if button == mouse.Button.left:
            btn_code = "MB1"
        elif button == mouse.Button.right:
            btn_code = "MB2"
        elif button == mouse.Button.middle:
            btn_code = "MB3"
        
        if btn_code:
            data = {
                "button": btn_code,
                "x": int(x),
                "y": int(y),
                "pressed": pressed
            }
            update_browser_source(click_source_name, "MouseClick", data)


def on_move(x, y):
    data = {
        "x": int(x),
        "y": int(y)
    }
    update_browser_source(position_source_name, "MouseMove", data)


def on_scroll(x, y, dx, dy):
    data = {
        "x": int(x),
        "y": int(y),
        "dx": int(dx),
        "dy": int(dy)
    }
    update_browser_source(scroll_source_name, "MouseScroll", data)


def update_browser_source(source_name, event_name, data):
    source = obs.obs_get_source_by_name(source_name)
    if source is not None:
        cd = obs.calldata_create()
        obs.calldata_set_string(cd, "eventName", event_name)
        obs.calldata_set_string(cd, "jsonString", json.dumps(data))
        obs.proc_handler_call(obs.obs_source_get_proc_handler(source), "javascript_event", cd)
        obs.calldata_destroy(cd)
        obs.obs_source_release(source)


def script_description():
    return "Monitors mouse clicks and sends events to a browser source."


def script_defaults(settings):
    obs.obs_data_set_default_string(settings, "click_source_name", DEFAULT_SOURCE_NAME)
    

def script_properties():
    props = obs.obs_properties_create()
    
    bool_click = obs.obs_properties_add_bool(props, "click_bool", "monitor mouse clicks")
    obs.obs_property_set_long_description(bool_click, "Check to monitor mouse clicks, else uncheck")
    click = obs.obs_properties_add_list(
        props,
        "click_source_name",
        "Click Source",
        obs.OBS_COMBO_TYPE_LIST,
        obs.OBS_COMBO_FORMAT_STRING
    )

    bool_position = obs.obs_properties_add_bool(props, "position_bool", "monitor mouse position")
    obs.obs_property_set_long_description(bool_position, "Check to monitor mouse position, else uncheck")
    position = obs.obs_properties_add_list(
        props,
        "position_source_name",
        "Position Source",
        obs.OBS_COMBO_TYPE_LIST,
        obs.OBS_COMBO_FORMAT_STRING
    )

    bool_scroll = obs.obs_properties_add_bool(props, "scroll_bool", "monitor mouse scroll")
    obs.obs_property_set_long_description(bool_scroll, "Check to monitor mouse scroll, else uncheck")
    scroll = obs.obs_properties_add_list(
        props,
        "scroll_source_name",
        "Scroll Source",
        obs.OBS_COMBO_TYPE_LIST,
        obs.OBS_COMBO_FORMAT_STRING
    )

    # populate drop down lists of browser sources
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_type = obs.obs_source_get_type(source)
            if source_type == obs.OBS_SOURCE_TYPE_INPUT:
                unversioned_id = obs.obs_source_get_unversioned_id(source)
                if unversioned_id == "browser_source":
                    name = obs.obs_source_get_name(source)
                    obs.obs_property_list_add_string(click, name, name)
                    obs.obs_property_list_add_string(position, name, name)
                    obs.obs_property_list_add_string(scroll, name, name)
        obs.source_list_release(sources)    

    return props


def script_load(settings):
    global click_monitor, click_source_name, position_monitor, position_source_name, scroll_monitor, scroll_source_name, script_settings
    print("loading mouse script")
    script_settings = settings  # Store OBS settings

    click_bool = obs.obs_data_get_bool(settings, "click_bool")
    position_bool = obs.obs_data_get_bool(settings, "position_bool")
    scroll_bool = obs.obs_data_get_bool(settings, "scroll_bool")
    print(f"click boolean {click_bool}")
    print(f"pos boolean {position_bool}")
    print(f"scroll boolean {scroll_bool}")

    # Stop existing monitors if they are running
    if click_monitor:
        click_monitor.stop()
    if position_monitor:
        position_monitor.stop()
    if scroll_monitor:
        scroll_monitor.stop()

    if click_bool:
        click_source_name = obs.obs_data_get_string(settings, "click_source_name")
        click_monitor = mouse.Listener(on_click=on_click)
        click_monitor.start()
    
    if position_bool:
        position_source_name = obs.obs_data_get_string(settings, "position_source_name")
        position_monitor = mouse.Listener(on_move=on_move)
        position_monitor.start()

    if scroll_bool:
        scroll_source_name = obs.obs_data_get_string(settings, "scroll_source_name")
        scroll_monitor = mouse.Listener(on_scroll=on_scroll)
        scroll_monitor.start()
    

def script_unload():
    global click_monitor, position_monitor, scroll_monitor
        
    if click_monitor:
        click_monitor.stop()
    click_monitor = None

    if position_monitor:
        position_monitor.stop()
    position_monitor = None

    if scroll_monitor:
        scroll_monitor.stop()
    scroll_monitor = None
    

def script_update(settings):
    script_load(settings)

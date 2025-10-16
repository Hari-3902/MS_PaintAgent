import time
import pyautogui

from .calibration import load_calibration, _extract_tools_and_canvas
from .paint import open_ms_paint, focus_paint_window, click_tool


def _get_canvas_bounds(canvas):
    if not canvas:
        return None
    try:
        x1, y1 = canvas["top_left"]
        x2, y2 = canvas["bottom_right"]
        left, right = (min(x1, x2), max(x1, x2))
        top, bottom = (min(y1, y2), max(y1, y2))
        return (left, top, right, bottom)
    except Exception:
        return None


def _clamp_point(x, y, canvas_bounds):
    if not canvas_bounds:
        return int(x), int(y)
    x1, y1, x2, y2 = canvas_bounds
    print(f"Clamping point: {x}, {y} to canvas bounds: {x1}, {y1}, {x2}, {y2}")

    cx = x1 + x
    cy = y1 + y

    return cx, cy


def _moveTo_clamped(x, y, canvas_bounds):
    cx, cy = _clamp_point(x, y, canvas_bounds)
    print(f"Moving to: {cx}, {cy}")
    pyautogui.moveTo(cx, cy)
    return cx, cy


def _drag_from_current_to_clamped(start_x, start_y, end_x, end_y, canvas_bounds, move_duration=0.3, button='left'):
    """
    Works reliably for all shape tools in MS Paint.
    Ensures:
      - Canvas is focused
      - Drawing starts & ends inside canvas
      - Final click commits the shape
    """

    # 1. Ensure Paint window is focused
    pyautogui.click(canvas_bounds[0] + 10, canvas_bounds[1] + 10)
    time.sleep(0.2)  # allow Paint to focus

    # 2. Move to starting point (inside canvas)
    pyautogui.moveTo(start_x, start_y)
    time.sleep(0.1)

    # 3. Press and drag
    pyautogui.mouseDown(button=button)
    pyautogui.moveTo(end_x, end_y, duration=move_duration)
    pyautogui.mouseUp(button=button)
    time.sleep(0.2)

    # 4. Finalize shape with a click inside it
    mid_x = (start_x + end_x) // 2
    mid_y = (start_y + end_y) // 2
    pyautogui.moveTo(mid_x, mid_y)
    pyautogui.click()
    time.sleep(0.2)


def draw_line(start_x, start_y, end_x, end_y, positions, canvas=None):
    click_tool("line", positions)
    time.sleep(0.1)
    bounds = _get_canvas_bounds(canvas)

    start_cx, start_cy = _moveTo_clamped(start_x, start_y, bounds)
    end_cx, end_cy = _moveTo_clamped(end_x, end_y, bounds)
    print(start_cx, start_cy, end_cx, end_cy)

    _drag_from_current_to_clamped(start_cx, start_cy, end_cx, end_cy, bounds, move_duration=0.4)

    time.sleep(0.2)


def draw_rectangle(start_x, start_y, end_x, end_y, positions, canvas=None):
    """Draws a rectangle in MS Paint."""
    click_tool("rectangle", positions)
    time.sleep(0.1)
    bounds = _get_canvas_bounds(canvas)

    start_cx, start_cy = _moveTo_clamped(start_x, start_y, bounds)
    end_cx, end_cy = _moveTo_clamped(end_x, end_y, bounds)
    print(start_cx, start_cy, end_cx, end_cy)

    _drag_from_current_to_clamped(start_cx, start_cy, end_cx, end_cy, bounds, move_duration=0.4)

    time.sleep(0.2)


def draw_shapes(shapes_list):
    # Load or use default calibration
    calib = load_calibration()
    positions, canvas = _extract_tools_and_canvas(calib)
    if positions is None:
        print("No calibration found. Using default positions.")
        print("Run calibrate_tools() first for better accuracy.")
        raise ValueError("No calibration found. Set Calibrate tool positions first.")
    else:
        print("Using calibrated tool positions.")

    if canvas:
        print("Using calibrated canvas bounds.")
    else:
        raise ValueError("No canvas calibration found. Set Calibrate canvas bounds first.")

    # Open MS Paint
    if not open_ms_paint():
        return False

    # Focus the Paint window
    if not focus_paint_window():
        print("Please click on the Paint window and run again")
        return False

    print("Starting to draw shapes...")
    time.sleep(1)

    for i, shape_data in enumerate(shapes_list):
        shape_type = shape_data.get("shape", "").lower()
        
        print(f"Drawing shape {i+1}/{len(shapes_list)}: {shape_type}")

        try:
            if shape_type == "rectangle":
                draw_rectangle(
                    shape_data["start_x"], shape_data["start_y"], 
                    shape_data["end_x"], shape_data["end_y"], 
                    positions, canvas
                )
            elif shape_type == "line":
                draw_line(
                    shape_data["start_x"], shape_data["start_y"], 
                    shape_data["end_x"], shape_data["end_y"], 
                    positions, canvas
                )
        except Exception as e:
            print(f"Error drawing {shape_type}: {e}")

    return True



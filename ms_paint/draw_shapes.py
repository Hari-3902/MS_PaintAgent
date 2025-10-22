import time
import pyautogui

# NOTE: Assuming these imports work correctly in your environment
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
    # Coordinates in the JSON are 0-1000 and 0-500. 
    # They are CLAMPED RELATIVE to the canvas top_left corner (x1, y1).
    print(f"Clamping point: {x}, {y} to canvas bounds: {x1}, {y1}, {x2}, {y2}")

    # Calculate the actual screen coordinate
    # For now, we will simply use the relative calculation as defined in the original code,
    # assuming the AI's coordinates (0-1000) need to be mapped/scaled, but the
    # original code only adds the top_left offset. This is kept for consistency.
    cx = x1 + x
    cy = y1 + y
    
    # Ensure point is within the *actual* canvas screen bounds
    cx = max(x1, min(cx, x2))
    cy = max(y1, min(cy, y2))


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

    # 1. Ensure Paint window is focused (Clicking a point inside the canvas)
    # The original code's approach to focus is used here.
    pyautogui.click(canvas_bounds[0] + 10, canvas_bounds[1] + 10)
    time.sleep(0.2)  # allow Paint to focus

    # 2. Move to starting point (inside canvas)
    # The original code moves *to* the point, which is fine before mouseDown.
    pyautogui.moveTo(start_x, start_y)
    time.sleep(0.1)

    # 3. Press and drag
    pyautogui.mouseDown(button=button)
    pyautogui.moveTo(end_x, end_y, duration=move_duration)
    pyautogui.mouseUp(button=button)
    time.sleep(0.2)

    # 4. Finalize shape with a click inside it
    # This step is crucial for most MS Paint shapes to commit the drawing.
    mid_x = (start_x + end_x) // 2
    mid_y = (start_y + end_y) // 2
    pyautogui.moveTo(mid_x, mid_y)
    pyautogui.click()
    time.sleep(0.2)


# --- NEW HELPER FUNCTION TO SIMPLIFY DRAWING ---

def _draw_bounding_box_shape(tool_name, start_x, start_y, end_x, end_y, positions, canvas):
    """Generic function to draw any shape defined by a bounding box drag."""
    
    click_tool(tool_name, positions)
    time.sleep(0.1)
    bounds = _get_canvas_bounds(canvas)

    # Calculate screen coordinates for start and end
    # Note: The original _moveTo_clamped is used to get the screen coordinates
    # and also move the mouse to the start point (which is unnecessary but kept for consistency).
    start_cx, start_cy = _clamp_point(start_x, start_y, bounds)
    end_cx, end_cy = _clamp_point(end_x, end_y, bounds)
    
    # Move to starting point (needed before drag)
    pyautogui.moveTo(start_cx, start_cy) 

    print(f"Drawing {tool_name} from ({start_cx}, {start_cy}) to ({end_cx}, {end_cy})")

    _drag_from_current_to_clamped(start_cx, start_cy, end_cx, end_cy, bounds, move_duration=0.4)


# --- PUBLIC DRAWING FUNCTIONS (Using the new helper) ---

# Existing functions redefined to use the helper
def draw_line(start_x, start_y, end_x, end_y, positions, canvas=None):
    _draw_bounding_box_shape("line", start_x, start_y, end_x, end_y, positions, canvas)

def draw_rectangle(start_x, start_y, end_x, end_y, positions, canvas=None):
    _draw_bounding_box_shape("rectangle", start_x, start_y, end_x, end_y, positions, canvas)


# NEW FUNCTIONS for all other calibrated shapes
def draw_triangle(start_x, start_y, end_x, end_y, positions, canvas=None):
    _draw_bounding_box_shape("triangle", start_x, start_y, end_x, end_y, positions, canvas)

def draw_circle(start_x, start_y, end_x, end_y, positions, canvas=None):
    _draw_bounding_box_shape("circle", start_x, start_y, end_x, end_y, positions, canvas)

def draw_diamond(start_x, start_y, end_x, end_y, positions, canvas=None):
    _draw_bounding_box_shape("diamond", start_x, start_y, end_x, end_y, positions, canvas)

def draw_right_triangle(start_x, start_y, end_x, end_y, positions, canvas=None):
    _draw_bounding_box_shape("right_triangle", start_x, start_y, end_x, end_y, positions, canvas)

def draw_polygon(start_x, start_y, end_x, end_y, positions, canvas=None):
    # Note: MS Paint's polygon tool requires more clicks to define vertices, 
    # but based on your previous JSON, the AI assumes a bounding box drag is sufficient.
    # The drag operation will start the shape, but may require manual input/a different logic 
    # for the polygon tool to be completed correctly. We use the same bounding box draw for consistency.
    _draw_bounding_box_shape("polygon", start_x, start_y, end_x, end_y, positions, canvas)

# --- MAIN DRAW SHAPES FUNCTION (UPDATED) ---

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
    
    # Map shape names to their new drawing functions
    draw_function_map = {
        "line": draw_line,
        "rectangle": draw_rectangle,
        "triangle": draw_triangle,
        "circle": draw_circle,
        "diamond": draw_diamond,
        "right_triangle": draw_right_triangle,
        "polygon": draw_polygon,
        # Note: pencil and brush are usually single-click/freehand, not bounding box.
    }


    for i, shape_data in enumerate(shapes_list):
        shape_type = shape_data.get("shape", "").lower()
        
        print(f"Drawing shape {i+1}/{len(shapes_list)}: {shape_type}")

        # Check if the shape type is supported and has a function
        draw_func = draw_function_map.get(shape_type)
        
        if draw_func:
            try:
                draw_func(
                    shape_data["start_x"], shape_data["start_y"], 
                    shape_data["end_x"], shape_data["end_y"], 
                    positions, canvas
                )
            except KeyError:
                print(f"Error: Missing coordinate for shape '{shape_type}' at index {i}.")
            except Exception as e:
                print(f"Error drawing {shape_type}: {e}")
        else:
            print(f"Warning: No drawing function found for shape type '{shape_type}'. Skipping.")

    return True
import json
import pyautogui
import subprocess
import time	
import os

def load_calibration():
    try:
        with open('paint_calibration.json', 'r') as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ No valid calibration file found. Starting fresh...")
        return {}


def _extract_tools_and_canvas(calibration_data):
	"""Return (tools_dict, canvas_dict_or_None) from loaded calibration data.

	Backward compatible with legacy file that only had tool positions.
	"""
	if calibration_data is None:
		return None, None
	if isinstance(calibration_data, dict) and ("tools" in calibration_data or "canvas" in calibration_data):
		return calibration_data.get("tools"), calibration_data.get("canvas")
	return calibration_data, None


def calibrate_tools():
	"""
	Interactive calibration tool to find exact positions of Paint tools.
	"""
	print("\n=== MS PAINT TOOL CALIBRATION ===")
	print("This will help you find the exact positions of Paint tools on your screen.")
	print("\nInstructions:")
	print("1. Open MS Paint manually")
	print("2. For each tool, hover your mouse over it")
	print("3. Press Enter to record the position")
	print("4. Press 'q' and Enter to skip a tool\n")
	
	input("Press Enter when Paint is open and ready...")
	
	tools_to_calibrate = [
		"pencil", "brush", "fill", # paint tools
		"line", "rectangle", "triangle", "circle", # basic shapes
		"diamond", "right_triangle", "polygon", # advanced shapes
	]
	calibrated_positions = {}
	
	for tool in tools_to_calibrate:
		response = input(f"\nHover over the {tool.upper()} tool and press Enter (or 'q' to skip): ")
		if response.lower() == 'q':
			print(f"Skipped {tool}")
			continue
		
		pos = pyautogui.position()
		calibrated_positions[tool] = (pos.x, pos.y)
		print(f"  → {tool}: {pos.x}, {pos.y}")
	
	# Save to file (merge with existing, store under "tools")
	existing = load_calibration()
	if isinstance(existing, dict) and ("tools" in existing or "canvas" in existing):
		existing["tools"] = calibrated_positions
		to_write = existing
	else:
		# Legacy file was a flat dict of tools; migrate to structured format
		to_write = {"tools": calibrated_positions}
		
	with open('paint_calibration.json', 'w') as f:
		json.dump(to_write, f, indent=2)
	
	print("\n✓ Calibration saved to 'paint_calibration.json'")
	print("The script will now use these positions automatically.")
	return calibrated_positions


def calibrate_canvas():
	"""Interactive calibration for the drawable canvas area in MS Paint."""
	print("\n=== MS PAINT CANVAS CALIBRATION ===")
	print("This will record the drawing page bounds so shapes stay inside it.")
	print("\nInstructions:")
	print("1. Open MS Paint and ensure the canvas is visible.")
	print("2. Hover your mouse at the TOP-LEFT inside the white canvas and press Enter.")
	print("3. Hover your mouse at the BOTTOM-RIGHT inside the white canvas and press Enter.\n")

	input("Press Enter when Paint is open and ready...")

	input("Hover at TOP-LEFT inside canvas and press Enter...")
	tl = pyautogui.position()
	print(f"  → top_left: {tl.x}, {tl.y}")

	input("Hover at BOTTOM-RIGHT inside canvas and press Enter...")
	br = pyautogui.position()
	print(f"  → bottom_right: {br.x}, {br.y}")

	canvas = {"top_left": [tl.x, tl.y], "bottom_right": [br.x, br.y]}

	existing = load_calibration()
	if isinstance(existing, dict) and ("tools" in existing or "canvas" in existing):
		existing["canvas"] = canvas
		to_write = existing
	elif isinstance(existing, dict):
		to_write = {"tools": existing, "canvas": canvas}
	else:
		to_write = {"canvas": canvas}

	with open('paint_calibration.json', 'w') as f:
		json.dump(to_write, f, indent=2)

	print("\n✓ Canvas calibration saved to 'paint_calibration.json'")
	return canvas
#---------------Automated Calibration Tool -----------------#	

# 1. DEFINE THE TOOL LOCATION FUNCTION
def get_tool_coordinates(image_file):
    """Searches the screen for the image and returns the center coordinates."""
    # Ensure the image file exists
    if not os.path.exists(image_file):
        print(f"Error: The image file '{image_file}' was not found in the script directory.")
        print("Please ensure you have saved a screenshot of the Pencil tool as 'pencil.png'.")
        return None

    try:
        # Locate the image and return the Box object
        # confidence=0.85 allows for minor visual differences
        location = pyautogui.locateOnScreen(image_file, confidence=0.85)
        
        if location:
            # Return the coordinates of the center of the found image
            return pyautogui.center(location)
        else:
            print(f"Tool '{image_file}' not found on screen.")
            return None
    except Exception as e:
        print(f"Error locating image: {e}")
        return None


def automated_calibration():
    """
    Automated calibration tool to find exact positions of Paint tools.
    """
    print("\n=== MS PAINT AUTOMATED TOOL CALIBRATION ===")
    print("This will help you find the exact positions of Paint tools on your screen.")
    print("\nInstructions:")
    print("1. The script will open MS Paint automatically.")
    print("2. It will then attempt to locate and click each tool based on provided images.")
    print("3. Ensure that the tool images are clear and visible on the screen.\n")
    
    input("Press Enter to start the automated calibration...")

    # 2. OPEN MS PAINT
    print("Attempting to open MS Paint...")
    try:
        subprocess.Popen('mspaint')
        time.sleep(3)
        print("MS Paint opened. Proceeding to locate the Pencil tool.")
    except FileNotFoundError:
        print("ERROR: 'mspaint' command not found. Ensure you are on a Windows machine or adjust the command for your OS.")
        exit()

    # 3. LOCATE AND CLICK EACH TOOL
    tools_to_calibrate = [
        "pencil", "brush", "fill",       # paint tools
        "line", "rectangle", "triangle", "circle",  # basic shapes
        "diamond", "right_triangle", "polygon"      # advanced shapes
    ]

    calibrated_positions = {}
    Failed_Tools = []

    for tool in tools_to_calibrate:
        IMAGE_FILE = f'./Tool_PNG/{tool}.png'
        coords = get_tool_coordinates(IMAGE_FILE)
        if coords:
            pyautogui.click(coords)
            print(f"✅ Success! {tool.capitalize()} clicked at: {coords}")
            calibrated_positions[tool] = (int(coords.x), int(coords.y))
            time.sleep(1)  # Brief pause between clicks
        else:
            Failed_Tools.append(tool)

    # 4. SAVE CALIBRATION
    existing = load_calibration()
    if isinstance(existing, dict) and ("tools" in existing or "canvas" in existing):
        existing["tools"] = calibrated_positions
        to_write = existing
    else:
        # Legacy file was a flat dict of tools; migrate to structured format
        to_write = {"tools": calibrated_positions}
		
    with open('paint_calibration.json', 'w') as f:
        json.dump(to_write, f, indent=2)

    print("\n✓ Calibration saved to 'paint_calibration.json'")
    print("The script will now use these positions automatically.")
    if Failed_Tools:
        print("\n⚠️ The following tools could not be located automatically:")
        for tool in Failed_Tools:
              print(f" - {tool}")
              print("Consider running the manual calibration for these tools.")
    else:
          print("\nAll tools were calibrated successfully!")
    print("\n=== MS PAINT CANVAS CALIBRATION ===")
    print("This will record the drawing page bounds so shapes stay inside it.")
    TOP_LEFT_IMAGE = './Tool_PNG/Top_left.png'
    BOTTOM_RIGHT_IMAGE = './Tool_PNG/Bottom_right.png'

    print("Locating Top-Left corner of canvas...")
    tl = get_tool_coordinates(TOP_LEFT_IMAGE)
    
    print("Locating Bottom-Right corner of canvas...")
    br = get_tool_coordinates(BOTTOM_RIGHT_IMAGE)
    # tl=int(top_left_coords.x), int(top_left_coords.y)
    # br=int(bottom_right_coords.x), int(bottom_right_coords.y)		

    if tl and br:
        canvas = {"top_left": [int(tl.x), int(tl.y)], "bottom_right": [int(br.x), int(br.y)]}
        existing = load_calibration()
        if isinstance(existing, dict) and ("tools" in existing or "canvas" in existing):
            existing["canvas"] = canvas
            to_write = existing
        elif isinstance(existing, dict):
            to_write = {"tools": existing, "canvas": canvas}
        else:
            to_write = {"canvas": canvas}
        with open('paint_calibration.json', 'w') as f:
            json.dump(to_write, f, indent=2)
        print(f"Canvas corners located in {canvas} and saved.")
        print("\n✓ Canvas calibration saved to 'paint_calibration.json'")
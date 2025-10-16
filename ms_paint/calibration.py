import json
import pyautogui


def load_calibration():
	"""Load calibrated data (tools and optional canvas) from file."""
	try:
		with open('paint_calibration.json', 'r') as f:
			return json.load(f)
	except FileNotFoundError:
		return None


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




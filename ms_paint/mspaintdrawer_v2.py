import sys
import time

from .calibration import calibrate_tools, calibrate_canvas,automated_calibration
from .draw_shapes import draw_shapes


def ms_paint_tool(shapes):
    if sys.platform != "win32":
        print("This script only works on Windows.")
        sys.exit(1)

    print("\nThis will open MS Paint and draw shapes.")
    input("Press Enter to continue...")

    draw_shapes(shapes)


if __name__ == "__main__":
    if sys.platform != "win32":
        print("This script only works on Windows.")
        sys.exit(1)
    
    print("=== MS PAINT DRAWING TOOL ===")
    print("\nOptions:")
    print("1. Calibrate tool positions (recommended first time)")
    print("2. Calibrate canvas bounds")
    print("3. Draw test shapes")
    print("4. Automated Calibration")
    print("5. Exit")

    choice = input("\nEnter your choice (1-5): ")

    if choice == "1":
        calibrate_tools()   

    elif choice == "2":
        calibrate_canvas()

    elif choice == "3":
        test_shapes = [
            {
                "shape": "rectangle",
                "start_x": 200,
                "start_y": 300,
                "end_x": 600,
                "end_y": 500
            },
            {
                "shape": "rectangle",
                "start_x": 200,
                "start_y": 100,
                "end_x": 600,
                "end_y": 300
            },
            {
                "shape": "line",
                "start_x": 200,
                "start_y": 100,
                "end_x": 400,
                "end_y": 0
            },
            {
                "shape": "line",
                "start_x": 400,
                "start_y": 0,
                "end_x": 600,
                "end_y": 100
            },
            {
                "shape": "rectangle",
                "start_x": 250,
                "start_y": 400,
                "end_x": 350,
                "end_y": 450
            },
            {
                "shape": "rectangle",
                "start_x": 450,
                "start_y": 400,
                "end_x": 550,
                "end_y": 450
            },
            {
                "shape": "rectangle",
                "start_x": 250,
                "start_y": 150,
                "end_x": 350,
                "end_y": 200
            },
            {
                "shape": "rectangle",
                "start_x": 450,
                "start_y": 150,
                "end_x": 550,
                "end_y": 200
            },
            {
                "shape": "rectangle",
                "start_x": 350,
                "start_y": 450,
                "end_x": 450,
                "end_y": 500
            }
        ]

        print("\nThis will open MS Paint and draw shapes.")
        input("Press Enter to continue...")
        
        draw_shapes(test_shapes)
    elif choice == "4":
        automated_calibration() 



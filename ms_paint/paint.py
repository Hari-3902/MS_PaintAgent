import subprocess
import time
import pyautogui


def open_ms_paint():
    """Opens Microsoft Paint on Windows."""
    try:
        subprocess.Popen(['mspaint.exe'])
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Failed to open MS Paint: {e}")
        return False


def focus_paint_window():
    """Brings MS Paint window to focus."""
    try:
        paint_window = pyautogui.getWindowsWithTitle('Paint')
        if paint_window:
            paint_window[0].activate()
            time.sleep(0.5)
            return True
        else:
            print("Paint window not found")
            return False
    except Exception as e:
        print(f"Could not focus Paint window: {e}")
        return False


def click_tool(tool_name, positions):
    """Clicks on a specific tool in Paint."""
    if tool_name in positions:
        x, y = positions[tool_name]
        pyautogui.moveTo(x, y)
        time.sleep(0.3)
        pyautogui.click(x=x, y=y)
        time.sleep(0.3)
        return True
    return False



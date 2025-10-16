## MS Paint Agent

Draw shapes in Microsoft Paint using natural-language prompts with Google's Gemini. The agent converts your prompt into a list of shapes and automates MS Paint to draw them.

### Prerequisites
- *Windows* (required, uses MS Paint and pyautogui)
- *Python 3.9+*
- MS Paint installed and accessible as mspaint.exe

### Install
bash
pip install -r requirements.txt


### Configure API Key
Set your Gemini API key via environment variable or .env file at the repo root.

- Option A: .env file

GEMINI_API_KEY=your_api_key_here


- Option B: Environment (PowerShell)
powershell
$Env:GEMINI_API_KEY="your_api_key_here"


### First-time Calibration
You must calibrate once so the agent knows where Paint tools and canvas are on your screen. Calibration data is stored in paint_calibration.json in the project root.

Run the calibration helper as a module (ensures package-relative imports work):
bash
python -m ms_paint.mspaintdrawer_v2


You will see a menu:
- 1: Calibrate tool positions (recommended first)
- 2: Calibrate canvas bounds
- 3: Draw test shapes
- 4: Exit

#### Calibrate Tool Positions
Select option 1 and follow the prompts:
- Hover your mouse over each listed tool (e.g., line, rectangle) and press Enter to record the position.
- Press q then Enter to skip any tool you don’t use.
- This writes the tools map in paint_calibration.json.

#### Calibrate Canvas Bounds
Select option 2 and follow the prompts:
- Hover at the top-left inside the white drawing area and press Enter.
- Hover at the bottom-right inside the white drawing area and press Enter.
- This writes the canvas bounds in paint_calibration.json.

Tip: Ensure Paint is visible and not obstructed. If you use display scaling (DPI), keep it consistent between calibration and usage.

### Run the Agent
After calibration, start the main program:
bash
python main.py

Enter a natural-language prompt, e.g.:

draw a wide rectangle at the bottom and a line across the top

The model returns a list of shapes and the agent draws them in MS Paint.

### Troubleshooting
- Paint doesn’t draw: Ensure paint_calibration.json exists and includes both tools and canvas. Re-run calibration if needed.
- Wrong positions: Re-run calibration after moving toolbars, changing resolution, or DPI scaling.
- Window focus issues: The script attempts to focus Paint; if it fails, click the Paint window and retry.
- Empty model output: Confirm GEMINI_API_KEY is set and that you have network access.

### Project Structure

ms_paint_agent/
  main.py                  # Entry point: prompts and draws
  models/
    gemini.py              # Calls Gemini, parses JSON
    system_prompt.txt      # System prompt used by the model
  ms_paint/
    calibration.py         # Tool + canvas calibration utilities
    draw_shapes.py         # Shape drawing logic
    paint.py               # Paint window control helpers
    mspaintdrawer_v2.py    # CLI for calibration/tests (run with -m)
  paint_calibration.json   # Created after calibration (not committed)
  requirements.txt
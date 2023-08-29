# Dry Eye Reminder

Dry Eye Reminder is a Python script designed to help alleviate the discomfort of dry eyes caused by prolonged screen time. The script plays gentle chime sounds at regular intervals, prompting you to take breaks and look away from your screen. It also provides the option to temporarily snooze the reminders, offering flexibility while maintaining eye health. The script operates as a lightweight system tray application, allowing easy configuration and access to the reminders.

## Features

- Plays soothing chime sounds at specified intervals to remind you to take breaks and rest your eyes.
- Configurable reminder interval and chime volume.
- Option to temporarily snooze the reminders using a custom shortcut.
- Runs unobtrusively in the system tray for seamless integration with your workflow.

## Prerequisites

- Python (3.7+ recommended)
- Required Python packages (install using `pip`):
  - `win10toast`
  - `keyboard`
  - `pygame`
  - `pystray`
  - `PIL`

## Usage

1. Clone or download this repository to your local machine.

2. Install the required Python packages:

   ```bash
   pip install win10toast keyboard pygame pystray pillow
   ```

3. Run the script or compile it to an exe:
   
    ```bash
   # To run it as a script
    python script.py

    # To compile into an exe using PyInstaller. The .exe can be found in the dist directory that was created
    pyinstaller script.spec
   ```
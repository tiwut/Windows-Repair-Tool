# Windows Repair Tool

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

A user-friendly graphical tool built with Python and Tkinter to simplify common Windows repair tasks. This application provides an intuitive interface to execute essential system maintenance commands like `SFC` and `DISM` without needing to open the command prompt.

It's designed for users who want a simple, one-click solution to diagnose and fix common Windows stability issues.

![Screenshot of the Windows Repair Tool](https://i.imgur.com/your-screenshot-url.png)
*(Note: You should replace the link above with an actual screenshot of your application)*

## Features

- **Simple Graphical Interface:** No complex commands to remember. Just click a button.
- **System File Checker:** Integrates `sfc /scannow` to scan and repair corrupt system files.
- **DISM Health Check:** Runs `DISM /Online /Cleanup-Image /ScanHealth` to check for component store corruption.
- **DISM Health Restore:** Runs `DISM /Online /Cleanup-Image /RestoreHealth` to automatically repair the Windows image.
- **Real-time Output:** A console-like text area displays the live output from the commands, so you can see exactly what's happening.
- **Progress Monitoring:** A dynamic progress bar shows the completion percentage for `SFC` and `DISM` commands.
- **Estimated Time Remaining:** Calculates and displays an estimated time until the current process is complete.
- **Automatic Admin Elevation:** The tool automatically prompts for administrator privileges (UAC) on launch, which is required for all repair tasks.

## Installation

### Via Tiwut Launcher (Recommended)

This application is designed for easy installation through the Tiwut Launcher.

1.  Open the **Tiwut Launcher**.
2.  Navigate to the **"System Utilities"** or **"Tools"** library.
3.  Find **"Windows Repair Tool"** in the list and click **"Install"**.
4.  The launcher will handle the download and setup. You can then launch the tool directly from your app library.

### Manual Installation

If you don't use the Tiwut Launcher, you can download a pre-compiled executable.

1.  Go to the [**Releases**](https://github.com/your-username/your-repo/releases) page of this repository.
2.  Download the latest `Windows_Repair_Tool.exe` file from the assets.
3.  Place the executable anywhere on your computer (e.g., your Desktop) and run it. No installation is required.

## Usage

1.  Launch the application from the Tiwut Launcher or by double-clicking the `.py` or `.exe` file.
2.  A **UAC (User Account Control)** prompt will appear requesting administrator privileges. This is necessary for the repair commands to function correctly. Click **"Yes"**.
3.  The main application window will appear.
4.  Click on the desired repair function button to start the process.
    - The buttons will be disabled while a task is running.
5.  Monitor the progress bar, estimated time, and real-time output in the main window.
6.  Wait for the command to complete. The buttons will become active again when the process is finished and the status returns to "Idle".

## Building from Source

If you prefer to run the script directly, you can build it from the source code.

### Prerequisites

- [Python 3.x](https://www.python.org/downloads/)

### Instructions

1.  Clone the repository:
    ```sh
    git clone https://github.com/your-username/your-repo.git
    ```
2.  Navigate to the project directory:
    ```sh
    cd your-repo
    ```
3.  Run the Python script:
    ```sh
    python "Windows Repair Tool.py"
    ```

## How It Works

- **GUI:** The graphical interface is built using Python's standard `tkinter` library.
- **Admin Elevation:** The script uses the `ctypes` library to interact with the Windows API. It checks if it has admin rights and, if not, re-launches itself via `ShellExecuteW` with the `runas` verb to trigger the UAC prompt.
- **Responsiveness:** Repair commands can take a long time. To prevent the GUI from freezing, each command is executed in a separate background thread using the `threading` module.
- **Thread Communication:** A `queue` is used to safely pass messages (like output lines and progress updates) from the background worker thread to the main GUI thread for display.

## Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, please feel free to:
1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourAmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/YourAmazingFeature`).
5.  Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

# Zoom Triad Tool

A utility for creating multiple Zoom meeting participants for testing and demonstration purposes. This tool allows you to quickly join a Zoom meeting with several simulated participants using browser-based Zoom clients.

## Features

- Join Zoom meetings with multiple simulated participants
- Each participant gets a random name with a prefix (DE, DE/EN, EN, NT)
- Optimized to use minimal system resources
- Automatically attempts to stop incoming video to reduce bandwidth usage
- Cross-platform: works on Windows, macOS, and Linux

## Requirements

No manual installation required. The tool's launcher scripts will automatically download and install all dependencies using Robocorp RCC.

## Installation & Usage

### Windows

1. Download the `Start_Triad_Tool_Windows.bat` file
2. Double-click to run the file
3. The tool will automatically download and set up its environment
4. Once launched, enter the Zoom meeting link and the number of participants
5. Click "Start" to begin

### macOS

1. Download the `Start_Triad_Tool_Mac.sh` file
2. Open Terminal and navigate to where you saved the file
3. Make the script executable:
   ```
   chmod +x Start_Triad_Tool_Mac.sh
   ```
4. Run the script:
   ```
   ./Start_Triad_Tool_Mac.sh
   ```
5. Once launched, enter the Zoom meeting link and the number of participants
6. Click "Start" to begin

### Linux

1. Download the `Start_Triad_Tool_Linux.sh` file
2. Open a Terminal and navigate to where you saved the file
3. Make the script executable:
   ```
   chmod +x Start_Triad_Tool_Linux.sh
   ```
4. Run the script:
   ```
   ./Start_Triad_Tool_Linux.sh
   ```
5. Once launched, enter the Zoom meeting link and the number of participants
6. Click "Start" to begin

## How It Works

The tool uses:
- Flet for the user interface
- Playwright for browser automation
- Headless Chromium browsers to join the Zoom meetings
- Robocorp's RCC to manage isolated environments and dependencies

## Tips

- For best performance, limit the number of participants to what your system can handle
- A warning will be displayed if you try to create more than 10 participants
- You can stop all participants at any time by clicking the "Stop" button
- The tool converts regular Zoom links to web client links automatically

## Troubleshooting

If you encounter issues:

1. Ensure you have a stable internet connection
2. Verify that the Zoom meeting link is valid
3. Try with a smaller number of participants
4. If the tool doesn't start, make sure you have permission to run scripts

## Technical Details

- Built with Python 3.10
- Uses a conda environment managed by RCC
- Includes automatic installation of Playwright and Chromium
- Browser instances run in headless mode to save resources
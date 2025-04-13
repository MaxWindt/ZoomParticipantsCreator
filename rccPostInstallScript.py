import os
import platform
import subprocess
import sys


def set_playwright_browsers_path(custom_path):
    """Sets the PLAYWRIGHT_BROWSERS_PATH environment variable based on OS"""
    # Detect the operating system
    system = platform.system()

    if system == "Windows":
        # Set environment variable for Windows
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = custom_path
        print(f"Set PLAYWRIGHT_BROWSERS_PATH to {custom_path} on Windows")
    elif system == "Darwin":  # macOS is identified as "Darwin"
        # Set environment variable for macOS
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = custom_path
        print(f"Set PLAYWRIGHT_BROWSERS_PATH to {custom_path} on macOS")
    else:
        print(f"Unsupported OS: {system}")
        return False
    return True


def install_chromium():
    """Runs the playwright install chromium command"""
    try:
        subprocess.run(
            ["python", "-m", "playwright", "install", "chromium"], check=True
        )
        print("Chromium installation successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during Chromium installation: {e}")


if __name__ == "__main__":
    # Get the directory where the current Python executable is located
    python_executable_dir = os.path.dirname(sys.executable)

    # Set custom_browser_path to the folder containing the python executable
    custom_browser_path = python_executable_dir
    # Set the environment variable
    if set_playwright_browsers_path(custom_browser_path):
        # Run the Playwright install command for Chromium
        install_chromium()

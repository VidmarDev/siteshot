# SITESHOT

## Overview
SITESHOT is a tool designed for capturing screenshots of websites effortlessly.

## Quick Start

### Download
Download the executable.

### Prepare Input:
Create a file named `domains.txt` in the same directory as the executable file. List the web addresses you want to capture, with one address per line.

### Run the Executable:
Double-click on the downloaded executable file to run the script. The tool will capture screenshots of the websites listed in `domains.txt`.

### View Results:
Screenshots will be saved in a folder named `screenshots` in the same directory as the executable file.

## Important Notes
- **domains.txt:** Ensure that the file `domains.txt` exists in the same directory as the executable file and contains the list of web addresses you want to capture.

- **chromedriver:** The tool uses Chrome WebDriver for capturing screenshots. Make sure the executable file `chromedriver` is available in the same directory as the main executable. You can download it [here](https://sites.google.com/chromium.org/driver/downloads?authuser=0) or [here](https://googlechromelabs.github.io/chrome-for-testing/#beta).

- **Antivirus Warning:** Some antivirus programs may flag the executable file due to its nature. If you encounter issues, consider adding an exception for this tool.

## Customization
### Specify Parameters for Screenshot Capture

In the `settings.txt` file, you can customize various parameters for the screenshot capture.

- **Capture Size:** Set the desired window size for capturing screenshots. Common values include "1920x1080" (Full HD), "1366x768" (Common laptop resolution), or "750x1334" (iPhone 7 screen size).
  ```ini
  capture_size = 1920x1080
  ```

- **Image Save Type:** Specify the image format for saving screenshots, such as "png" or "jpg".
  ```ini
  image_save_type = png
  ```

- **Output Folder:** Define the folder where screenshots will be saved.
  ```ini
  output_folder = screenshots
  ```

- **Waiting Time:** Set the time to wait (in seconds) after the page has loaded before capturing the screenshot.
  ```ini
  waiting_time = 5
  ```

- **Filename Format:** Customize the filename format using placeholders such as {domain}, {timestamp}, {capture_size}, and {image_save_type}.
  ```ini
  filename_format = {domain}_{capture_size}
  ```

Feel free to adjust these settings based on your specific requirements.

import os
import logging
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configparser import ConfigParser

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)


def configure_webdriver(capture_size):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument(f"--window-size={capture_size}")
    return webdriver.Chrome(options=options)


def read_settings():
    config = ConfigParser()
    config_file_path = os.path.join(os.getcwd(), 'settings.txt')

    if not os.path.exists(config_file_path):
        logging.error("Settings file not found.")
        return None

    config.read(config_file_path)

    capture_size = config.get('Settings', 'capture_size', fallback='1920x1080')
    image_save_type = config.get('Settings', 'image_save_type', fallback='png')
    output_folder = config.get('Settings', 'output_folder', fallback='screenshots')
    waiting_time = config.getint('Settings', 'waiting_time', fallback=10)
    filename_format = config.get('Settings', 'filename_format', fallback='{domain}_{timestamp}.{image_save_type}')

    return capture_size, image_save_type, output_folder, waiting_time, filename_format


def add_protocol_if_missing(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return f"http://{url}"
    return url


def take_screenshot(url, output_folder, capture_size="1920x1080", image_save_type="png", waiting_time=10, filename_format="{domain}_{capture_size}_{timestamp}_{image_save_type}"):
    with configure_webdriver(capture_size) as driver:
        try:
            url_with_protocol = add_protocol_if_missing(url)
            driver.get(url_with_protocol)

            domain = url.split("//")[-1].split("/")[0].split('?')[0].replace("www.", "")

            # Format timestamp as a string with Swedish format
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

            filename = filename_format.format(domain=domain, capture_size=capture_size, timestamp=timestamp, image_save_type=image_save_type)

            # Ensure image_save_type is always appended to the filename
            if not filename.endswith(f".{image_save_type}"):
                filename += f".{image_save_type}"

            screenshot_path = os.path.join(output_folder, filename)

            # Skip if screenshot already exists
            if os.path.exists(screenshot_path):
                logging.info(f"Screenshot already exists for {url}. Skipping.")
                return

            # Add a sleep to wait for JavaScript execution
            time.sleep(waiting_time)

            driver.save_screenshot(screenshot_path)
            logging.info(f"Screenshot saved for {url} with capture size {capture_size}")
        except (WebDriverException, Exception) as e:
            logging.error(f"Error capturing screenshot for {url}: {str(e)}")


def main():
    # Read settings from the settings file
    settings = read_settings()

    if settings is None:
        return  # Stop execution if settings are not available

    capture_size, image_save_type, output_folder, waiting_time, filename_format = settings

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_file = "domains.txt"

    with open(input_file, "r") as file:
        domains = [line.strip() for line in file if line.strip()]

    for domain in domains:
        take_screenshot(
            domain,
            output_folder,
            capture_size=capture_size,
            image_save_type=image_save_type,
            waiting_time=waiting_time,
            filename_format=filename_format
        )


if __name__ == "__main__":
    main()

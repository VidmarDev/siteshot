import os
import logging
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from configparser import ConfigParser

# Add common user screen sizes as a constant
COMMON_SCREEN_SIZES = {
    "mobile": "360x640",
    "tablet": "768x1024",
    "laptop": "1366x768",
    "desktop": "1920x1080"
}

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
    fullscreen_screenshot = config.getboolean('Settings', 'fullscreen_screenshot', fallback=False)
    create_base_folders = config.getboolean('Settings', 'create_base_folders', fallback=False)

    return capture_size, image_save_type, output_folder, waiting_time, filename_format, fullscreen_screenshot, create_base_folders

def add_protocol_if_missing(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return f"http://{url}"
    return url

def take_screenshot(url, output_folder, capture_size="1920x1080", image_save_type="png", waiting_time=10, filename_format="{domain}_{timestamp}_{label}_{capture_size}.{image_save_type}", fullscreen_screenshot=False, create_base_folders=False):
    with configure_webdriver(capture_size) as driver:
        try:
            url_with_protocol = add_protocol_if_missing(url)
            parsed_url = urlparse(url_with_protocol)
            domain = parsed_url.netloc.replace("www.", "")
            path = parsed_url.path.strip("/").replace('/', '_')

            if path:
                domain_path = f"{domain}_{path}"
            else:
                domain_path = domain

            driver.get(url_with_protocol)
            time.sleep(waiting_time)  # Wait for the page to load
            
            # This step is only necessary if fullscreen_screenshot is enabled
            if fullscreen_screenshot:
                full_width = driver.execute_script("return document.body.scrollWidth")
                full_height = driver.execute_script("return document.body.scrollHeight")
            
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            
            domain_folder = os.path.join(output_folder, domain_path) if create_base_folders else output_folder

            if create_base_folders and not os.path.exists(domain_folder):
                os.makedirs(domain_folder)
            
            if create_base_folders:
                # Capture screenshots for COMMON_SCREEN_SIZES
                for label, size in COMMON_SCREEN_SIZES.items():
                    width, height = map(int, size.split('x'))
                    driver.set_window_size(full_width, full_height) if fullscreen_screenshot else driver.set_window_size(width, height)
                    time.sleep(waiting_time)
                    
                    formatted_filename = filename_format.format(
                        domain=domain_path,
                        timestamp=timestamp,
                        label=label,
                        capture_size=size.replace('x', 'x') + ("_fullscreen" if fullscreen_screenshot else ""),
                        image_save_type=image_save_type
                    )
                    screenshot_path = os.path.join(domain_folder, formatted_filename)
                    if not screenshot_path.endswith(f".{image_save_type}"):
                        screenshot_path += f".{image_save_type}"
                    driver.save_screenshot(screenshot_path)
                    logging.info(f"Screenshot saved for {url_with_protocol} at size {size} in {screenshot_path}")
            else:
                # Capture a single screenshot at the specified size or full page size
                capture_width, capture_height = map(int, capture_size.split('x'))
                size_label = "custom"
                driver.set_window_size(full_width, full_height) if fullscreen_screenshot else driver.set_window_size(capture_width, capture_height)
                formatted_filename = filename_format.format(
                    domain=domain_path,
                    timestamp=timestamp,
                    label=size_label + ("_fullscreen" if fullscreen_screenshot else ""),
                    capture_size=capture_size if not fullscreen_screenshot else "fullscreen",
                    image_save_type=image_save_type
                )
                screenshot_path = os.path.join(domain_folder, formatted_filename)
                if not screenshot_path.endswith(f".{image_save_type}"):
                    screenshot_path += f".{image_save_type}"
                driver.save_screenshot(screenshot_path)
                logging.info(f"Screenshot saved for {url_with_protocol} with capture size {capture_size} in {screenshot_path}")

        except (WebDriverException, Exception) as e:
            logging.error(f"Error capturing screenshot for {url}: {str(e)}")
			
def main():
    settings = read_settings()

    if settings is None:
        return

    capture_size, image_save_type, output_folder, waiting_time, filename_format, fullscreen_screenshot, create_base_folders = settings

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
            filename_format=filename_format,
            fullscreen_screenshot=fullscreen_screenshot,
            create_base_folders=create_base_folders
        )

if __name__ == "__main__":
    main()
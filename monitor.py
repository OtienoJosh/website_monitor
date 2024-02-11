import requests
import time
import os
from selenium import webdriver

def measure_website_info(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        response_time = end_time - start_time
        status_code = response.status_code
        content_length = len(response.content)
        headers = response.headers
        html_content = response.content.decode('utf-8')  # Decode content from bytes to string
        return response_time, status_code, content_length, headers, html_content
    except requests.ConnectionError:
        print(f"Connection error: Unable to reach the website '{url}'")
        return None, None, None, None, None

def take_screenshot(url, output_dir, filename):
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # Run Chrome in headless mode (without opening browser window)
    driver = webdriver.Chrome(options=options)
    
    try:
        # Load the URL
        driver.get(url)
        
        # Wait for the page to fully load (you may need to adjust the wait time)
        time.sleep(2)
        
        # Take screenshot and save to file
        screenshot_path = os.path.join(output_dir, filename)
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
    finally:
        # Quit the WebDriver
        driver.quit()

def monitor_website_performance(url, num_measurements, output_dir):
    response_times = []
    status_codes = []
    content_lengths = []
    html_contents = []  # List to store HTML contents
    for i in range(num_measurements):
        response_time, status_code, content_length, _, html_content = measure_website_info(url)
        if response_time is not None:
            response_times.append(response_time)
            status_codes.append(status_code)
            content_lengths.append(content_length)
            html_contents.append(html_content)
            print(f"Measurement {i + 1}: Response time: {response_time:.2f} seconds | Status code: {status_code} | Content length: {content_length}")
            # Write HTML content to file
            output_file = os.path.join(output_dir, f"measurement_{i + 1}.html")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            # Take screenshot
            screenshot_filename = f"screenshot_{i + 1}.png"
            take_screenshot(url, output_dir, screenshot_filename)
        time.sleep(1)  # Wait for 1 second between measurements
    return response_times, status_codes, content_lengths

if __name__ == "__main__":
    website_url = 'https://www.bikini.com'
    num_measurements = 3  # Number of measurements to take
    output_directory = 'website_data'  # Output directory to save HTML content files

    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    response_times, status_codes, content_lengths = monitor_website_performance(website_url, num_measurements, output_directory)

    print("\nWebsite performance monitoring completed.")

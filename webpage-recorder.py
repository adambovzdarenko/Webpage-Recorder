import requests
import time
import hashlib
import os
from datetime import datetime
from bs4 import BeautifulSoup

def get_webpage_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

def save_html_and_css(content, url, folder):
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    html_filename = os.path.join(folder, f"{timestamp}.html")
    css_folder = os.path.join(folder, "css")

    if not os.path.exists(css_folder):
        os.makedirs(css_folder)

    # Parse HTML and save CSS files
    soup = BeautifulSoup(content, "html.parser")
    for link in soup.find_all("link", rel="stylesheet"):
        css_url = link.get("href")
        if css_url:
            if not css_url.startswith("http"):
                css_url = requests.compat.urljoin(url, css_url)
            try:
                css_response = requests.get(css_url)
                css_response.raise_for_status()
                css_filename = os.path.join(css_folder, os.path.basename(css_url))
                with open(css_filename, "w", encoding="utf-8") as css_file:
                    css_file.write(css_response.text)
                print(f"Saved CSS: {css_filename}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch CSS from {css_url}: {e}")

    # Save HTML file
    with open(html_filename, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Saved HTML as: {html_filename}")

def monitor_webpage(url, folder, interval):
    if not os.path.exists(folder):
        os.makedirs(folder)

    previous_hash = None
    while True:
        print("Fetching webpage...")
        content = get_webpage_content(url)
        if content is None:
            print("Failed to fetch the webpage. Retrying in 10 seconds...")
            time.sleep(10)
            continue

        current_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()

        if current_hash != previous_hash:
            print("Change detected! Saving new version...")
            save_html_and_css(content, url, folder)
            previous_hash = current_hash
        else:
            print("No changes detected.")

        time.sleep(interval)

if __name__ == "__main__":
    url = input("Enter the URL of the webpage to monitor: ")
    folder = input("Enter the folder to save HTML and CSS files: ")
    interval = int(input("Enter the time interval between checks (in seconds): "))

    print("Starting webpage monitor...")
    monitor_webpage(url, folder, interval)


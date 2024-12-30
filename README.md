# Webpage Recorder

A Python script that monitors a webpage for changes, records the HTML content, and downloads related CSS files when a change is detected. The script compares the current page content with the previous version using a hash and saves a new version if any differences are found.

## Features

- Fetches the webpage's HTML content and checks for changes.
- Downloads CSS files associated with the webpage.
- Saves the HTML and CSS files with timestamps to a specified folder.
- Periodically checks the webpage at a configurable time interval.
- Creates a unique hash of the webpage content to detect changes.

## Requirements

Before running the script, ensure you have the following Python packages installed:

- `requests` — For making HTTP requests.
- `beautifulsoup4` — For parsing HTML and extracting CSS links.

You can install the required packages with pip:

```bash
pip install requests beautifulsoup4

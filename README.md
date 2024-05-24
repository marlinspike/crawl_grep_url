# CrawlGrepURL

CrawlGrepURL is a Python application that takes a root URL, extracts all links on that page, and creates a single Markdown file with the contents of every link appended to it. The app is designed to work with dynamic web content using Selenium and Docker.

## Features

- Takes a root URL and an optional output filename as parameters.
- Extracts all URLs from the root page.
- Fetches the content of each URL and appends it to a Markdown file.
- Outputs the Markdown file to a specified folder.
- Uses Selenium to handle dynamic web content.
- Uses Docker to run Selenium in a headless Chrome browser.

## Requirements

- Python 3.6 or higher
- Docker
- The following Python packages:
  - `requests`
  - `beautifulsoup4`
  - `selenium`
  - `webdriver-manager`
  - `rich`

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/CrawlGrepURL.git
   cd CrawlGrepURL

## Install the required Python packages
```pip install -r requirements.txt```

## Install the Selenium Standalone Chrome Docker Image
```docker pull seleniarm/standalone-chromium:latest```

This lets you run Selenium tests in a headless Chrome browser. I'll be using Port 4444 to connect to the Selenium server.

### Run the Docker Image
```docker run -d -p 4444:4444 --name selenium-chrome seleniarm/standalone-chromium:latest```

This command runs the Selenium server in a Docker container and exposes port 4444.

## Usage
```python app.py -u <root_url> [-o <output_filename>] [-f <output_folder>]```

Arguments
-u, --url: The root URL to start scraping from (required).
-o, --output: Optional output filename.
-f, --folder: Output folder (default is "processed").

# Example
```python app.py -u https://osc.github.io/ood-documentation/latest/index.html```


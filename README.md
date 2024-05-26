# CrawlGrepURL

CrawlGrepURL is a Python application that takes a root URL, extracts all links on that page, and creates a single Markdown file with the contents of every link appended to it. The app is designed to work with dynamic web content using Selenium in a Docker container. This is a great setup because you can run the app on any machine without worrying about browser compatibility or other fiddly stuff.

## Features

- Takes a root URL and an optional output filename as parameters.
- Extracts all URLs from the root page.
- Fetches the content of each URL and appends it to a Markdown file.
- Outputs the Markdown file to a specified folder.
- Uses Selenium to handle dynamic web content.
- Uses Docker to run Selenium in a headless Chrome browser.

## Requirements

- Python 3.10+
- Docker
- The following Python packages:
  - `selenium`
  - `rich`

## Installation

1. **Clone the repository**:

## Install the required Python packages
```pip install -r requirements.txt```

## Install the Selenium Standalone Chrome Docker Image
```docker pull seleniarm/standalone-chromium:latest```

This lets you run Selenium tests in a headless Chrome browser. I'll be using Port 4444 to connect to the Selenium server.

**Note:** That's the container image to use for Apple Silicon. If you're using Linux, you'd use:
```docker pull selenium/standalone-chrome:latest```

### Run the Docker Image
```docker run -d -p 4444:4444 --name selenium-chrome seleniarm/standalone-chromium:latest```

This command runs the Selenium server in a Docker container and exposes port 4444.

**Note:** If you're on Linux, use the corresponding container image:
```docker run -d -p 4444:4444 --name selenium-chrome selenium/standalone-chrome:latest```

## Usage
```python app.py -u <root_url> [-o <output_filename>] [-f <output_folder>]```

Arguments
-u, --url: The root URL to start scraping from (required).
-o, --output: Optional output filename.
-f, --folder: Output folder (default is "processed").

# Example
```python app.py -u https://osc.github.io/ood-documentation/latest```


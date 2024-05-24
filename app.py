import os
import re
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from rich.console import Console
from rich.progress import track
from typing import List, Optional

console = Console()

def get_all_links(driver: webdriver.Remote, root_url: str) -> List[str]:
    driver.get(root_url)
    elements = driver.find_elements(By.TAG_NAME, 'a')
    links = []
    for element in elements:
        url = element.get_attribute('href')
        if url and not url.startswith('javascript:'):
            if not url.startswith('http'):
                url = os.path.join(root_url, url)
            links.append(url)
    return links

def fetch_text_content(driver: webdriver.Remote, url: str) -> str:
    driver.get(url)
    body = driver.find_element(By.TAG_NAME, 'body')
    return body.text

def scrape_to_string(root_url: str) -> str:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')

    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )

    console.print(f"[bold]Top level URL being parsed:[/bold] {root_url}")
    
    links = get_all_links(driver, root_url)
    total_links = len(links)
    console.print(f"[bold]Total links that will be traversed:[/bold] {total_links}")

    start_time = time.time()

    markdown_content = f"# Root URL: {root_url}\n\n"
    for link in track(links, description="Crawling links"):
        link_start_time = time.time()
        console.print(f"[blue]Current link being crawled:[/blue] {link}")
        text_content = fetch_text_content(driver, link)
        markdown_content += f"## {link}\n"
        markdown_content += text_content
        markdown_content += "\n\n"
        link_duration = (time.time() - link_start_time) * 1000  # Time in ms
        console.print(f"[green]✓[/green] [bold]{link}[/bold] [dim]({link_duration:.2f} ms)[/dim]")

    driver.quit()

    total_duration = (time.time() - start_time) * 1000
    console.print(f"[bold]Total time taken:[/bold] {total_duration:.2f} ms")
    return markdown_content

def create_markdown_file(root_url: str, output_filename: Optional[str] = None, output_folder: str = 'processed') -> None:
    if output_filename is None:
        url_part = re.sub(r'https?://', '', root_url).split('/')[0]
        timestamp = datetime.now().strftime('%Y-%m-%d')
        output_filename = f"{timestamp}_{url_part}.md"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_path = os.path.join(output_folder, output_filename)

    markdown_content = scrape_to_string(root_url)

    with open(output_path, 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_content)

    file_size_kb = os.path.getsize(output_path) / 1024
    console.print(f"[bold]Output file length:[/bold] {file_size_kb:.2f} KB")
    console.print(f"Markdown file created: [bold]{output_path}[/bold]")

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description='Create a Markdown file from the text content of all links on a given webpage.')
    parser.add_argument('-u', '--url', type=str, required=True, help='The root URL to start scraping from')
    parser.add_argument('-o', '--output', type=str, help='Optional output filename')
    parser.add_argument('-f', '--folder', type=str, default='processed', help='Output folder (default is "processed")')

    args = parser.parse_args()

    create_markdown_file(args.url, args.output, args.folder)

if __name__ == "__main__":
    main()

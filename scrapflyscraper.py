from crewai.tools import BaseTool
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os

load_dotenv()
key = os.getenv("SCRAPE_KEY")

class WebScraper(BaseTool):
    name: str = "scrapfly content extractor"
    description: str = "Extract all visible, readable text from a web page using Scrapfly."

    def _run(self, url: str) -> str:
        # Compose the Scrapfly API URL
        api_url = f"https://api.scrapfly.io/scrape?url={url}&country=us&render_js=true&key={key}"
        response = requests.get(api_url)
        data = response.json()
        html = data.get('result', {}).get('content', '')

        soup = BeautifulSoup(html, 'html.parser')

        # Remove script, style, and other non-visible elements
        for tag in soup(['script', 'style', 'noscript', 'header', 'footer', 'svg', 'form', 'nav', 'meta', 'link']):
            tag.decompose()

        # Get all visible text
        text = soup.get_text(separator='\n', strip=True)

        # Clean up excessive blank lines
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = '\n'.join(lines)

        return clean_text
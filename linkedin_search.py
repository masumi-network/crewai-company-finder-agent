from crewai.tools import BaseTool
from dotenv import load_dotenv
import http.client
import json

load_dotenv()

class LinkedinSearch(BaseTool):
    name: str = "contact finder"
    description: str = "Search the the prompt for a list of companies"

    def _run(self, domain: str) -> list[dict]:

        conn = http.client.HTTPSConnection("google.serper.dev")

      
        payload = json.dumps({
        "q": f"{domain} site:linkedin.com",
        "num": 1})

        headers = {
        'X-API-KEY': '957d5b2a0d43ede679fda0c75794b2acbf707f31',
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()


        result = json.loads(data.decode("utf-8"))
        links = [item['link'] for item in result.get("organic", [])]

        return links

        """
        tool = SerperDevTool(
            location = country,
            n_results= 100,
        )

        


        search_query =f"{url} (\"About Us\" OR \"Our Company\" OR \"Contact Us\" ) site:*.com -site:forbes.com -site:nytimes.com -site:mckinsey.com -site:cnn.com -site:medium.com -site:linkedin.com -site:twitter.com -site:facebook.com -site:youtube.com -site:reddit.com -site:quora.com -inurl:blog -inurl:article -inurl:insights"

        result = tool.run(search_query=search_query)
        return result
        """
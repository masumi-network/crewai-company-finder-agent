from crewai.tools import BaseTool
from dotenv import load_dotenv
from crewai_tools import SerperDevTool

load_dotenv()

class Scraper(BaseTool):
    name: str = "contact finder"
    description: str = "Search the the prompt for a list of companies"

    def _run(self, url: str,country: str,domain_list:list) -> list[dict]:
        tool = SerperDevTool(
            location = country,
            n_results= 100,
        )

        domains = ""
        for domain in domain_list:
            domains += str(domain)
            if domain != domain_list[-1]:
                domains += " OR "


        search_query =f"{url} site:*{domains} -site:linkedin.com -site:twitter.com -site:facebook.com -site:youtube.com \"About Us\" OR \"Our Company\" OR \"Solutions\""

        result = tool.run(search_query=search_query)
        companies = []
        for entry in result.get('organic', []):
            name = entry.get('title', '')
            url = entry.get('link', '')
            # Try to find contact info in sitelinks or snippet
            contact = ''
            if 'sitelinks' in entry:
                for sitelink in entry['sitelinks']:
                    if 'contact' in sitelink['title'].lower():
                        contact = sitelink['link']
                        break
            if not contact and 'contact' in entry.get('snippet', '').lower():
                contact = entry['link']
            companies.append({
                'Company': name,
                'URL': url,
                'Contact': contact
            })
        return companies

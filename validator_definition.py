from crewai import Agent, Crew, Task
from logging_config import get_logger
import pandas as pd
from typing import Generator, Type
from crewai_tools import ScrapeWebsiteTool
from pydantic import BaseModel
from scrapflyscraper import WebScraper
from scrapertool import Scraper



class result(BaseModel):
    result: str

class ValidatorCrew():
    def __init__(self,verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.crew = self.create_crew()
        self.logger.info("ResearchCrew initialized")

    def create_crew(self):
        self.logger.info("Creating research crew with agents")

        validator = Agent(
            role='Contact Validator',
            goal='Read the list of urls from a given context, scrape them and find return the names of each company from their website',
            backstory='Expert at finding company names from urls, ensuring that the real name is returned should the url redirect to a different company name than what was in the url',
            verbose=self.verbose
        )

        self.logger.info("Created research and writer agents")

        crew = Crew(
            agents=[validator],
            tasks=[
                Task(
                    description="""Read {text} use tools to scrape the url and return the root domain name of the company from the website ONLY if it's a company, if it is a blog or news website, skip over it and do not return anything """,
                    expected_output= """The Top-level (.io,.com etc) and second-level domain name of the company from the scraped website. ONLY if it isnt a blog, news, survey or article website. the result MUST be a domain, COMPANY.io for example, it cannot be COMPANY by itself. This is imperitive for differentiating same-name companies""",
                    agent=validator,
                    tools=[WebScraper()],
                    output_pydantic = result
                )
            ]
        )
        self.logger.info("Crew setup completed")
        return crew
    

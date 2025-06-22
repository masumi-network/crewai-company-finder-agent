from crewai import Agent, Crew, Task
from logging_config import get_logger
import pandas as pd
from typing import Generator, Type
from crewai_tools import ScrapeWebsiteTool
from pydantic import BaseModel
from scrapertool import Scraper
from scrapflyscraper import ScrapflyScraper

class result(BaseModel):
    result: str

class ResearchCrew():
    def __init__(self,verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.crew = self.create_crew()
        self.logger.info("ResearchCrew initialized")

    def create_crew(self):
        self.logger.info("Creating research crew with agents")
        
        companyFinder = Agent(
            role='Company Finder',
            goal='Read the prompt from the input and use tools to make a list of companies that appear',
            backstory='Expert at searching for relevant companies and compiling them into a list',
            verbose=self.verbose
        )

        validator = Agent(
            role='Contact Validator',
            goal='Read the list of urls from a given context, scrape them and find return the names of each company from their website',
            backstory='Expert at finding company names from urls, ensuring that the real name is returned should the url redirect to a different company name than what was in the url',
            verbose=self.verbose
        )

        self.logger.info("Created research and writer agents")

        crew = Crew(
            agents=[companyFinder,validator],
            tasks=[
                Task(
                    description="""read {text} and use that as the input for the contact finder tool and return the result. 
                                    If there is a country in the input, use that as the search tools country variable as a two letter word. 
                                    EXAMPLE: France -> "fr", Poland -> "pl", if none are provided, use the default of "us"(united states)
                                    If there are any domains in the input (.com, .io, .ie, etc.) then add them to a list and use that in the tool's 'domain' argument, if none are present then default to .com
                                    For the url argument, get the one word TYPE of company requested, e.g. "Companies in Photography" -> url = "Photography" """,
                    expected_output= """"The result of the tool output""",
                    agent=companyFinder,
                    tools=[Scraper()]
                ),

                Task(
                    description="""Read a list of company URLS from a given context, use tools to scrape them and return the names of each company""",
                    expected_output= """"The names of each company from the tool output""",
                    agent=companyFinder,
                    tools=[ScrapflyScraper()],
                    output_pydantic = result
                )
            ]
        )
        self.logger.info("Crew setup completed")
        return crew
    

from crewai import Agent, Crew, Task
from logging_config import get_logger
import pandas as pd
from typing import Generator, Type
from crewai_tools import ScrapeWebsiteTool
from pydantic import BaseModel
from scrapertool import Scraper

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

        self.logger.info("Created research and writer agents")

        crew = Crew(
            agents=[companyFinder],
            tasks=[
                Task(
                    description="""read {text} and use that as the input for the contact finder tool, analyze the result and get ONLY the list of companies and their URLS, nothing else. 
                                    If there is a country in the input, use that as the search tools country variable as a two letter word. 
                                    EXAMPLE: France -> "fr", Poland -> "pl", if none are provided, use the default of "us"(united states)
                                    If there are any domains in the input (.com, .io, .ie, etc.) then add them to a list and use that in the tool's 'domain' argument, if none are present then default to .com
                                    For the url argument, get the one word TYPE of company requested, e.g. "Companies in Photography" -> url = "Photography" """,
                    expected_output= """"a list of all companies found in the result and their URLS based on the country (if any) in the input and domain (if any), ignoring all other data. ensure to get ALL companies listed, the output must contain EVERY company, it cannot be shortened.
                                        in terms of the URLS, get only the company's base url, not any sub pages. ALSO get an X handles of the companies.
                                        If none can be found, assume it is the company name.
                                        if any other contact can be found (gmail, etc) then add that aswell

                                        return everything in a CSV format, with fields for the company name, their website, x handle and other contact
                                        
                                        following these guidelines without exception:

                                            -every single company must be read and returned in the final output.
                                            -Every company must be DISPLAYED in the final output.
                                            -do NOT summarize or omit any results.
                                            -if there is no X handle found, put @COMPANY_NAME in the field e.g. exampleCompany = @exampleCompany
                                            -To get the company name, look at the URL and get the domain name. e.g., www.ExampleCo.com/solutions -> in the Company field, return ExampleCo
                                            -The final answer IS the list displayed, you cannot shorten it for brevity and cannot list companies in a different "final answer" as the final answer is the output
                                            disregard everything in the 'Company' field of the tool output, for the company you are analysing the url in the 'URL' field.

                                        EXAMPLE OUTPUT FOR 3 COMPANIES:

                                        Company,URL,Description,X- Handle,Other contact
                                        "Company1"
                                        www.Company1.com,@Company1,other_contact,
                                        "Company2"
                                        www.Company2.com,@Company2,other_contact
                                        "Company3"
                                        www.Company3.com,@Company3,other_contact

                                    
                                        EXAMPLE: {'Company': 'finance Solutions | ExampleCO USA', 'URL': 'https://www.ExampleCo.com/en-us/shop/solutions/sc/', 'Contact': 'ExampleCo@gmail.com'}

                                        the result for this would be:

                                            "ExampleCo"
                                            www.ExampleCo.com,@ExampleCo,ExampleCo@gmail.com
                                        """,
                    agent=companyFinder,
                    tools=[Scraper()],
                    output_pydantic = result
                )
            ]
        )
        self.logger.info("Crew setup completed")
        return crew
    

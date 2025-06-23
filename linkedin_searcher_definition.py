from crewai import Agent, Crew, Task
from logging_config import get_logger
import pandas as pd
from typing import Generator, Type
from pydantic import BaseModel
from linkedin_search import LinkedinSearch



class result(BaseModel):
    result: str

class LinkedinCrew():
    def __init__(self,verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.crew = self.create_crew()
        self.logger.info("ResearchCrew initialized")

    def create_crew(self):
        self.logger.info("Creating research crew with agents")

        searcher = Agent(
            role='Linkedin URL searcher',
            goal='Read the given URL,use a tool to parse a google search for a linkedin company url and return the first result',
            backstory='Expert at finding linkedin company profiles from given input, and returning a https url of the linkedin',
            verbose=self.verbose
        )

        self.logger.info("Created research and writer agents")

        crew = Crew(
            agents=[searcher],
            tasks=[
                Task(
                    description="""Read {text} use tools to make a google search for a linkedin company profile, returning the first result """,
                    expected_output= """The linkedin URL first result of the tool in HTTPS format, ensuring it is valid URL""",
                    agent=searcher,
                    tools=[LinkedinSearch()],
                    output_pydantic = result
                )
            ]
        )
        self.logger.info("Crew setup completed")
        return crew
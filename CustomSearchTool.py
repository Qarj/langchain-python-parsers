from typing import Optional, Type

from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool

class CustomSearchTool(BaseTool):
    name = "job_search"
    description = "Useful for doing a job search. Input is a job title. Output is a list of jobs."

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Use the tool."""
        return "There were 3 jobs found. The job titles are: Software Engineer, Test Engineer, and Electrical Engineer."
    
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
    

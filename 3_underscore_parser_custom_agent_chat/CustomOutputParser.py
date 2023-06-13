from langchain.agents import AgentOutputParser
from typing import Union
from langchain.schema import AgentAction, AgentFinish
import re

class CustomOutputParser(AgentOutputParser):
    
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Parse out the action and action input
        regex = r"___start_action___(.*)___end_action___.*___start_action_input___(.*)___end_action_input___"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)

        # Check if agent should finish
        if action == "FinalResponse":
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": action_input},
                log=llm_output,
            )

        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input, log=llm_output)

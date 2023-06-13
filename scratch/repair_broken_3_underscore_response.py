import re
from typing import List, Dict, Any, Tuple

class OutputParser:
    def __init__(self, tools: List, bot_name: str):
        self.tools = tools
        self.bot_name = bot_name

    async def parse(self, text: str) -> Dict[str, Any]:
        print(f"OutputParser {self.bot_name} input text: {text}")

        original_text = text

        u = '_' * 3
        # repair incorrect end_action_input, end_action, end_thought, end_response
        text = self._repair_tags(text, u)

        # sometimes the llm forgets to give any of the tags, especially when giving the final response
        # or sometimes it forgets the closing tags, so we try to repair it here
        text = self._add_missing_tags(text, u)

        if original_text != text:
            print(f"OutputParser repaired text: {text}")

        thought_regex = re.compile(f"___start_thought___(.*)___end_thought___", re.S)
        action_regex = re.compile(f"___start_action___(.*)___end_action___", re.S)
        action_input_regex = re.compile(f"___start_action_input___(.*)___end_action_input___", re.S)

        thought = re.search(thought_regex, text)
        action = re.search(action_regex, text)
        action_input = re.search(action_input_regex, text)

        response = {
            "thought": thought.group(1),
            "action": action.group(1),
            "actionInput": action_input.group(1),
        }

        if re.search("finalresponse", response["action"], re.IGNORECASE):
            final_answers = {"output": response["actionInput"]}
            return {"log": text, "returnValues": final_answers}

        tool = response["action"]
        print(f"OutputParser {self.bot_name} parsed tool: {tool}")
        tool = self._find_tool(tool)

        print(f"OutputParser {self.bot_name} parsed text: {response}")

        tool_input = response["actionInput"]
        if isinstance(tool_input, dict):
            tool_input = json.dumps(tool_input)

        return {
            "tool": tool,
            "toolInput": tool_input,
            "log": text,
        }

    def _repair_tags(self, text: str, u: str) -> str:
        replacements = [
            (f"___action_input___", f"___end_action_input___"),
            (f"___action___", f"___end_action___"),
            (f"___thought___", f"___end_thought___"),
            (f"___response___", f"___end_response___"),
            (f"___action_input___", f"___start_action_input___"),
            (f"___action___", f"___start_action___"),
            (f"___thought___", f"___start_thought___"),
            (f"___response___", f"___start_response___"),
        ]

        for old, new in replacements:
            if old in text and new in text:
                text = text.replace(old, new)

        return text

    def _add_missing_tags(self, text: str, u: str) -> str:
        additions = [
            (f"___start_action_input___", f"___end_action_input___"),
            (f"___start_action___finalresponse___end_action___", f"___end_response___"),
            (f"___start_thought___No thought.___end_thought___", f"___start_response___"),
        ]

        for start, end in additions:
            if start not in text:
                text = start + text
            if end not in text:
                text += end

        return text

    def _find_tool(self, tool: str) -> str:
        for t in self.tools:
            if tool.lower().find(t.name.lower()) != -1:
                tool = t.name
                print(f"OutputParser {self.bot_name} confirmed tool: {tool}")
                break

        return tool

    def get_format_instructions(self) -> None:
        raise NotImplementedError("Not implemented")

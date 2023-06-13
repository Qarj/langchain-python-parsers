from dotenv import load_dotenv
load_dotenv()

from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from CustomSearchTool import CustomSearchTool
from CustomPromptTemplate import CustomPromptTemplate, template
from CustomOutputParser import CustomOutputParser

search = CustomSearchTool()
tools = [
    Tool(
        name = "CustomSearchTool",
        func=search.run,
        description="Useful for doing some kind of search"
    )
]

prompt = CustomPromptTemplate(
    template=template,
    tools=tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps"]
)


output_parser = CustomOutputParser()
llm = ChatOpenAI(temperature=0, model="gpt-4")
# LLM chain consisting of the LLM and a prompt
llm_chain = LLMChain(llm=llm, prompt=prompt)

tool_names = [tool.name for tool in tools]
agent = LLMSingleActionAgent(
    llm_chain=llm_chain, 
    output_parser=output_parser,
    stop=["\nObservation:"], 
    allowed_tools=tool_names
)

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

result = agent_executor.run("Search me test engineer jobs in London.")
print("\n\n")
print(result)

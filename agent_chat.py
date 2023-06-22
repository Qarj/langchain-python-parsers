from dotenv import load_dotenv
load_dotenv()

from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from Tools.JobSearchTool import JobSearchTool
from ThreeUnderscoreParser.ThreeUnderscorePromptTemplate import ThreeUnderscorePromptTemplate
from ThreeUnderscoreParser.ThreeUnderscoreOutputParser import ThreeUnderscoreOutputParser
from JsonParser.JsonPromptTemplate import JsonPromptTemplate
from JsonParser.JsonOutputParser import JsonOutputParser

search = JobSearchTool()
tools = [
    Tool(
        name = "JobSearchTool",
        func=search.run,
        description="Useful for searching for jobs, input is jobTitle and jobLocation as a JSON object"
    )
]

# prompt = ThreeUnderscorePromptTemplate(tools=tools, input_variables=["input", "intermediate_steps"])
# output_parser = ThreeUnderscoreOutputParser()

prompt = JsonPromptTemplate(tools=tools, input_variables=["input", "intermediate_steps"])
output_parser = JsonOutputParser()


llm = ChatOpenAI(temperature=0, model="gpt-4")
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

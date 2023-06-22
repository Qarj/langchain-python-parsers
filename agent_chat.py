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
from Journey.JobBot import formatted_journey_prompt

from langchain.agents import AgentType
from langchain.agents import initialize_agent


llm = ChatOpenAI(temperature=0, model="gpt-4")

search = JobSearchTool()
tools = [
    Tool(
        name = search.name,
        func=search.run,
        description=search.description
    )
]

# prompt = ThreeUnderscorePromptTemplate(tools=tools, input_variables=["input", "intermediate_steps"])
# output_parser = ThreeUnderscoreOutputParser()

# prompt = JsonPromptTemplate(tools=tools, input_variables=["input", "intermediate_steps"])
# output_parser = JsonOutputParser()

# llm_chain = LLMChain(llm=llm, prompt=prompt)

tool_names = [tool.name for tool in tools]
# agent = LLMSingleActionAgent(
#     llm_chain=llm_chain, 
#     output_parser=output_parser,
#     stop=["\nObservation:"], 
#     allowed_tools=tool_names
# )
agent = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)


# agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)



# result = agent_executor.run(formatted_journey_prompt())
result = agent.run(formatted_journey_prompt())


print("\n\n")

print("JobBot: ", result)

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

journey_prompt = """Your name is JobBot. You are an advanced AI that helps people find jobs. You
are currently helping a person find a job. You are currently in the middle of a conversation with a person.

Latest message from person: {utterance}

Guidelines:
- Answer the person's questions on job related topics
- Offer to do a job search for the person

__START_EXAMPLES__
{examples}
__END_EXAMPLES__

Conversation so far:
{chat_history}

Jobseeker: {utterance}

JobBot:
"""

utterance = "Search me test engineer jobs in London."
chat_history = """
JobBot: Hey, I'm JobBot, I can help you find a job. What kind of job are you looking for?

Jobseeker: Hey there JobBot. Nice to meet you.

JobBot: Nice to meet you too. What kind of job are you looking for?
"""
examples = """
__Example 1__
Jobseeker: I'm bored of my Chef job. Can you suggest some types of jobs I could do?
JobBot: Sure, here are 10 job titles that someone with a Chef's experience could do:
1. <job title>
2. <job title>
...
10. <job title>

__Example 2__
Jobseeker: Can you please search me tester jobs in Leeds?
JobBot: Sure, here are 5 tester jobs in Leeds:

1. <job title>
2. <job title>
...
5. <job title>

Are you interested in any of these jobs?
""" 

placeholders = []
placeholders.append(("utterance", utterance))
placeholders.append(("chat_history", chat_history))
placeholders.append(("examples", examples))
formatted_journey_prompt = journey_prompt.format(**dict(placeholders))

print (formatted_journey_prompt)

result = agent_executor.run(formatted_journey_prompt)
print("\n\n")

print("JobBot: ", result)

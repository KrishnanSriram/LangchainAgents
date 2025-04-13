from langchain.agents import AgentExecutor, create_react_agent
from langchain_ollama import OllamaLLM
from langchain.tools import Tool
from langchain.prompts import PromptTemplate

llm = OllamaLLM(model="mistral")

def simple_math_tool(input: str) -> str:
    try:
        result = eval(input)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"
    

tools = [ Tool(
    name="Calculator",
    func=simple_math_tool,
    description="Performs basic arithmetic, like '2 + 2 * 5'"
  )
]

prompt = PromptTemplate.from_template("""
Answer the following question as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Begin!

Question: {input}
{agent_scratchpad}
""")

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
response = agent_executor.invoke({"input": "What is 10 multiplied by 12?"})
print(response)

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.tools import DuckDuckGoSearchRun


def search_agent():
  return DuckDuckGoSearchRun()

def str_prompt_template() -> str:
  return """
You are a helpful AI assistant that can search the internet to answer user questions.
You have access to the following tools:

{tools}

You should use the following format:

Question: The input question you must answer
Thought: You should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: The input to the action
Observation: The result of the action
... (This Thought/Action/Observation can repeat multiple times)
Thought: I now know the final answer
Final Answer: The final answer to the original question.

Begin!
Previous conversation history: {chat_history}
Question: {input}
{agent_scratchpad}
"""
  

def main(model: str = ""):
  llm = ChatOllama(model=model)
  tool = [search_agent()]
  memory = ConversationBufferMemory(memory_key="chat_history")
  prompt = PromptTemplate.from_template(str_prompt_template())
  agent = create_react_agent(llm, tools=tool, prompt=prompt)
  agent_executor = AgentExecutor(agent=agent, tools=tool, memory=memory, verbose=False, handle_parsing_errors=True)
  response = agent_executor.invoke({"input": "What is the capital of France?"})
  print(response['output'])

  response = agent_executor.invoke({"input": "What is the population of that city"})
  print(response['output'])

# Check what happens if you execute it without history

if __name__ == "__main__":
  main(model="gemma3:12b")

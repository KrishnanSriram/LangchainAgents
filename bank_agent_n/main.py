import os
from langchain_ollama import OllamaLLM
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from bank_tools import bank_tools


def main():
  # Set up Ollama
  ollama_model = OllamaLLM(model="gemma3:12b")
  tools = bank_tools
  prompt = PromptTemplate.from_template("""
  You are a helpful financial assistant. Answer the following questions as best you can. You have access to the following tools.

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
  # Create the ReAct agent
  agent = create_react_agent(llm=ollama_model, tools=tools, prompt=prompt)
  # Create an agent executor
  agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
  
  # Run the agent
  # response = agent_executor.invoke({"input": "What is the balance of account 12345?"})
  # print(response)
  # response = agent_executor.invoke({"input": "I often buy groceries and shop online, I rarely travel and don't care much about rewards or discounts. What credit card might be good for me?"})
  # response = agent_executor.invoke({"input": "I buy a lot online and spend on groceries, I hardly travel and value credits on purchase or cash back deals. What credit card might be good for me?"})

  response = agent_executor.invoke({"input": "I intend to use this card to purchase air tickets and I travel frequently. What credit card might be good for me?"})
  print(response)


if __name__ == "__main__":
  main()
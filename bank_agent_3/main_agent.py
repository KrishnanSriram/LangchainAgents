from langchain_ollama.llms import OllamaLLM
from langchain.agents import initialize_agent, Tool, AgentType, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from banking_tools import credit_card_advice, investment_banking_advice

def build_tools():
  my_banking_tools = [
    Tool(
        name="Choose CreditCard",
        func=credit_card_advice,
        description="Recommends a credit card from our bank. Input: spending habits, travel frequency, preferred rewards",
    ),
    Tool(
        name="Investment banking advisor",
        func=investment_banking_advice,
        description="Helps you with right kind of recommendations for investment banking",
    ),
  ]
  return my_banking_tools

def main():
  ollama_model = OllamaLLM(model="gemma3:12b")
  tools = build_tools()
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
  response = agent_executor.invoke({"input":"I'm a traveller and I do purchases in airport and online. What's the credit card you recommend?"})
  print(response)

  # response = agent_executor.invoke({"input":"Explain the concept of discounted cash flow in investment banking."})
  # print(response)

if __name__ == "__main__":
  print("invoked main")
  main()
  print("Done")
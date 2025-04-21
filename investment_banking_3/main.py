from langchain_ollama import OllamaLLM 
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from watchlist_tools import add_stock, update_stock, delete_stock, get_all_stocks
from dotenv import load_dotenv

# def create_prompt_template():
#   react_prompt = PromptTemplate.from_template("""
#   You are a portfolio management assistant.
#   Your job is to understand the user's instruction and use tools to perform the correct action.
#   You have access to the following tools:
#   {tools}
#   Available tools:
#   {tool_names}

#   Follow this format:
#   Question: {input}
#   {agent_scratchpad}
#   """)
#   return react_prompt


def create_prompt_template():
  return PromptTemplate.from_template("""
  You are a smart agent that uses tools to solve problems step-by-step.

  You have access to the following tools:
  {tools}

  Use the following format in your reasoning:

  Question: the input question you must answer
  Thought: think about what to do
  Action: the action to take, should be one of [{tool_names}]
  Action Input: the input to the action
  Observation: the result of the action
  ... (repeat Thought/Action/Action Input/Observation as needed)
  Thought: I now know the final answer
  Final Answer: the final answer to the original question

  Begin!

  Question: {input}
  {agent_scratchpad}
  """)



def main(model_name: str = "gemma3:12b"):
  llm = OllamaLLM(model=model_name)
  # 4. ReAct-style prompt template
  prompt = create_prompt_template()
  llm = OllamaLLM(model=model_name)

  nlp_tools = [add_stock, update_stock, delete_stock, get_all_stocks]

  nlp_agent = create_react_agent(llm=llm, tools=nlp_tools, prompt=create_prompt_template())
  nlp_executor = AgentExecutor(agent=nlp_agent, tools=nlp_tools, verbose=True, handle_parsing_errors=True)
  response = nlp_executor.invoke({"input":"list all scrips in watchlist. Can you?"})
  print(response)

if __name__ == "__main__":
  load_dotenv()
  main(model_name="gemma3:12b")
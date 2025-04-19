from langchain_ollama import OllamaLLM
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import tool
from investment_tools import get_recommended_shares, buy_shares, notify_user
from dotenv import load_dotenv
import os


def build_market_executor(llm, react_prompt):
  # Agent 1: Recommends Shares
  market_tools = [get_recommended_shares]
  market_agent = create_react_agent(llm=llm, tools=market_tools, prompt=react_prompt)
  market_executor = AgentExecutor(agent=market_agent, tools=market_tools, verbose=True)
  return market_executor

def build_trading_executor(llm, react_prompt):
  # Agent 2: Buys Shares
  trading_tools = [buy_shares]
  trading_agent = create_react_agent(llm=llm, tools=trading_tools, prompt=react_prompt)
  trading_executor = AgentExecutor(agent=trading_agent, tools=trading_tools, verbose=True)
  return trading_executor

def build_notification_executor(llm, react_prompt):
  # Agent 3: Notifies Users
  notify_tools = [notify_user]
  notify_agent = create_react_agent(llm=llm, tools=notify_tools, prompt=react_prompt)
  notify_executor = AgentExecutor(agent=notify_agent, tools=notify_tools, verbose=True)
  return notify_executor

def investment_workflow(llm, prompt):
  print("\n=== STEP 1: Market Research ===")
  market_executor = build_market_executor(llm, prompt)
  research_output = market_executor.invoke({"input": "Which shares should I buy today?"})
  shares = research_output['output']
  print(shares)

  print("\n=== STEP 2: Trading Execution ===")
  trade_executor = build_trading_executor(llm, prompt)
  trade_output = trade_executor.invoke({"input": shares})
  purchase_summary = trade_output['output']
  print(purchase_summary)

  print("\n=== STEP 3: User Notification ===")
  notify_executor = build_notification_executor(llm, prompt)
  notify_output = notify_executor.invoke({"input": purchase_summary})
  print(f"\n{notify_output['output']}")



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
  investment_workflow(llm=llm, prompt=prompt)


if __name__ == "__main__":
  load_dotenv()
  main(model_name="gemma3:12b")


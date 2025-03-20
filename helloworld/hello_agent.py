from langchain.agents import AgentType
from langchain.agents.initialize import initialize_agent
from langchain.tools import Tool
from langchain_ollama import ChatOllama
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_core.prompts import PromptTemplate

def get_model(name: str) -> ChatOllama:
  return ChatOllama(model="mistral")


def greet(name: str) -> str:
  return f"Hello {name}, How can I assist you?"


def get_prompt_template():
  return PromptTemplate.from_template("Tell me about {name}")


def create_greet_tool() -> Tool:
  greet_tool = Tool(
    name= "GreetUser",
    func=greet,
    description="Greets the user by name"
  )
  return greet_tool


def init_agents():
  tools = [Tool(
    name= "GreetUser",
    func=greet,
    description="Greets the user by name"
  )]
  agent = initialize_agent(tools=tools, llm=get_model("mistral"), agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
  return agent


def main():
  agent = init_agents()
  agent.invoke("Wish Sriram")


if __name__ == "__main__":
  main()
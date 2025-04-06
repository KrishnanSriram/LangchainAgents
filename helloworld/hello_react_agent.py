from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.chat_models import ChatOllama
from langchain.tools import Tool
from langchain.tools import tool
from langchain import hub
# Step 1: Define a tool the agent can use
@tool
def add_numbers(numbers: str) -> str:
    """Adds two numbers. Input should be two numbers separated by a comma."""
    a, b = map(float, numbers.split(","))
    return str(a + b)

tools = [add_numbers]

# Step 2: Load the Ollama LLM with llama3
llm = ChatOllama(model="llama3.2")

prompt = hub.pull("hwchase17/react")

# Step 3: Create the ReAct Agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

# Step 4: Wrap it with AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Step 5: Run it!
if __name__ == "__main__":
    while True:
        user_input = input("\nAsk me something (or type 'exit'): ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent_executor.invoke({"input": user_input})
        print("\n🤖 Response:", response["output"])

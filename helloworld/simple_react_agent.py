from langchain.agents import AgentExecutor, create_tool_calling_agent, tool
from langchain_core.prompts import ChatPromptTemplate

retriever_tool = create_retriever_tool(
    retriever, 
    "similar_app_search",
    "Search for information about the given Android app. For any questions about the given Android app, you must use this tool!"
)
tools = [retriever_tool]
role_prompt = "Given app name to you, you need to search related information."

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", role_prompt),
        ("human", "What is {app_name}?"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

llm = get_llm("llama3")
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Example usage
agent_executor.invoke({"input": "What is the value of similar_app_search for 'example app'?"})
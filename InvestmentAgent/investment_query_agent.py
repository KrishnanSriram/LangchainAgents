import os
from langchain.llms import Ollama
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.tools import DuckDuckGoSearchRun
from langchain.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA

# Configuration
persist_directory = "chroma_db"
ollama_model = "gemma3:12b" # or whatever model you chose
text_embedding_model = "nomic-embed-text"

# Ollama Setup
ollama_llm = Ollama(model=ollama_model)
ollama_embeddings = OllamaEmbeddings(model=text_embedding_model)

# Tools
search = DuckDuckGoSearchRun()

# Load ChromaDB
vectordb = Chroma(persist_directory=persist_directory, embedding_function=ollama_embeddings)
retriever = vectordb.as_retriever()
qa = RetrievalQA.from_chain_type(llm=ollama_llm, chain_type="stuff", retriever=retriever)

tools = [
    # Tool(
    #     name="Search",
    #     func=search.run,
    #     description="useful for when you need to answer questions about current financial events.",
    # ),
    Tool(
        name="Investment Knowledge",
        func=qa.run,
        description="useful for when you need to answer questions about investment banking, mergers and acquisitions, financial analysis, and valuation. Input should be a fully formed question.",
    ),
]

# Agent Initialization
agent = initialize_agent(
    tools,
    ollama_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# Example Queries
try:
    response = agent.invoke("What do investment bankers do?")
    print(response)
    # response = agent.run("Explain the process of a leveraged buyout.")
    # print(response)
    # response = agent.run("What are the recent valuations of companies in the renewable energy sector?")
    # print(response)
except Exception as e:
    print(f"An error occurred: {e}")
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms import Ollama
from langchain.agents import AgentExecutor
import os

# 1. Setup the Ollama LLM
llm = Ollama(model="gemma3:12b") # or your preferred model

# 2. Setup the SQL Database connection.
# Replace with your actual database connection string.
# Example for SQLite:
db_uri = "sqlite:///./chinook.sqlite"

# Example for PostgreSQL:
# db_uri = "postgresql://user:password@host:port/database"

#Example for MySQL:
#db_uri = "mysql+pymysql://user:password@host:port/database"

#Example for MSSQL:
#db_uri = "mssql+pyodbc://user:password@host:port/database?driver=ODBC+Driver+17+for+SQL+Server"

#Ensure you have the correct driver installed. For example, for postgres, install psycopg2-binary: pip install psycopg2-binary
#For mysql, install pymysql: pip install pymysql

db = SQLDatabase.from_uri(db_uri)

# 3. Create the SQL Toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# 4. Create the SQL Agent
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True, # Set to True for debugging
    handle_parsing_errors=True
)

# 5. Run the Agent with a Query
query = "How many artists are there?"
response = agent_executor.run(query)
print(response)

# query = "What are the top 5 highest total sales?"
# response = agent_executor.run(query)
# print(response)

# query = "List all the albums by AC/DC"
# response = agent_executor.run(query)
# print(response)
import os
from langchain.agents import initialize_agent, AgentType
from langchain_community.llms import Ollama
from langchain.tools import Tool
from langchain_community.document_loaders import CSVLoader
import psycopg2
import pandas as pd
from psycopg2 import extras

# 1. Setup
os.environ['OLLAMA_BASE_URL'] = "http://localhost:11434" # Replace with your Ollama server address
DB_HOST = "localhost"
DB_NAME = "your_database_name"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_PORT = "5432"
CSV_FILE_PATH = "your_data.csv"
TABLE_NAME = "your_table_name"

# 2. Load CSV into Pandas
df = pd.read_csv(CSV_FILE_PATH)

# 3. Infer Schema and Generate CREATE TABLE Statement
def get_postgres_type(dtype):
    if dtype == 'int64':
        return 'INTEGER'
    elif dtype == 'float64':
        return 'REAL'
    elif dtype == 'bool':
        return 'BOOLEAN'
    elif dtype == 'datetime64[ns]':
         return 'TIMESTAMP'
    else:
        return 'TEXT'  # Default to TEXT for other types

columns = []
for col, dtype in df.dtypes.items():
    columns.append(f"{col} {get_postgres_type(str(dtype))}")
create_table_statement = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({', '.join(columns)})"

# 4. Create Table in Postgres
def create_table_postgres():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute(create_table_statement)
        conn.commit()
        cur.close()
        conn.close()
        return "Table created successfully!"
    except Exception as e:
        return f"Error creating table: {str(e)}"
    
create_table_postgres() # Call the function to create the table

# 5. Modified Tool
def insert_to_postgres(data):
  try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        df_to_insert = pd.DataFrame([data])
        cols = ', '.join(list(df_to_insert.columns))
        query = f"INSERT INTO {TABLE_NAME} ({cols}) VALUES %s"
        vals = [tuple(x) for x in df_to_insert.values]
        extras.execute_values(cur, query, vals)
        conn.commit()
        cur.close()
        conn.close()
        return "Data inserted successfully!"
  except Exception as e:
    return f"Error inserting data: {str(e)}"

tools = [
    Tool(
        name="Postgres Insert",
        func=insert_to_postgres,
        description="Use this tool to insert data into the Postgres database table."
    )
]

# 6. Initialize Agent
llm = Ollama(model="llama3")
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# 7. Run Agent
loader = CSVLoader(file_path=CSV_FILE_PATH)
docs = loader.load()

for doc in docs:
    agent.run(f"Insert this data: {doc.page_content} into the {TABLE_NAME} table using the Postgres Insert tool.")

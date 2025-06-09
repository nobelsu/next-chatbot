from openai import OpenAI
from os import getenv
from dotenv import load_dotenv
import duckdb

load_dotenv()
model = OpenAI(
    api_key=getenv("OPENAI_API_KEY"),
)
db = duckdb.connect("db/csv_db")

def text2SQL(q, df, table_name):
    prompt = f"""
    You are a helpful assistant that can generate SQL queries to answer questions about the data.
    The data could be stored in the following table: {table_name}. 
    If the table's data is insufficient, only return the string "none".
    Here is the schema of the table:
    {df}
    The question is: {q}
    """

    response = model.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that can generate SQL queries to answer questions about the data. Only return the sql query and nothing else."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content

def querySQL(q, tableCnt):
    for i in range(tableCnt):
        table_name = f"table{i}"
        print("here")
        df = db.sql(f"DESCRIBE {table_name}")
        print("here2")
        sqlQuery = text2SQL(q, df, table_name)
        sqlQuery = sqlQuery.replace("```sql", "").replace("```", "").strip()
        print("sqlQuery: ", sqlQuery)
        if sqlQuery != "none":
            return db.sql(sqlQuery)
    return "I'm sorry, I can't answer that question."
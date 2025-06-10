from openai import OpenAI
from os import getenv
from dotenv import load_dotenv
from chonkie import OpenAIEmbeddings
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
    If the table data is not helpful in responding to the user's query, return the string "none" only.
    Please ensure that the SQL queries are valid for DuckDB.
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

def sql2Text(q):
    prompt = f"""
    You are a helpful assistant that can turn SQL data into user-friendly text.
    Make sure that the data is presented in a readable and easily digestible format.
    If the data provided is not JSON/SQL data, respond with "I'm sorry, I can't answer that question." 
    Highlight titles, subtitles, and key details with a bold. 

    The data is {q}
    """
    response = model.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that can turn SQL data into user-friendly text."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content

def querySQL(q, collection):
    embeddings = OpenAIEmbeddings()
    query_embedding = embeddings.embed(q)
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )
    print(results)
    print(results["metadatas"])

    for item in results["metadatas"][0]:
        table_name = item["table_name"] 
        df = db.sql(f"DESCRIBE {table_name}")
        sqlQuery = text2SQL(q, df, table_name)
        sqlQuery = sqlQuery.replace("```sql", "").replace("```", "").strip()
        if sqlQuery == "none": 
            continue
        result = db.sql(sqlQuery).df().to_dict(orient="records")
        return sql2Text(str(result)) 


    # print("metadata", results["documents"][0][0].metadata)
    # return "Temporary"
    # for i in range(tableCnt):
    #     table_name = f"table{i}"
    #     df = db.sql(f"DESCRIBE {table_name}")
    #     sqlQuery = text2SQL(q, df, table_name)
    #     sqlQuery = sqlQuery.replace("```sql", "").replace("```", "").strip()
    #     print(sqlQuery)
    #     try:
    #         if sqlQuery != "none":
    #             result = db.sql(sqlQuery).df().to_dict(orient="records")
    #             return sql2Text(str(result)) 
    #     except Exception as e:
    #         return f"SQL Error: {str(e)}"
    return "I'm sorry, I can't answer that question."
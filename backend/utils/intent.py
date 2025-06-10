from openai import OpenAI
from os import getenv
from dotenv import load_dotenv
import duckdb

def classifyIntent(q):
    load_dotenv()
    model = OpenAI(
        api_key=getenv("OPENAI_API_KEY"),
    )
    db = duckdb.connect("db/csv_db")

    prompt = f"""
        Decide if the query needs a vector search or text 2 sql search.print
        If the user is asking for specific data which is usually like a numerical operation like greater than, less than, etc. then it is a text 2 sql search. Similary if they are asking for details mentioning a specific field name like find me details of employee with id 123 then it is a text 2 sql search.
        If the user query is a general, hi, hello, etc. then it is a General intent.
        For everything else, it is a vector search.

        Here are the list of tables in the database:
        {db.sql("SELECT table_name FROM information_schema.tables").fetchall()}

        here is the list of pdf documents we have ingested in vector db:
        "budget_speech.pdf". This document has all data to related budget of India.

        The query is: {q}

        Only return the Intent as a string. It will be either "vector" or "text_2_sql" or "general".    """

    response = model.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content
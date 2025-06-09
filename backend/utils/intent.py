from openai import OpenAI
from os import getenv
from dotenv import load_dotenv

def classifyIntent(q):
    load_dotenv()
    model = OpenAI(
        api_key=getenv("OPENAI_API_KEY"),
    )

    prompt = f"""
        Decide if the query needs a vector search or text 2 sql search.print
        If the user is asking for specific data which is usually like a numerical operation like greater than, less than, etc. then it is a text 2 sql search. Similary if they are asking for details mentioning a specific field name like find me details of employee with id 123 then it is a text 2 sql search.
        If the user query is a general, hi, hello, etc. then it is a General intent.
        For everything else, it is a vector search.

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
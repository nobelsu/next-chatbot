from openai import OpenAI
from os import getenv
from dotenv import load_dotenv

def classifyIntent(q):
    load_dotenv()
    model = OpenAI(
        api_key=getenv("OPENAI_API_KEY"),
    )

    prompt = f"""
        Decide if the query needs a vector search or a general response.
        If the user query is a general, hi, hello, etc. then it is a General intent.
        For everything else, it is a vector search.

        The query is: {q}

        Only return the Intent as a string. It will be either "vector" or "general".    """

    response = model.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content
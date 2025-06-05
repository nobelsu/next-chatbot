from openai import OpenAI
from os import getenv
from dotenv import load_dotenv

def rewriteQuery(query, conversations: list[dict]):
    load_dotenv()
    model = OpenAI(
        api_key=getenv("OPENAI_API_KEY")
    )

    history_context = "\n".join([f"{conv['role']}: {conv['content']}" for conv in conversations])

    prompt = f"""
    You are a helpful assistant that can rewrite queries to be more specific and accurate. Always rewrite the query mentioning the name of the person if they have already mentioned it.
    The conversation history is:
    {history_context}
    The query is:
    {query}
    """

    response = model.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content
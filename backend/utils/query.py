import chromadb
from chonkie import ChromaHandshake, RecursiveChunker, Visualizer, OpenAIEmbeddings
from markitdown import MarkItDown
from openai import OpenAI
from os import getenv
from dotenv import load_dotenv  

def get_rag_answer(results, query, model, model_name="gpt-4o", temperature=0):
    """
    Generate an answer using RAG (Retrieval Augmented Generation).
    
    Args:
        results: Search results from vector database query
        query: The user's question
        model: OpenAI client instance
        model_name: The model to use for completion (default: "gpt-4o")
        temperature: Temperature for the completion (default: 0)
    
    Returns:
        str: The generated answer
    """
    # Format the context from the search results
    context = "\n".join(results["documents"][0])

    # Create the prompt with the context and query
    prompt = f"""Use the following context to answer the question. If you cannot answer the question based on the context, say "I cannot answer this based on the provided context."

Context:
{context}

Question: {query}"""

    # Get completion from OpenAI
    response = model.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )

    return response.choices[0].message.content 

def sendQuery(q, collection):
    load_dotenv()
    model = OpenAI(
        api_key=getenv("OPENAI_API_KEY"),
    )
    embeddings = OpenAIEmbeddings()
    query_embedding = embeddings.embed(q)
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )
    answer = get_rag_answer(results, q, model)
    return answer
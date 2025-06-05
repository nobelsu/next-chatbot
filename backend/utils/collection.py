import chromadb
from chonkie import ChromaHandshake, OpenAIEmbeddings   
from dotenv import load_dotenv
from openai import OpenAI
from os import getenv

def createCollection(x):
    load_dotenv()
    model = OpenAI(
        api_key=getenv("OPENAI_API_KEY"),
    )
    embeddings = OpenAIEmbeddings()
    client = chromadb.Client()
    handshake = ChromaHandshake(client=client, collection_name="pdf_data", embedding_model=embeddings, path="db/pdf_db")
    for i in x:
        handshake.write(i)
    collection = client.get_collection("pdf_data")
    return collection

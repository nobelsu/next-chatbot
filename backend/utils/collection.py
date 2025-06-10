import chromadb
from chonkie import ChromaHandshake, OpenAIEmbeddings   
from dotenv import load_dotenv
from openai import OpenAI
from os import getenv

load_dotenv()
model = OpenAI(
    api_key=getenv("OPENAI_API_KEY"),
)
embeddings = OpenAIEmbeddings()
client = chromadb.Client()

def createCollectionPDF(x):
    handshake = ChromaHandshake(client=client, collection_name="pdf_data", embedding_model=embeddings, path="db/pdf_db")
    for i in x:
        handshake.write(i)
    collection = client.get_collection("pdf_data")
    return collection

def createCollectionCSV(x):
    handshake = ChromaHandshake(client=client, collection_name="csv_data", embedding_model=embeddings, path="db/csv_db")
    for i in x:
        handshake.write({
            "text": i.text,
            "metadata": i.metadata
        })
    collection = client.get_collection("csv_data")
    return collection
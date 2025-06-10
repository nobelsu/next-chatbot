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

def createCollectionPDF(chunks):
    handshake = ChromaHandshake(client=client, collection_name="pdf_data", embedding_model=embeddings, path="db/pdf_db")
    for chunk in chunks:
        handshake.write(chunk)
    collection = client.get_collection("pdf_data")
    return collection

def createCollectionCSV(chunks):
    texts = [chunk.text for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    ids = [chunk.id for chunk in chunks]
    # client = chromadb.PersistentClient(path="db/csv_db")
    collection = client.get_or_create_collection("csv_data")
    # handshake = ChromaHandshake(client=client, collection_name="csv_data", embedding_model=embeddings, path="db/csv_db")
    # for chunk in chunks:
    #     handshake.write(chunk)
    # collection = client.get_collection("csv_data")
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings(texts),
        metadatas=metadatas
    )
    return collection
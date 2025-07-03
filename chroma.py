import chromadb
from chromadb.config import Settings

chroma_client = client = chromadb.PersistentClient(path="./chroma_store", settings=Settings(anonymized_telemetry=False))
collection = chroma_client.get_or_create_collection("investors")
import chromadb
from chromadb.config import Settings

chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))
collection = chroma_client.get_or_create_collection("investors")
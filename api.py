from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
from chroma import chromadb
from api_keys import api_key

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

openai.api_key = api_key
collection = chromadb.PersistentClient(path="./chroma-db").get_or_create_collection("investors")

class Startup(BaseModel):
    description: str

@app.post("/match")
def match_startup(startup: Startup):
    emb = openai.Embedding.create(model="text-embedding-3-small", input=[startup.description])
    query_embedding = emb["data"][0]["embedding"]

    results = collection.query(query_embeddings=[query_embedding], n_results=5)

    return {
        "matches": [
            {"investor": m["name"], "profile": d}
            for d, m in zip(results["documents"][0], results["metadatas"][0])
        ]
    }

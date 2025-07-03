from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
from chroma import chromadb
from api_keys import api_key
from utils import get_incoming_startup_prompt
from chatCompletionLLM import fill_extra_matches

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

    formatted_prompt = get_incoming_startup_prompt(startup)
    emb = openai.Embedding.create(model="text-embedding-3-small", input=[formatted_prompt])
    query_embedding = emb["data"][0]["embedding"]

    results = collection.query(query_embeddings=[query_embedding], n_results=3,  include=["distances", "documents", "metadatas"])

    final_matches = []

    for d, m, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        if dist < 0.3:
            final_matches.append({
                "investor": m["name"],
                "profile": d,
                "distance": dist
            })

    if len(final_matches) < 5:
        fill_extra_matches(5-len(final_matches), final_matches)
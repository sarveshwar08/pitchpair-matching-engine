import pandas as pd
from embedding import get_embedding, get_investor_profile_prompt
from chroma import collection, chroma_client

def process_excel_and_store():
    df = pd.read_excel('assets/investor_data.xlsx', sheet_name='P0-data')
    print(len(df))

    for _, row in df.iterrows():

        investor_name = row['investor_name']
        print(investor_name, type(investor_name))
        prompt = get_investor_profile_prompt(row)
        embedding = get_embedding(prompt)

        collection.add(
            documents=[prompt],
            embeddings=[embedding],
            ids=[f"investor-{investor_name}"],
            metadatas=[{"name": investor_name}]
        )
    print("Investor profiles stored in vector database.")


process_excel_and_store()
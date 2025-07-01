import pandas as pd
from embedding import get_embedding, get_investor_profile_prompt, get_llm_profile
from chroma import collection

def process_excel_and_store():
    df = pd.read_excel('investor_data.xlsx', sheet_name='P0-Data for Matching Logic(Investor)')

    for _, row in df.iterrows():
        investor_name = row['investor_name']
        prompt = get_investor_profile_prompt(row)
        profile_json = get_llm_profile(prompt)
        embedding = get_embedding(profile_json)

        if investor_name == 'Rocket Internet':
            print(profile_json)
        collection.add(
            documents=[profile_json],
            embeddings=[embedding],
            ids=[f"investor-{investor_name}"],
            metadatas=[{"name": investor_name}]
        )

    print("Investor profiles stored in vector database.")
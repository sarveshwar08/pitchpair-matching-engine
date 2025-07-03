import openai
import pandas as pd
from chroma import chroma_client, collection
from api_keys import api_key

openai.api_key = api_key

def get_investor_profile_prompt(row):
    investor = row.get('investor_name', 'Unknown Investor').strip()

    thesis_raw = str(row.get('thesis', '')).strip()
    thesis = "All" if 'Not Public' in thesis_raw or thesis_raw == '' else thesis_raw

    stage = row.get('stage', 'Any Stage').strip()
    geos = row.get('geographies_funded', 'Global').strip()
    ticket_size = row.get('Team Size Range', 'Not Disclosed').strip()  # Rename if needed

    return f"""
        {investor} prefers {thesis} (sector) startups which have their raising stage as {stage}. {investor} focuses on {geos} countries
        with an average ticke size ranging as {ticket_size}.
        (Note the curency in ticket size)
        """


def get_llm_profile(prompt):
    response = openai.ChatCompletion.create(
        model='gpt-4o',
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response['choices'][0]['message']['content']

def get_embedding(text):
    response = openai.Embedding.create(
        model="text-embedding-3-small",
        input=[text]
    )
    return response["data"][0]["embedding"]
from openai import OpenAI
from api_keys import api_key

client = OpenAI()

def get_investor_profile_prompt(row):
    investor = row.get('investor_name', 'Unknown Investor').strip()

    thesis_raw = str(row.get('thesis', '')).strip()
    thesis = "All" if 'Not Public' in thesis_raw or thesis_raw == '' else thesis_raw

    stage = row.get('stage', 'Any Stage').strip()
    geos = row.get('geographies_funded', 'Global').strip()
    ticket_size = row.get('ticket_size', 'Not Disclosed').strip() 

    return f"""{investor} prefers {thesis} (sector) startups which have their raising stage as {stage}. {investor} focuses on {geos} countries with an average ticket size ranging as {ticket_size}."""


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=[text]
    )
    return response.data[0].embedding
import openai
import pandas as pd
from chroma import chroma_client, collection
from api_keys import api_key

openai.api_key = api_key

def get_investor_profile_prompt(row):
    investor = row.get('investor_name', 'Unknown Investor').strip()

    # Handle defaults and edge cases
    thesis_raw = str(row.get('thesis', '')).strip()
    thesis = "All" if 'Not Public' in thesis_raw or thesis_raw == '' else thesis_raw

    stage = row.get('stage', 'Any Stage').strip()
    geos = row.get('geographies_funded', 'Global').strip()
    ticket_size = row.get('Team Size Range', 'Not Disclosed').strip()  # Rename if needed

    return f"""
        Return the investment preferences in JSON format for the investor below.
        If any field is unclear or marked as "Not Public", use a sensible default.

        Investor: {investor}
        Preferred Industries: {thesis}
        Preferred Stages: {stage}
        Geographies: {geos}
        Ticket Size: {ticket_size}

        Output only JSON. Do not add any explanation.
        Some notes per field to follow while converting in JSON:
            Geographies: May contin abbreviations, resolve to full country name. If the value is global, don't read further for this field.
            Preferred Stages: Maybe 1 or 2 values or may be a range(seperated by 'to'). Resolve accordingly
        """


def get_llm_profile(prompt):
    response = openai.ChatCompletion.create(
        model='gpt-4o',
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response['choices'][0]['message']['content']

# Step 2: Get embedding for the profile
def get_embedding(text):
    response = openai.Embedding.create(
        model="text-embedding-3-small",
        input=[text]
    )
    return response["data"][0]["embedding"]
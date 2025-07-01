import pandas as pd
import openai
from pymongo import MongoClient
from collections import defaultdict
import json

# ==== Setup ====
openai.api_key = 'sk-proj-_j0uogeLCxO2XzHBw2g8EZ87czpeXRrgs7-'

client = MongoClient('mongodb+srv://swesarveshwar08:mongoDBpp2025@pitchpair.cvbhstl.mongodb.net/?retryWrites=true&w=majority&appName=pitchpair')
db = client['investor_matching']
collection = db['investor_profiles']

# ==== Step 1: Load Excel and Organize Startups per Investor ====


# Replace with your actual attribute column names
attribute_columns = ['geographies_funded', 'stage', 'ticket_size', 'thesis', 'country']

investor_startups = defaultdict(list)

# ==== Step 2: Extract Preferences using LLM ====
def build_prompt(investor_name, startup_list):
    return (
        f"Investor: {investor_name}\n"
        f"Based on the following attributes of a startup this investor invests in\n"
        f"Startups:\n{json.dumps(startup_list, indent=2)}\n\n"
        "Return a JSON structure like this:\n"
        "{\n"
        "  \"Preferred Industries\": [...],\n"
        "  \"Preferred Stages\": [...],\n"
        "  \"Preferred Geographies\": [...],\n"
        "  \"Ticket Range\": \"\",\n"
        "}"
    )

def build_prompt_feed_memory():
    

def feed_data_on_server_start():
    df = pd.read_excel('investor_data.xlsx', sheet_name='P0-Data for Matching Logic(Investor)')  # adjust path

    for _, row in df.iterrows():
        investor_name = str(row['investor_name']).strip()
        attrs = row[attribute_columns].to_dict()
        investor_startups[investor_name].append(attrs)



def get_investor_profile(investor, startups):
    prompt = build_prompt(investor, startups)
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    content = response['choices'][0]['message']['content']
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print(f"Error parsing response for {investor}: {content}")
        return None

# ==== Step 3: Store in MongoDB ====
for investor, startups in investor_startups.items():
    profile = get_investor_profile(investor, startups)
    if profile:
        doc = {'investor': investor, 'preferences': profile}
        collection.replace_one({'investor': investor}, doc, upsert=True)
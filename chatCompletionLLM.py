from openai import OpenAI
from api_keys import api_key
from utils import parse_llm_json_string

client = OpenAI()


def fill_extra_matches(num, startup_query, final_matches = []):
    
    if num==0:
        return []

    prompt = f"""
            Based on the following startup profile:
            {startup_query}

    Please suggest {num} investors (with name and brief profile) who are likely to be a match. excluding any of the following already matched investors: {[m['investor'] for m in final_matches]}
    Return the output in this format:
    [
    {{
        "investor": "Investor Name",
        "profile": "Brief description here"
    }},
    ...
    ]
    """

    # Call the LLM
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    extra_matches = parse_llm_json_string((response.choices[0].message.content).strip())

    for match in extra_matches:
        match['external'] = 'Y'
    
    final_matches.extend(extra_matches)

    return final_matches


startup_q = """We are a Edtech/AI sector startup, looking for Seed (Pre-Series A at time of funding) funding. We are based out of India (global users, HQ Lucknow)
            and have an ask of $1200K."""
fill_extra_matches(2, startup_q)
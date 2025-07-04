import json
import ast

def get_incoming_startup_prompt(startup):

    return "Startup Sector: Edtech/AI | Stage: Seed (Pre-Series A) | Geography: India | Ask: $1200K"
    return (f"""We are a {startup.industry} sector startup, looking for {startup.stage} funding. We are based out of {startup.country} and have an ask of {startup.ask}.""")

def parse_llm_json_string(response_str: str):
    """
    Attempts to parse a JSON-style string from an LLM response.
    Tries json.loads first, then ast.literal_eval as a fallback.

    Args:
        response_str (str): The raw response string from the LLM.

    Returns:
        list[dict]: Parsed list of dictionaries if successful.
        None: If parsing fails.
    """
    cleaned = response_str.replace("“", "\"").replace("”", "\"").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(cleaned)
        except Exception as e:
            print("Failed to parse LLM response:", e)
            return None

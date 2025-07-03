def fill_extra_matches(num, final_matches):
    if num==0:
        return []
    startup_attrs = {  # The incoming startup query
        "sector": "FinTech",
        "stage": "Seed",
        "geo": "India",
    }

    # Generate the prompt
    prompt = f"""
    Based on the following startup profile:
    {startup_attrs}

    Please suggest {num} investors (with name and brief profile) who are likely to be a match, excluding any of the following already matched investors: {[m['investor'] for m in final_matches]}.
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
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    print(response["choices"][0]["message"]["content"])
    # # Parse LLM response
    # try:
    #     extra_matches = eval(response["choices"][0]["message"]["content"])
    #     final_matches.extend(extra_matches)
    # except Exception as e:
    #     print("Failed to parse LLM response:", e)
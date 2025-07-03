def get_incoming_startup_prompt(startup):

    return (f"""We are a {startup.industry} sector startup, looking for {startup.stage} funding. We are based out of {startup.country}
    and have an ask of {startup.ask}.
    """)

from chroma import collection, chroma_client

def get_existing_ids():
    existing_ids = collection.get()
    print(type(existing_ids))
    print(f"Total stored entries: {len(existing_ids)}")


get_existing_ids()
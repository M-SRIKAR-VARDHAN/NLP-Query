import chromadb

# Use the new PersistentClient — this is what the Chroma docs recommend now
client = chromadb.PersistentClient(path="./chroma_db")

# Create or load your collection
collection = client.get_or_create_collection(name="assessments")

import pandas as pd
from embeddings import get_embedding
from store import collection  # Import only collection, no need for client.persist()

# Read the CSV file
df = pd.read_csv("shl_all_assessments_with_time_tags.csv")
# right after you load df:
df.columns = df.columns.str.strip()

# Optional: Print column names to check for correct names
print(df.columns.tolist())

# Generate ids based on row index
ids = df.index.astype(str).tolist()

# Create the document list with formatted strings
documents = [
    f"{r['Name']}. Types: {r['Test Type']}. Adaptive: {r['Adaptive/IRT']}. "
    f"Remote: {r['Remote Testing']}. Duration: {r['Time']} min."
    for _, r in df.iterrows()
]

# Convert dataframe rows to a list of dictionaries for metadata
metadatas = df.to_dict(orient="records")

# Add the data to Chroma
collection.add(
    ids=ids,
    documents=documents,
    embeddings=[get_embedding(doc) for doc in documents],
    metadatas=metadatas
)

# No need for client.persist(), data is automatically persisted.

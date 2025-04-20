from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # example
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding)

retrieved = db.similarity_search("remote numerical test for entry-level roles", k=3)
for doc in retrieved:
    print(doc.metadata)

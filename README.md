# SHL Assessment Recommendation API

This project is a FastAPI-based recommendation system for SHL assessments. It allows users to input a query (e.g., *"remote numerical test for entry-level roles"*) and receive relevant assessment suggestions based on predefined metadata.

## 🔧 Features

- REST API built with FastAPI
- Ingests and indexes SHL assessments from a CSV
- Vector search using embeddings (via ChromaDB)
- Filtering based on remote support and duration
- Supports interactive Swagger UI and programmatic POST requests

---

## 📁 Project Structure

```
SHL/
│
├── api.py                  # FastAPI app and route definitions
├── embeddings.py           # Text embedding logic
├── ingest.py               # Data ingestion script
├── tagging.py              # Tag/metadata extraction
├── scrape.py / scrape2.py  # Web scraping utilities
├── store.py                # ChromaDB storage handler
├── test.py                 # Evaluation script
├── shl_all_assessments_with_time_tags.csv  # Source data
├── chroma_db/              # Local vector database
└── .vscode/                # Editor config (optional)
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```
cd SHL
```

### 2. Install Dependencies

Create a virtual environment (optional):

```
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
```

Install the requirements:

```
pip install -r requirements.txt
```

> If \`requirements.txt\` isn't available, manually install:
```
pip install fastapi uvicorn chromadb openai
```

### 3. Ingest Data

Before running the API, index the assessments:

```
python ingest.py
```

---

## 🧪 Running the API

```
uvicorn api:app --reload
```

### API Endpoints

- \`GET /\` - Welcome route  
- \`GET /health\` - Health check  
- \`POST /recommend\` - Get recommended assessments  

### Example Request (via cURL)

```
curl -X POST "http://127.0.0.1:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{"query": "remote numerical test for entry-level roles", "k": 3, "remote_only": true, "max_duration": 30}'
```

### Try in Browser

Once the server is running, visit:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

You can test the endpoints directly from this interactive Swagger UI.

---

## ✅ Evaluation

Run the \`test.py\` script to evaluate the system's recall and precision:


```python test.py```

---

## 🧠 Notes

- Ensure you have \`shl_all_assessments_with_time_tags.csv\` in the root directory.  
- Embeddings and index are stored in \`chroma_db/\`.


---

## 🙌 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)  
- [ChromaDB](https://www.trychroma.com/)  
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)  


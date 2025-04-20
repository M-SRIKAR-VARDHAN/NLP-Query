# from typing import List, Dict
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
# from store import collection
# from embeddings import get_embedding
# import traceback

# app = FastAPI()

# # --- 1) Pydantic models for request & response --------------------------------

# class RecommendRequest(BaseModel):
#     query: str = Field(..., description="Job description or natural-language query")
#     k: int = Field(10, ge=1, le=10, description="Number of recommendations desired (1–10)")

# class Assessment(BaseModel):
#     url: str
#     adaptive_support: str
#     description: str
#     duration: int
#     remote_support: str
#     test_type: List[str]

# class RecommendResponse(BaseModel):
#     recommended_assessments: List[Assessment]

# # --- 2) Standalone recommend() function ---------------------------------------
# def recommend(query: str, k: int = 10) -> List[Dict]:
#     print(f"🔍 Embedding query: {query}")
#     q_emb = get_embedding(query)
#     print(f"✅ Got embedding: {q_emb[:5]}...")

#     results = collection.query(
#         query_embeddings=[q_emb],
#         n_results=k
#     )
#     print("📦 Query results keys:", results.keys())

#     metadatas = results["metadatas"][0]
#     documents = results["documents"][0]
#     print(f"📝 Found {len(metadatas)} assessments")

#     formatted = []
#     for md in metadatas:
#         try:
#             item = {
#                 "url": md["URL"],
#                 "adaptive_support": "Yes" if md["Adaptive/IRT"] == "Yes" else "No",
#                 "description": md["Name"],
#                 "duration": int(md["Time (Minutes)"]),
#                 "remote_support": "Yes" if md["Remote Testing"] == "Yes" else "No",
#                 "test_type": [t.strip() for t in md["Test Type"].split(",")]
#             }
#             formatted.append(item)
#         except Exception as e:
#             print("❌ Error parsing metadata:", md)
#             print("❗ Exception:", e)
#             raise e

#     return formatted

# # --- 3) Health check endpoint -------------------------------------------------

# @app.get("/health")
# def health():
#     return {"status": "healthy"}

# # --- 4) Recommend endpoint ----------------------------------------------------

# @app.post("/recommend", response_model=RecommendResponse)
# def recommend_endpoint(req: RecommendRequest):
#     print("Received query:", req.query)
#     print("Top K:", req.k)

#     if not req.query.strip():
#         raise HTTPException(status_code=400, detail="Query must not be empty")

#     results = recommend(req.query, req.k)

#     print("Recommendation results:", results)

#     if len(results) == 0:
#         raise HTTPException(status_code=404, detail="No assessments found")

# #     return {"recommended_assessments": results}
# from typing import List, Dict
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
# from store import collection
# from embeddings import get_embedding
# import traceback

# app = FastAPI()

# # --- 1) Pydantic models for request & response --------------------------------

# class RecommendRequest(BaseModel):
#     query: str = Field(..., description="Job description or natural-language query")
#     k: int = Field(10, ge=1, le=10, description="Number of recommendations desired (1–10)")

# class Assessment(BaseModel):
#     url: str
#     adaptive_support: str
#     description: str
#     duration: int
#     remote_support: str
#     test_type: List[str]

# class RecommendResponse(BaseModel):
#     recommended_assessments: List[Assessment]

# # --- 2) Standalone recommend() function ---------------------------------------
# def recommend(query: str, k: int = 10, remote_only=False, max_duration=None) -> List[Dict]:
#     q_emb = get_embedding(query)
#     results = collection.query(query_embeddings=[q_emb], n_results=k*2)  # pull extras to allow filtering

#     metadatas = results["metadatas"][0]

#     formatted = []
#     for md in metadatas:
#         try:
#             duration = int(md["Time"])
#             remote = md["Remote Testing"] == "Yes"

#             # Apply filters
#             if remote_only and not remote:
#                 continue
#             if max_duration is not None and duration > max_duration:
#                 continue

#             item = {
#                 "url": md["URL"],
#                 "adaptive_support": "Yes" if md["Adaptive/IRT"] == "Yes" else "No",
#                 "description": md["Name"],
#                 "duration": duration,
#                 "remote_support": "Yes" if remote else "No",
#                 "test_type": [t.strip() for t in md["Test Type"].split(",")]
#             }
#             formatted.append(item)

#         except Exception as e:
#             print("Error:", e)

#     return formatted[:k]


# # --- 3) Health check endpoint -------------------------------------------------

# @app.get("/health")
# def health():
#     return {"status": "healthy"}

# # --- 4) Recommend endpoint ----------------------------------------------------

# @app.post("/recommend", response_model=RecommendResponse)
# def recommend_endpoint(req: RecommendRequest):
#     print("Received query:", req.query)
#     print("Top K:", req.k)

#     if not req.query.strip():
#         raise HTTPException(status_code=400, detail="Query must not be empty")

#     results = recommend(req.query, req.k)

#     print("Recommendation results:", results)

#     if len(results) == 0:
#         raise HTTPException(status_code=404, detail="No assessments found")

#     return {"recommended_assessments": results}
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from store import collection
from embeddings import get_embedding
import traceback

app = FastAPI()

# --- 1) Pydantic models for request & response --------------------------------

class RecommendRequest(BaseModel):
    query: str = Field(..., description="Job description or natural-language query")
    k: int = Field(10, ge=1, le=10, description="Number of recommendations desired (1–10)")
    remote_only: bool = Field(False, description="If true, only include remote assessments")
    max_duration: int | None = Field(None, description="Max duration in minutes (optional)")

class Assessment(BaseModel):
    url: str
    adaptive_support: str
    description: str
    duration: int
    remote_support: str
    test_type: List[str]

class RecommendResponse(BaseModel):
    recommended_assessments: List[Assessment]

# --- 2) Root endpoint ----------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to the SHL API!"}

# --- 3) Standalone recommend() function ---------------------------------------

def recommend(query: str, k: int = 10, remote_only=False, max_duration=None) -> List[Dict]:
    q_emb = get_embedding(query)
    results = collection.query(query_embeddings=[q_emb], n_results=k*2)  # Pull extras to allow filtering

    metadatas = results["metadatas"][0]

    formatted = []
    for md in metadatas:
        try:
            # Debugging step: Let's print the metadata to inspect it
            print(f"Metadata: {md}")

            # Ensure we handle the 'Time (Minutes)' key correctly (check for exact name)
            duration = md.get("Time", None)  # Get duration if exists, None otherwise
            if duration is None:  # Skip entries that don't have a duration
                print("❌ Missing 'Time' field, skipping this entry.")
                continue

            duration = int(duration)  # Ensure it's an integer
            remote = md.get("Remote Testing") == "Yes"

            # Apply filters
            if remote_only and not remote:
                continue
            if max_duration is not None and duration > max_duration:
                continue

            item = {
                "url": md.get("URL", ""),
                "adaptive_support": "Yes" if md.get("Adaptive/IRT") == "Yes" else "No",
                "description": md.get("Name", ""),
                "duration": duration,
                "remote_support": "Yes" if remote else "No",
                "test_type": [t.strip() for t in md.get("Test Type", "").split(",")]
            }
            formatted.append(item)

        except Exception as e:
            print(f"Error processing metadata: {e}")
            print(f"Metadata: {md}")

    return formatted[:k]

# --- 4) Health check endpoint -------------------------------------------------

@app.get("/health")
def health():
    return {"status": "healthy"}

# --- 5) Recommend endpoint ----------------------------------------------------

@app.post("/recommend", response_model=RecommendResponse)
def recommend_endpoint(req: RecommendRequest):
    print("Received query:", req.query)
    print("Top K:", req.k)

    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")

    results = recommend(
        query=req.query,
        k=req.k,
        remote_only=req.remote_only,
        max_duration=req.max_duration
    )

    if len(results) == 0:
        raise HTTPException(status_code=404, detail="No assessments found")

    return {"recommended_assessments": results}

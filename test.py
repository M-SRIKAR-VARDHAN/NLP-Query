# test.py

from api import recommend  # Import the recommend function

test_set = [
    {
        "query": "remote numerical test for entry-level roles",
        "relevant_urls": [
            "https://www.shl.com/solutions/products/product-catalog/view/apprentice-8-0-job-focused-assessment/"
        ],
        "remote_only": True,
        "max_duration": 30
    },
    {
        "query": "cognitive ability screen for engineers",
        "relevant_urls": [
            "https://www.shl.com/solutions/products/product-catalog/view/interviewing-and-hiring-concepts-u-s/"
        ],
        "remote_only": False,
        "max_duration": None
    },
]

# Define the evaluation metrics
def recall_at_k(relevant, retrieved, k):
    retrieved_at_k = retrieved[:k]
    return len(set(relevant) & set(retrieved_at_k)) / len(set(relevant))

def average_precision_at_k(relevant, retrieved, k):
    score = 0.0
    hits = 0
    for i in range(k):
        if i < len(retrieved) and retrieved[i] in relevant:
            hits += 1
            score += hits / (i + 1)
    return score / min(len(relevant), k)

# Evaluation loop
recalls = []
maps = []

for case in test_set:
    # Call the recommend function with remote_only and max_duration filters
    results = recommend(
        query=case["query"],
        k=3,
        remote_only=case.get("remote_only", False),
        max_duration=case.get("max_duration", None)
    )
    
    # Extract retrieved URLs for comparison
    retrieved_urls = [r["url"] for r in results]
    relevant_urls = case["relevant_urls"]

    # Calculate recall and average precision at K
    recall = recall_at_k(relevant_urls, retrieved_urls, 3)
    ap = average_precision_at_k(relevant_urls, retrieved_urls, 3)

    # Print the evaluation results
    print(f"Query: {case['query']}")
    print(f"Recall@3: {recall:.2f} | AP@3: {ap:.2f}")
    print("-" * 50)  # Separator for better readability
    recalls.append(recall)
    maps.append(ap)

# Calculate mean recall and mean average precision
mean_recall = sum(recalls) / len(recalls)
mean_ap = sum(maps) / len(maps)

# Print final evaluation scores
print("\n📊 Final Scores:")
print(f"Mean Recall@3: {mean_recall:.3f}")
print(f"MAP@3: {mean_ap:.3f}")

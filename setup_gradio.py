"""
Setup script to initialize the DSA Mentor Gradio app
This script will load the expert solutions dataset into ChromaDB
"""

import json
import os
import chromadb
from sentence_transformers import SentenceTransformer

def setup_expert_solutions():
    """Load expert solutions into ChromaDB"""
    
    # Initialize ChromaDB
    chroma_client = chromadb.PersistentClient(path="D:/Projects/DSA Mentor/chroma_data")
    EXPERT_SOLUTION_collection = chroma_client.get_or_create_collection(
        name="expert_solutions",
        metadata={"description": "Expert algorithm solutions and explanations"}
    )
    
    # Initialize embedding model
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Load expert data
    EXPERT_SOLUTION_DATASET = "data_set/striver_sde/problems.json"
    
    if not os.path.exists(EXPERT_SOLUTION_DATASET):
        print(f"❌ Expert dataset not found at {EXPERT_SOLUTION_DATASET}")
        print("Please make sure the dataset file exists.")
        return False
    
    with open(EXPERT_SOLUTION_DATASET, "r", encoding="utf-8") as f:
        expert_data = json.load(f)
    
    print(f"✅ Loaded {len(expert_data)} problems from dataset.")
    
    # Prepare documents for ChromaDB
    EXPERT_SOLUTION_documents = []
    EXPERT_SOLUTION_metadatas = []
    EXPERT_SOLUTION_ids = []
    
    for idx, item in enumerate(expert_data):
        # Create a combined document text for better semantic retrieval
        combined_text = f"""
Problem: {item.get('problem_title', '')}
Difficulty: {item.get('difficulty', '')}
Topic: {item.get('topic', '')}

Problem Statement:
{item.get('problem_statement', '')}

Brute Force Approach:
{item.get('brute_force_explanation', '')}

Better Approach:
{item.get('better_approach', '')}

Optimized Explanation:
{item.get('optimized_explanation', '')}

Key Idea:
{item.get('key_idea', '')}
"""
        
        EXPERT_SOLUTION_documents.append(combined_text)
        EXPERT_SOLUTION_metadatas.append({
            "problem_title": item.get("problem_title", ""),
            "difficulty": item.get("difficulty", ""),
            "topic": item.get("topic", ""),
        })
        EXPERT_SOLUTION_ids.append(f"expert_{idx}")
    
    # Generate embeddings
    print("🔄 Generating embeddings...")
    EXPERT_SOLUTION_embeddings = embedding_model.encode(EXPERT_SOLUTION_documents, show_progress_bar=True).tolist()
    
    # Add to ChromaDB
    EXPERT_SOLUTION_collection.add(
        documents=EXPERT_SOLUTION_documents,
        metadatas=EXPERT_SOLUTION_metadatas,
        ids=EXPERT_SOLUTION_ids,
        embeddings=EXPERT_SOLUTION_embeddings
    )
    
    print(f"✅ Successfully added {len(EXPERT_SOLUTION_documents)} expert solutions to ChromaDB")
    return True

if __name__ == "__main__":
    print("🚀 Setting up DSA Mentor Gradio App...")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("❌ .env file not found!")
        print("Please create a .env file with your API key:")
        print("ZnapAI_API_KEY=your_api_key_here")
        exit(1)
    
    # Setup expert solutions
    if setup_expert_solutions():
        print("✅ Setup complete! You can now run the Gradio app with:")
        print("python gradio_app.py")
    else:
        print("❌ Setup failed. Please check the error messages above.")

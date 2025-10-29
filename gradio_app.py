import gradio as gr
import os
import json
import sys
import importlib
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from sentence_transformers import SentenceTransformer
import memory_manager
from memory_manager import create_memory_entry, update_memory_entry, find_existing_memory, load_memory

# Load environment variables
load_dotenv(override=True)

# Initialize components
api_key = os.getenv('ZnapAI_API_KEY')
MODEL = 'gpt-4o-mini'
openai = OpenAI(
    api_key=api_key,
    base_url="https://api.znapai.com/"
)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Set cache directories
os.environ["HF_HOME"] = "D:/huggingface_cache"
os.environ["TRANSFORMERS_CACHE"] = "D:/huggingface_cache"
os.environ["TORCH_HOME"] = "D:/huggingface_cache"
os.environ["CHROMA_CACHE_DIR"] = "D:/chroma_cache"

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="D:/Projects/DSA Mentor/chroma_data")
user_collection = chroma_client.get_or_create_collection(name="mentor_memory")
EXPERT_SOLUTION_collection = chroma_client.get_or_create_collection(name="expert_solutions")

# System prompts
SYSTEM_PROMPT_DIAGNOSE = """You are a precise DSA problem analyzer.
Given a user's code and problem statement, extract the conceptual mistakes,
edge cases missed, and reasoning flaws. Return a short structured JSON summary like:

{
  "mistake_summary": "<one-line summary>",
  "issues": [
    {"type": "edge-case", "confidence": "high", "evidence": "..."},
    {"type": "logic-gap", "confidence": "medium", "evidence": "..."}
  ]
}"""

SYSTEM_PROMPT_FEEDBACK = """You are a senior DSA mentor.
Use the given user's mistakes and retrieved past mistakes to guide them.
Do not give the full solution directly — nudge them toward the right logic.
If a past mistake pattern repeats, point it out and explain how to fix their thinking."""

# Utility functions
def embed_text(text, embedding_model=embedding_model):
    return embedding_model.encode([text])[0].tolist()

def retrieve_similar_memories_chroma(user_collection, query_text, top_k=3):
    results = user_collection.query(
        query_texts=[query_text],
        n_results=top_k
    )
    
    retrieved = []
    for i in range(len(results["ids"][0])):
        retrieved.append((
            results["ids"][0][i],
            results["documents"][0][i],
            float(results["distances"][0][i])
        ))
    return retrieved

def build_retrieval_context(retrieved_memories, mistake_summary, top_n=3):
    context = "Here are the user's most relevant past mistakes:\n\n"
    for idx, (mid, text, score) in enumerate(retrieved_memories[:top_n]):
        context += f"Memory {idx+1} (similarity: {1 - score:.2f}):\n{text}\n\n"
    context += "Use this information to tailor your feedback for the current problem.\n\n"
    context += f"User's current mistake summary:\n{mistake_summary}"
    return context

def get_diagnosis(user_code):
    diagnosis = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_DIAGNOSE},
            {"role": "user", "content": user_code}
        ]
    )
    try:
        diagnosis_json = json.loads(diagnosis.choices[0].message.content)
    except json.JSONDecodeError:
        print("⚠️ Could not parse model output as JSON. Using raw text fallback.")
        diagnosis_json = {"mistake_summary": diagnosis.choices[0].message.content, "issues": []}
    return diagnosis_json

def retrieve_expert_context(query, embedding_model, collection, top_k=3):
    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    context = ""
    for i in range(len(results["documents"][0])):
        meta = results["metadatas"][0][i]
        doc = results["documents"][0][i]

        context += f"\n\nExpert Solution {i+1}:\n"
        context += f"Problem: {meta.get('problem_title', 'Unknown')}\n"
        context += doc[:1500]

    return context.strip()

def get_mentor_feedback(mentor_context, expert_context):
    final_prompt = f"""

The user made the following mistake:
{mentor_context}

Here are some relevant expert solutions from a trusted dataset:
{expert_context}

Using this information, give the user clear, structured feedback on:
1. What they missed or misunderstood.
2. How they can improve.
3. Step-by-step reasoning toward an optimal approach.
    """

    feedback = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_FEEDBACK},
            {"role": "user", "content": final_prompt}
        ]
    )
    response = feedback.choices[0].message.content
    return response

def mentor_pipeline(problem_title, user_code):
    """Runs full reasoning–retrieval–feedback pipeline."""
    
    # STEP 1 — Diagnose user's logic
    diagnosis_json = get_diagnosis(user_code)
    mistake_summary = diagnosis_json["mistake_summary"]
    
    # STEP 2 — Retrieve from ChromaDB
    similar_memories = retrieve_similar_memories_chroma(user_collection, mistake_summary, top_k=3)

    # STEP 3.a — Build mentor context
    mentor_context = build_retrieval_context(similar_memories, mistake_summary)

    # STEP 3.b - Retrieve expert context
    expert_context = retrieve_expert_context(mistake_summary, embedding_model, EXPERT_SOLUTION_collection, top_k=3)

    # STEP 4 — Generate mentor-style feedback
    mentor_feedback = get_mentor_feedback(mentor_context, expert_context)
    
    # STEP 5 — Store this new memory
    vector = embed_text(mistake_summary)
    user_collection.add(
        ids=[f"{problem_title}_{len(user_collection.get()['ids'])}"],
        documents=[f"Problem: {problem_title}\nMistake Summary: {mistake_summary}\nIssues: {diagnosis_json['issues']}"],
        embeddings=[vector]
    )
    
    return mentor_feedback

def process_code(problem_title, user_code, language):
    """Process user code and return mentor feedback"""
    if not problem_title.strip() or not user_code.strip():
        return "Please provide both a problem title and your code."
    
    try:
        # Format the user message similar to the notebook
        user_msg = f"""
Problem: {problem_title}
Language: {language}
My reasoning: Please analyze my approach
Outcome: Needs analysis
Code:
{user_code}
"""
        
        feedback = mentor_pipeline(problem_title, user_msg)
        return feedback
    except Exception as e:
        return f"Error processing your code: {str(e)}"

# Create Gradio interface
def create_interface():
    with gr.Blocks(
        title="DSA Mentor",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: auto !important;
        }
        .main-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .problem-section {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .code-section {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        """
    ) as interface:
        
        gr.HTML("""
        <div class="main-header">
            <h1>🎯 DSA Mentor</h1>
            <p>Get personalized feedback on your algorithmic problem-solving approach</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML('<div class="problem-section">')
                problem_title = gr.Textbox(
                    label="Problem Title",
                    placeholder="e.g., Two Sum, Remove Nth Node From End of List",
                    lines=1
                )
                language = gr.Dropdown(
                    choices=["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust"],
                    value="Python",
                    label="Programming Language"
                )
                gr.HTML('</div>')
                
                gr.HTML('<div class="code-section">')
                user_code = gr.Textbox(
                    label="Your Code",
                    placeholder="Paste your solution here...",
                    lines=15,
                    max_lines=20
                )
                gr.HTML('</div>')
                
                submit_btn = gr.Button("Get Feedback", variant="primary", size="lg")
                
            with gr.Column(scale=1):
                feedback_output = gr.Textbox(
                    label="Mentor Feedback",
                    lines=20,
                    max_lines=25,
                    interactive=False,
                    show_copy_button=True
                )
        
        # Example problems
        with gr.Accordion("💡 Example Problems", open=False):
            gr.HTML("""
            <div style="padding: 1rem;">
                <h4>Try these example problems:</h4>
                <ul>
                    <li><strong>Two Sum:</strong> Given an array of integers, return indices of the two numbers that add up to a target.</li>
                    <li><strong>Remove Nth Node From End of List:</strong> Remove the nth node from the end of a linked list.</li>
                    <li><strong>Valid Parentheses:</strong> Check if a string of parentheses is valid.</li>
                    <li><strong>Maximum Subarray:</strong> Find the contiguous subarray with maximum sum.</li>
                </ul>
            </div>
            """)
        
        # Connect the submit button
        submit_btn.click(
            fn=process_code,
            inputs=[problem_title, user_code, language],
            outputs=feedback_output
        )
        
        # Add some example data
        gr.Examples(
            examples=[
                ["Two Sum", "def two_sum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i+1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]", "Python"],
                ["Remove Nth Node From End of List", "var removeNthFromEnd = function(head, n) {\n    if(head.next == null) return null;\n    let slow = head, fast = head;\n    while(n > 0 && fast.next) {\n        fast = fast.next;\n        n--;\n    }\n    while(fast.next) {\n        slow = slow.next;\n        fast = fast.next;\n    }\n    slow.next = slow.next.next;\n    return head;\n};", "JavaScript"]
            ],
            inputs=[problem_title, user_code, language]
        )
    
    return interface

if __name__ == "__main__":
    # Create and launch the interface
    interface = create_interface()
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )

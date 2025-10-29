"""
Simplified DSA Mentor Gradio App
This version has minimal dependencies and focuses on the core functionality
"""

import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

def process_code_simple(problem_title, user_code, language):
    """Simplified code processing without AI analysis"""
    if not problem_title.strip() or not user_code.strip():
        return "Please provide both a problem title and your code."
    
    # Simple analysis without AI
    analysis = f"""
Problem Analysis for: {problem_title}
Language: {language}

Code Review:
- Code length: {len(user_code)} characters
- Lines of code: {len(user_code.split(chr(10)))}
- Language: {language}

Common things to check:
1. Edge cases (empty inputs, single elements, etc.)
2. Boundary conditions (array bounds, loop termination)
3. Time complexity (is it optimal?)
4. Space complexity (can it be improved?)
5. Correct data structures for the problem
6. Proper initialization of variables
7. Loop conditions and termination

For detailed AI-powered feedback, please ensure all dependencies are installed and run the full version.
"""
    
    return analysis

def create_simple_interface():
    """Create a simple Gradio interface"""
    try:
        import gradio as gr
        
        with gr.Blocks(title="DSA Mentor - Simple Version") as interface:
            gr.HTML("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1>DSA Mentor - Simple Version</h1>
                <p>Get basic feedback on your algorithmic problem-solving approach</p>
            </div>
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
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
                    user_code = gr.Textbox(
                        label="Your Code",
                        placeholder="Paste your solution here...",
                        lines=15,
                        max_lines=20
                    )
                    submit_btn = gr.Button("Get Basic Feedback", variant="primary", size="lg")
                
                with gr.Column(scale=1):
                    feedback_output = gr.Textbox(
                        label="Basic Analysis",
                        lines=20,
                        max_lines=25,
                        interactive=False,
                        show_copy_button=True
                    )
            
            # Connect the submit button
            submit_btn.click(
                fn=process_code_simple,
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
        
    except ImportError:
        print("Gradio not available. Please install it with: pip install gradio")
        return None

def main():
    """Main function to run the app"""
    print("Starting DSA Mentor - Simple Version...")
    
    # Check if API key is available
    api_key = os.getenv('ZnapAI_API_KEY')
    if not api_key:
        print("Warning: No API key found. Running in basic mode only.")
    
    # Create and launch interface
    interface = create_simple_interface()
    if interface:
        print("Launching Gradio interface...")
        interface.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            show_error=True
        )
    else:
        print("Failed to create interface. Please install Gradio.")

if __name__ == "__main__":
    main()

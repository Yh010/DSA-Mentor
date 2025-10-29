"""
Simple test script to verify Gradio app functionality
"""

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import gradio as gr
        print("Gradio imported successfully")
    except ImportError as e:
        print(f"Failed to import Gradio: {e}")
        return False
    
    try:
        import os
        import json
        import sys
        import importlib
        from dotenv import load_dotenv
        from openai import OpenAI
        import chromadb
        from sentence_transformers import SentenceTransformer
        import memory_manager
        print("All other modules imported successfully")
    except ImportError as e:
        print(f"Failed to import required module: {e}")
        return False
    
    return True

def test_environment():
    """Test if environment variables are set"""
    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    api_key = os.getenv('ZnapAI_API_KEY')
    if not api_key:
        print("ZnapAI_API_KEY not found in environment")
        return False
    else:
        print("API key found in environment")
        return True

if __name__ == "__main__":
    print("Testing DSA Mentor Gradio App...")
    
    if test_imports() and test_environment():
        print("All tests passed! The app should work correctly.")
        print("\nTo run the app:")
        print("python gradio_app.py")
    else:
        print("Some tests failed. Please check the issues above.")

"""
Launch script for DSA Mentor Gradio App
This script will run the Gradio app using the same environment as the notebook
"""

import subprocess
import sys
import os

def launch_gradio_app():
    """Launch the Gradio app"""
    try:
        # Try to run the gradio app
        result = subprocess.run([
            sys.executable, "gradio_app.py"
        ], check=True, capture_output=True, text=True)
        
        print("Gradio app launched successfully!")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Error launching Gradio app: {e}")
        print(f"Error output: {e.stderr}")
        print("\nTrying alternative approach...")
        
        # Alternative: Run with explicit module
        try:
            subprocess.run([
                sys.executable, "-m", "gradio", "gradio_app.py"
            ], check=True)
        except subprocess.CalledProcessError as e2:
            print(f"Alternative approach also failed: {e2}")
            print("\nPlease try running manually:")
            print("python gradio_app.py")
            
    except FileNotFoundError:
        print("Gradio app file not found. Please make sure gradio_app.py exists.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    print("Launching DSA Mentor Gradio App...")
    launch_gradio_app()

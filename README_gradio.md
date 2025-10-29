# DSA Mentor - Gradio Frontend

A minimalistic web interface for the DSA Mentor system using Gradio. This frontend provides an intuitive way to get personalized feedback on your algorithmic problem-solving approach.

## Features

- 🎯 **Clean Interface**: Simple, focused UI for submitting code
- 🧠 **Smart Analysis**: AI-powered mistake detection and feedback
- 📚 **Expert Solutions**: Integration with curated expert solutions
- 🔄 **Memory System**: Learns from your past mistakes to provide better guidance
- 🌐 **Web-based**: Easy to use in any browser

## Two Versions Available

### Full Version (Recommended)
Complete AI-powered analysis with memory system and expert solutions.

### Simple Version
Basic analysis without AI dependencies - perfect for quick setup and testing.

## Quick Start

### Option 1: Simple Version (Easiest)

1. **Install Gradio only:**
   ```bash
   pip install gradio
   ```

2. **Run the simple version:**
   ```bash
   python simple_gradio_app.py
   ```

3. **Open your browser to:** `http://localhost:7860`

### Option 2: Full Version (Complete Features)

1. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup environment:**
   Create a `.env` file in the project root:
   ```env
   ZnapAI_API_KEY=your_api_key_here
   ```

3. **Initialize the system:**
   ```bash
   python setup_gradio.py
   ```

4. **Launch the full app:**
   ```bash
   python gradio_app.py
   ```

5. **Open your browser to:** `http://localhost:7860`

## Usage

1. **Enter Problem Title**: Type the name of the problem you're working on
2. **Select Language**: Choose your programming language
3. **Paste Your Code**: Submit your solution or approach
4. **Get Feedback**: Receive personalized guidance and hints

## Example Problems

The interface includes example problems to get you started:

- **Two Sum**: Find two numbers that add up to a target
- **Remove Nth Node**: Remove the nth node from the end of a linked list
- **Valid Parentheses**: Check if parentheses are balanced
- **Maximum Subarray**: Find the contiguous subarray with maximum sum

## How It Works

1. **Code Analysis**: Your code is analyzed to identify mistakes and patterns
2. **Memory Retrieval**: The system looks up similar past mistakes you've made
3. **Expert Context**: Relevant expert solutions are retrieved for guidance
4. **Personalized Feedback**: AI generates tailored feedback based on your learning profile

## Customization

You can customize the interface by modifying `gradio_app.py`:

- **Theme**: Change the Gradio theme in the `create_interface()` function
- **Styling**: Modify the CSS in the `css` parameter
- **Layout**: Adjust the column ratios and component arrangement

## Troubleshooting

### Common Issues

1. **Gradio Import Error**: 
   - Try: `pip install gradio --upgrade`
   - Or: `pip3 install gradio`
   - Check Python version compatibility

2. **API Key Error**: 
   - Make sure your `.env` file contains the correct API key
   - Check that the `.env` file is in the project root directory

3. **ChromaDB Error**: 
   - Ensure the `chroma_data` directory exists and is writable
   - Try running `python setup_gradio.py` first

4. **Memory Issues**: 
   - If you get memory errors, try reducing the batch size in the embedding generation
   - Use the simple version if you're having dependency issues

5. **Python Environment Issues**:
   - Make sure you're using the same Python environment as your notebook
   - Try using `python -m pip install gradio` instead of just `pip install gradio`

### Quick Fixes

**If Gradio won't install:**
```bash
# Try different installation methods
python -m pip install gradio
pip3 install gradio
conda install gradio
```

**If you get import errors:**
```bash
# Check which Python you're using
python --version
which python

# Install for the correct Python version
python -m pip install gradio
```

**If the app won't start:**
```bash
# Try the simple version first
python simple_gradio_app.py

# Or check for missing dependencies
python test_gradio.py
```

### Reset Everything

To start fresh:

```bash
# Remove ChromaDB data
rm -rf chroma_data/

# Remove memory file
rm mentor_memory.json

# Re-run setup
python setup_gradio.py
```

## Development

The frontend is built with:

- **Gradio**: For the web interface
- **ChromaDB**: For vector storage and retrieval
- **Sentence Transformers**: For text embeddings
- **OpenAI API**: For AI-powered analysis

## Support

If you encounter any issues, check the console output for error messages. The system provides detailed logging to help diagnose problems.

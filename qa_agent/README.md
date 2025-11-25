# Autonomous QA Agent

An intelligent agent that builds a "testing brain" from project documentation and generates test cases and Selenium scripts.

## Features
- **Knowledge Base Ingestion**: Uploads and parses Markdown, Text, and JSON documents.
- **RAG Pipeline**: Uses ChromaDB and OpenAI to ground test cases in documentation.
- **Test Case Generation**: Generates comprehensive test plans based on user queries.
- **Selenium Script Generation**: Converts test cases into executable Python Selenium scripts using the target HTML structure.

## Prerequisites
- Python 3.9+
- OpenAI API Key

## Setup

1. **Clone the repository** (if applicable) or navigate to the project folder.

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set OpenAI API Key**:
   Export your API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Running the Application

The application consists of a FastAPI backend and a Streamlit frontend. You need to run both.

### 1. Setup
Run the setup script to install dependencies:
```bash
./setup.sh
```

### 2. Start the Backend
Open a terminal and run:
```bash
./run_backend.sh
```
The API will be available at `http://localhost:8000`.

### 3. Start the Frontend
Open a new terminal window and run:
```bash
./run_frontend.sh
```
The UI will open in your browser (usually at `http://localhost:8501`).

## Usage Guide

### Phase 1: Build Knowledge Base
1. Go to the **Knowledge Base** tab.
2. Click "Browse files" under "Upload Support Documents".
3. Select the provided assets from `qa_agent/assets`:
   - `product_specs.md`
   - `ui_ux_guide.txt`
   - `api_endpoints.json`
4. Click **Build Knowledge Base**. Wait for the success message.
5. Upload `checkout.html` in the "Target HTML" section.

### Phase 2: Generate Test Cases
1. Switch to the **Test Case Agent** tab.
2. Enter a prompt, e.g., *"Generate positive and negative test cases for the discount code feature."*
3. Click **Generate Test Cases**.
4. Review the generated test plan.

### Phase 3: Generate Selenium Script
1. Switch to the **Script Agent** tab.
2. Copy a specific test case from the previous step (e.g., the entire block for "TC-001").
3. Paste it into the text area.
4. Click **Generate Script**.
5. Copy the generated Python code and run it locally (ensure you have `chromedriver` installed).

## Project Structure
```
qa_agent/
├── assets/                 # Sample project files
│   ├── checkout.html
│   ├── product_specs.md
│   ├── ui_ux_guide.txt
│   └── api_endpoints.json
├── backend/
│   ├── main.py             # FastAPI app
│   └── rag.py              # RAG logic and LLM chains
├── frontend/
│   └── app.py              # Streamlit UI
├── requirements.txt
└── README.md
```

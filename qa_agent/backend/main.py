import os
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
import uvicorn
from rag import KnowledgeBase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Autonomous QA Agent API")

# Global instance of KnowledgeBase
kb = KnowledgeBase()

class TestCaseRequest(BaseModel):
    query: str

class ScriptRequest(BaseModel):
    test_case: str
    html_content: str

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    upload_dir = "uploads"
    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)
    os.makedirs(upload_dir)

    saved_files = []
    for file in files:
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        saved_files.append(file_path)
    
    try:
        kb.build_knowledge_base(saved_files)
        return {"message": f"Knowledge Base built successfully with {len(saved_files)} files."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-test-cases")
async def generate_test_cases(request: TestCaseRequest):
    """
    Generates test cases based on the query and knowledge base.
    """
    try:
        result = kb.generate_test_cases(request.query)
        return {"test_cases": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-script")
async def generate_script(request: ScriptRequest):
    """
    Generates a Selenium script for a specific test case.
    """
    try:
        script = kb.generate_selenium_script(request.test_case, request.html_content)
        return {"script": script}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

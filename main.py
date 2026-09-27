from fastapi import FastAPI, UploadFile, File, HTTPException
import google.generativeai as genai
import os
from PIL import Image
import io

app = FastAPI()

# It will take the key from the server's environment 
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

@app.get("/")
def home():
    return {"status": "Server is running perfectly!"}

@app.post("/process-document")
async def process_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([
            "Extract all text from this document image cleanly and provide a structured summary.",
            image
        ])
        return {"extracted_text": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
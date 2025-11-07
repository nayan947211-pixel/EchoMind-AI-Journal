from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import uvicorn

# --- 1. Initialize Your Application ---
app = FastAPI(
    title="EchoMind AI Co-Pilot",
    description="API for the AI-powered emotional co-pilot.",
)

# --- 2. Load Your AI Models (Pipelines) ---
# This can take a moment when the server first starts.
print("Loading Conversational model (google/flan-t5-small)...")
chatbot_pipeline = pipeline(
    "text2text-generation", 
    model="google/flan-t5-small"
)

print("Loading Emotion Analysis model (j-hartmann/emotion-english-distilroberta-base)...")
emotion_pipeline = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=3  # Return the top 3 potential emotions
)
print("--- All models loaded successfully. Server is ready. ---")


# --- 3. Define Your API Input/Output ---
class JournalEntry(BaseModel):
    text: str

# --- 4. Create Your API Endpoints ---

@app.get("/")
def read_root():
    """A simple root endpoint to check if the server is running."""
    return {"message": "Welcome to the EchoMind API. Go to /docs to test."}


@app.post("/chat")
def get_chat_response(entry: JournalEntry):
    """
    Module 1: The Conversational Journal.
    Takes user text and returns an empathetic response.
    """
    # We add a "prompt" to guide the small LLM to be empathetic.
   # This is the NEW prompt
    prompt = f"Generate a short, empathetic, and supportive response to the following journal entry: '{entry.text}'"
    
    try:
        response = chatbot_pipeline(prompt, max_length=100, num_return_sequences=1)
        ai_response = response[0]['generated_text']
        
        return {"user_text": entry.text, "ai_response": ai_response}
        
    except Exception as e:
        return {"error": str(e)}


@app.post("/analyze")
def get_emotion_analysis(entry: JournalEntry):
    """
    Module 2: The Deep Emotion Analysis Engine.
    Takes user text and returns the detected emotions.
    """
    try:
        analysis = emotion_pipeline(entry.text)
        
        return {"user_text": entry.text, "analysis": analysis}
        
    except Exception as e:
        return {"error": str(e)}
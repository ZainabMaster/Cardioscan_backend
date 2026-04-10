from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Enable CORS for your React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NEW: Root Route to prevent "Not Found" error ---
@app.get("/")
def read_root():
    return {"status": "Online", "message": "CardioScan API is active. Go to /docs to test."}

# --- Tab 1: Risk Profiler ---
class RiskInput(BaseModel):
    age: int
    bp: int
    bmi: float
    smoker: bool
    drinking: str
    sleep: int
    diet: str

@app.post("/analyze-risk")
async def analyze_risk(data: RiskInput):
    risk_lvl = "High" if data.bp > 140 or data.smoker else "Low"
    return {
        "risk": risk_lvl,
        "routine": "30 mins cardio daily, low salt diet",
        "precautions": "Monitor BP weekly",
        "exercise": "Brisk Walking"
    }

# --- Tab 2: MRI Scan ---
@app.post("/scan-mri")
async def scan_mri(file: UploadFile = File(...)):
    return {"analysis": "No significant anomalies detected", "confidence": "94%"}

# --- Tab 3: Report Translator ---
@app.post("/translate-report")
async def translate_report(file: UploadFile = File(...), language: str = Form(...)):
    explanations = {
        "hindi": "आपका रिपोर्ट सामान्य है। (Report is normal)",
        "marathi": "तुमचा रिपोर्ट सामान्य आहे।"
    }
    return {
        "summary": "Heart valves are healthy.",
        "translation": explanations.get(language, "Language not supported")
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
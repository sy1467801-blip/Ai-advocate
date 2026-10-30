import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from openai import OpenAI

BASE_DIR = Path(__file__).parent
app = FastAPI(title="AI Vakeel", version="0.1.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

SYSTEM_PROMPT = """
You are AI Vakeel, an Indian-law information and document-drafting assistant for citizens,
advocates and law students. Support English and Hindi; answer in the user's chosen language.
Be careful, clear, and practical. Ask for missing facts when they materially affect the answer.
Distinguish legal information from legal advice. Do not claim to be a lawyer or guarantee outcomes.
Never invent legislation, section numbers, judgments, citations, court rules, deadlines, or facts.
If uncertain or current law needs verification, say so and point to official sources.
Prefer primary sources: India Code (indiacode.nic.in), Supreme Court of India (sci.gov.in),
eCourts (ecourts.gov.in), and the relevant High Court or government department.
Mention jurisdiction, relevant dates, and potential exceptions when material.
For documents, use placeholders for unknown facts, do not fabricate facts, and label drafts
as requiring review. For urgent danger or imminent deadlines, recommend contacting a qualified
advocate or appropriate emergency authority promptly.
Do not imply an answer is guaranteed to be complete or suitable for filing without review.
"""

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    language: str = "English"
    mode: str = "legal"
    jurisdiction: str = "India"
    context: str = ""

@app.get("/", response_class=HTMLResponse)
def home():
    return (BASE_DIR / "static" / "index.html").read_text(encoding="utf-8")

@app.get("/health")
def health():
    return {"status": "ok", "app": "AI Vakeel"}

@app.post("/api/assist")
def assist(req: ChatRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured. Follow the README setup steps.")
    try:
        client = OpenAI(api_key=api_key)
        mode_instructions = {
            "legal": "Answer the legal question with a short summary, relevant legal framework, practical next steps, and verification sources.",
            "document": "Draft the requested legal or formal document. Use a professional Indian format, clear headings, placeholders for missing details, an enclosure list if useful, and a checklist of details to verify. State that it is a draft for review.",
            "case": "Analyze the supplied case facts or text. Separate stated facts, issues, possible arguments for each side, missing evidence, procedural questions, and next steps. Do not predict a guaranteed outcome.",
            "research": "Provide a research plan and identify official sources to verify. Cite a statute or judgment only when you are confident it exists and is relevant; clearly mark anything requiring verification."
        }.get(req.mode, "Answer carefully and helpfully.")
        prompt = f"""Language: {req.language}
Jurisdiction/state: {req.jurisdiction}
Task mode: {req.mode}
Instruction: {mode_instructions}
Additional context: {req.context or 'None supplied'}
User request:
{req.message}
"""
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            instructions=SYSTEM_PROMPT,
            input=prompt,
        )
        return {"answer": response.output_text, "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini")}
    except HTTPException:
        raise
    except Exception as exc:
        # Avoid leaking secrets or stack traces to the browser.
        raise HTTPException(status_code=502, detail="The AI service request failed. Check server logs and API configuration.") from exc

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.database import SessionLocal
from app import models

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Flashcard API"}

# Subject inference (rule-based)
def infer_subject(text):
    text = text.lower()
    if "photosynthesis" in text or "cell" in text or "organism" in text:
        return "Biology"
    elif "force" in text or "acceleration" in text or "gravity" in text or "newton" in text:
        return "Physics"
    elif "algorithm" in text or "programming" in text or "python" in text:
        return "Computer Science"
    elif "equation" in text or "calculus" in text or "geometry" in text:
        return "Mathematics"
    else:
        return "General"

# Request model
class FlashcardRequest(BaseModel):
    student_id: str
    question: str
    answer: str

@app.post("/flashcard")
def add_flashcard(card: FlashcardRequest):
    subject = infer_subject(card.question)
    db = SessionLocal()
    flashcard = models.Flashcard(
        student_id=card.student_id,
        question=card.question,
        answer=card.answer,
        subject=subject
    )
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    db.close()
    return {
        "message": "Flashcard added successfully",
        "subject": subject
    }

@app.get("/get-subject")
def get_flashcards(student_id: str, limit: int = 5):
    db = SessionLocal()
    flashcards = db.query(models.Flashcard).filter(models.Flashcard.student_id == student_id).all()
    db.close()
    import random
    random.shuffle(flashcards)
    seen_subjects = set()
    result = []
    for card in flashcards:
        if card.subject not in seen_subjects:
            result.append({
                "question": card.question,
                "answer": card.answer,
                "subject": card.subject
            })
            seen_subjects.add(card.subject)
        if len(result) >= limit:
            break
    return result

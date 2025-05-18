from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, database
from pydantic import BaseModel
import random

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema for input
class FlashcardCreate(BaseModel):
    student_id: str
    question: str
    answer: str

# Simple rule-based subject inference
def infer_subject(text: str) -> str:
    text = text.lower()
    if any(word in text for word in ["photosynthesis", "cell", "organism", "plant", "mitochondria"]):
        return "Biology"
    elif any(word in text for word in ["force", "velocity", "acceleration", "newton", "gravity"]):
        return "Physics"
    elif any(word in text for word in ["algorithm", "function", "variable", "python", "code"]):
        return "Computer Science"
    elif any(word in text for word in ["equation", "geometry", "calculus", "algebra", "matrix"]):
        return "Mathematics"
    else:
        return "General"

@app.post("/flashcard")
def create_flashcard(flashcard: FlashcardCreate, db: Session = Depends(get_db)):
    subject = infer_subject(flashcard.question)
    db_flashcard = models.Flashcard(
        student_id=flashcard.student_id,
        question=flashcard.question,
        answer=flashcard.answer,
        subject=subject
    )
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return {"message": "Flashcard added successfully", "subject": subject}

@app.get("/get-subject")
def get_flashcards(student_id: str, limit: int = 5, db: Session = Depends(get_db)):
    flashcards = db.query(models.Flashcard).filter(models.Flashcard.student_id == student_id).all()
    
    # Group by subject
    subject_map = {}
    for fc in flashcards:
        subject_map.setdefault(fc.subject, []).append(fc)

    # Randomly select flashcards from different subjects
    result = []
    while len(result) < limit and subject_map:
        for subject in list(subject_map.keys()):
            if subject_map[subject]:
                result.append(subject_map[subject].pop(0))
            if not subject_map[subject]:
                del subject_map[subject]
            if len(result) == limit:
                break

    random.shuffle(result)

    return [
        {
            "question": fc.question,
            "answer": fc.answer,
            "subject": fc.subject
        } for fc in result
    ]

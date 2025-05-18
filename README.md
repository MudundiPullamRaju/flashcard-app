# Flashcard Backend API

##  Overview

This is a backend API for a smart flashcard system. Users can add flashcards (question + answer), and the system automatically infers the subject based on keywords in the question. Students can later retrieve flashcards across multiple subjects, intelligently mixed.

---

##  Features

-  Add flashcards with automatic **subject inference** (Physics, Biology, Computer Science, Mathematics, General)
-  Retrieve flashcards for a student with a **mix of subjects**
-  Simple, rule-based keyword classification

---

##  Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/MudundiPullamRaju/flashcard-app.git
cd flashcard-app

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Run the Server
uvicorn main:app --reload

### Project Structure
flashcard-app/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│
├── main.py
├── requirements.txt
├── flashcards.db
├── README.md



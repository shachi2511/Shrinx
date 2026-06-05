# ShrinX — AI Study Assistant

Upload a PDF. Get summaries, flashcards, and quizzes — instantly.

![Home](screenshots/HomePage.png)

---

## What it does

ShrinX extracts text from any PDF, constructs structured prompts, and calls the Claude API to generate 7 study formats automatically — all parsed and served through a Flask web app.

**Generated formats:** Summary · Notes · Flashcards · MCQ · True/False · Fill-in-the-blank · Q&A

---

## Screenshots

![Upload](screenshots/pdf_upload.png)

![Summary](screenshots/Summary.png)

![Flashcards](screenshots/FlashCard.png)

![Quiz](screenshots/quiz.png)

---

## Stack

| | |
|---|---|
| Backend | Python, Flask |
| AI | Anthropic Claude API (`claude-sonnet-4-6`) |
| PDF | pdfplumber, PyPDF2 |
| Frontend | HTML, CSS, JavaScript, Marked.js |

---

## Setup

```bash
git clone https://github.com/shachi2511/Shrinx.git
cd Shrinx
pip install -r requirements.txt
```

Create a `.env` file:
```
ANTHROPIC_API_KEY=your_key_here
```

Run:
```bash
python app.py
```
Open `http://127.0.0.1:5000`

---

Built with the [Anthropic Claude API](https://www.anthropic.com)
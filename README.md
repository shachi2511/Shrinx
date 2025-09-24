ShrinX AI Study Assistant

📚 SHRINK THE STUDYING, EXPAND THE LEARNING 🚀

ShrinX is an AI-powered study buddy that transforms boring PDFs into summaries, detailed notes, flashcards, and interactive quizzes. Whether you’re cramming for exams or just revising, ShrinX helps you learn smarter, not harder.

✨ Features
Core Functionality

PDF Text Extraction: Extracts clean text from PDFs with PyPDF2 or pdfplumber

AI-Powered Generation: Uses Anthropic’s Claude API to create study materials

Multiple Formats: Generates summaries, notes, flashcards, and quizzes

Dual Interface: Run ShrinX in the terminal (full power) or GUI (quick use)

Study Materials Generated

📖 Summaries – Quick overviews of PDF chapters

📝 Detailed Notes – Bullet points + key concepts

🎴 Flashcards – Spaced repetition friendly

🎯 MCQs – Multiple choice quizzes with explanations

✍️ Fill-in-the-Blank – Cloze exercises

✅ True/False Questions – Binary quizzes with reasoning

❓ Q&A Pairs – Question-answer sets for deeper recall

🛠 Tech Stack

Python 3.6+

Libraries:

anthropic (Claude API)

PyPDF2 / pdfplumber

tkinter (GUI)

dotenv (API key management)


🎮 Interfaces
GUI (Quick + Simple)

Upload PDFs

Browse topics

View summaries, notes, and Q&A

Terminal (Full Power Mode)

Interactive flashcards with progress tracking

Complete quiz system (MCQ, Fill-in-the-Blank, True/False)

Advanced study session management

Topic/content organization

📈 How It Works

Upload PDF → ShrinX extracts the text

AI Processing → Claude generates summaries, notes, and quizzes

Study Time → Use flashcards, quizzes, and review tools

Track Progress → Monitor your learning over sessions

🚀 Future Enhancements

🌐 Full-featured GUI (with quizzes + flashcards)

🧠 Spaced repetition algorithm

📊 Study analytics + performance insights

📤 Export to Anki, Word, or mobile apps

🤝 Collaborative study modes

📱 Mobile app version

🔊 Voice integration for audio-based studying

🔒 Offline mode for local-only use

🐞 Troubleshooting

API Key Error → Check your .env file for a valid Anthropic key

PDF Not Extracting Well → Install pdfplumber for better parsing

GUI Won’t Start → Ensure tkinter is installed (usually bundled)

Import Errors → Run pip install -r requirements.txt

📜 License

Educational use only. Please follow Anthropic’s API terms of service.

🙌 Acknowledgments

Built on Anthropic’s Claude API

PDF parsing powered by PyPDF2 + pdfplumber

GUI built with tkinter

# ShrinX AI Study Assistant

**SHRINK THE STUDYING, EXPAND THE LEARNING!**

An AI-powered study assistant that transforms PDF documents into comprehensive study materials including summaries, notes, flashcards, and interactive quizzes.

## Features

### Core Functionality
- **PDF Text Extraction**: Extract text from PDF documents using PyPDF2 or pdfplumber
- **AI-Powered Content Generation**: Uses Anthropic's Claude API to generate study materials
- **Multiple Study Formats**: Creates summaries, detailed notes, flashcards, and various quiz types
- **Dual Interface**: Both GUI and terminal versions available

### Study Materials Generated
- **Summaries**: Concise overviews of PDF content
- **Detailed Notes**: Comprehensive study notes with bullet points and key concepts
- **Flashcards**: Interactive flashcard system with spaced repetition
- **Multiple Choice Questions**: AI-generated MCQ quizzes with explanations
- **Fill-in-the-Blank**: Cloze deletion exercises
- **True/False Questions**: Binary choice quizzes with explanations
- **Q&A Pairs**: Detailed question-answer sets

## Installation

### Prerequisites
- Python 3.6 or higher
- Anthropic API key

### Required Dependencies
```bash
pip install anthropic PyPDF2 python-dotenv
```

### Optional Dependencies
```bash
pip install pdfplumber  # Better PDF text extraction
pip install tkinter     # GUI support (usually included with Python)
```

### Setup
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

### GUI Version (Limited Features)
```bash
python main_launcher.py
```
or
```bash
python shrinx_gui.py
```

The GUI version provides:
- PDF upload interface
- Topic browsing
- Content viewing (summaries, notes, Q&A)
- Basic navigation

### Terminal Version (Full Features)
```bash
python main.py
```

The terminal version includes all features:
- Interactive flashcard study sessions
- Complete quiz systems (MCQ, Fill-in-blanks, True/False)
- Advanced study session management
- Progress tracking
- Content review and management

## Project Structure

```
shrinx/
├── main.py                 # Terminal interface (full features)
├── main_launcher.py        # Simple launcher with fallbacks
├── shrinx_gui.py          # GUI interface (basic features)
├── ai_utils.py            # AI content generation functions
├── pdf_utils.py           # PDF text extraction utilities
├── quiz_system.py         # Interactive quiz functionality
├── flashcard_system.py    # Flashcard study system
├── run_gui.py             # GUI launcher
├── requirements.txt       # Python dependencies
├── .env                   # API key configuration (create this)
└── README.md             # This file
```

## How It Works

1. **Upload PDF**: Select a PDF document containing study material
2. **Text Extraction**: System extracts text using PDF processing libraries
3. **AI Processing**: Claude API generates multiple study formats from the extracted text
4. **Study Sessions**: Use interactive tools to study the generated content
5. **Progress Tracking**: Monitor your learning progress across different topics

## Terminal vs GUI Features

### Available in Both
- PDF upload and processing
- Content generation (summaries, notes, questions)
- Topic management
- Content viewing

### Terminal-Only Features
- **Interactive Flashcards**: Full flashcard study sessions with progress tracking
- **Complete Quiz System**: MCQ, fill-in-blanks, and true/false quizzes with scoring
- **Advanced Study Sessions**: Detailed progress tracking and session management
- **Content Management**: Advanced file and topic organization

## Configuration

Create a `.env` file in the project root:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Get your API key from [Anthropic's website](https://console.anthropic.com/).

## Supported File Types

- PDF documents (.pdf)
- Text content extraction from various PDF formats

## Future Enhancements

- **Full GUI Quiz Implementation**: Complete interactive quiz system in the GUI
- **GUI Flashcard Study**: Interactive flashcard sessions with visual progress tracking
- **Spaced Repetition Algorithm**: Intelligent flashcard scheduling based on performance
- **Study Progress Analytics**: Detailed performance tracking and learning analytics
- **Export Functionality**: Export study materials to various formats (Anki, Word, etc.)
- **Collaborative Features**: Share and collaborate on study materials
- **Mobile App**: Native mobile application for on-the-go studying
- **Voice Integration**: Audio playback of study materials and voice-activated quizzes
- **Multiple AI Models**: Support for different AI providers and models
- **Advanced PDF Support**: Better handling of complex PDF layouts, images, and tables
- **Study Schedule Management**: Automated study session planning and reminders
- **Offline Mode**: Local processing without requiring internet connection

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your `.env` file contains a valid Anthropic API key
2. **PDF Processing Error**: Try installing pdfplumber for better PDF support: `pip install pdfplumber`
3. **GUI Not Starting**: Make sure tkinter is installed (usually comes with Python)
4. **Module Import Errors**: Install all dependencies: `pip install -r requirements.txt`


## License

Educational use project. Please respect API usage limits and terms of service.

## Acknowledgments

- Built with Anthropic's Claude API for intelligent content generation
- PDF processing powered by PyPDF2 and pdfplumber
- GUI built with Python's tkinter framework

---

**Note**: The terminal version provides full functionality including interactive quizzes and flashcards. The GUI version currently offers basic features with advanced functionality planned for future releases.

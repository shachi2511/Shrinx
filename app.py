from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import threading
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
app.config['UPLOAD_FOLDER'] = 'uploads'
OUTPUT_DIR = Path('output')

os.makedirs('uploads', exist_ok=True)
os.makedirs('output', exist_ok=True)

# ── AI + PDF utils (same as your existing files) ──────────────────────────────
import os as _os
from dotenv import load_dotenv
import anthropic

load_dotenv()
_client = anthropic.Anthropic(api_key=_os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-6"

def _call(system, user, max_tokens=1000):
    r = _client.messages.create(
        model=MODEL,
        system=system,
        messages=[{"role": "user", "content": user}],
        max_tokens=max_tokens
    )
    return r.content[0].text.strip()

def generate_summary(text):
    return _call("You are an expert study assistant. Create concise, well-structured summaries.",
                 f"Create a comprehensive summary with key points and main concepts:\n\n{text[:4000]}", 900)

def generate_notes(text):
    return _call("You are an expert study assistant. Create detailed, well-organized study notes.",
                 f"Create detailed study notes with clear headings, bullet points, and key concepts:\n\n{text[:4000]}", 1200)

def generate_flashcards(text):
    return _call("You are an expert study assistant creating flashcards.",
                 f"Create 10 flashcards. Format EXACTLY as:\nQ: [question]\nA: [answer]\n---\n\n{text[:4000]}", 1400)

def generate_mcq(text):
    return _call("You are an expert creating multiple choice questions with explanations.",
                 f"Create 5 MCQ questions. Format EXACTLY:\nQ1: [question]\nA) [opt]\nB) [opt]\nC) [opt]\nD) [opt]\nCorrect: [letter]\nExplanation: [explanation]\n\n{text[:4000]}", 1800)

def generate_fill_blanks(text):
    return _call("You are an expert creating fill-in-the-blank questions.",
                 f"Create 5 fill-in-the-blank questions. Format EXACTLY:\nQ: [sentence with ___]\nA: [answer]\nExplanation: [brief explanation]\n\n{text[:4000]}", 1200)

def generate_true_false(text):
    return _call("You are an expert creating true/false questions.",
                 f"Create 5 true/false questions. Format EXACTLY:\nQ: [statement]\nA: [True/False]\nExplanation: [explanation]\n\n{text[:4000]}", 1200)

def generate_qa(text):
    return _call("You are an expert creating Q&A study pairs.",
                 f"Create 5 detailed Q&A pairs. Format EXACTLY:\nQ: [question]\nA: [detailed answer]\n\n{text[:4000]}", 1800)

def extract_text_from_pdf(pdf_path):
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        return text.strip()
    except ImportError:
        pass
    try:
        import PyPDF2
        text = ""
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"PDF extraction failed: {e}")

# ── parsing helpers ───────────────────────────────────────────────────────────
def parse_flashcards(text):
    cards = []
    for block in text.split('---'):
        lines = block.strip().split('\n')
        q = a = ""
        for line in lines:
            if line.startswith('Q:'):
                q = line[2:].strip()
            elif line.startswith('A:'):
                a = line[2:].strip()
        if q and a:
            cards.append({'question': q, 'answer': a})
    return cards

def parse_mcq(text):
    questions = []
    for block in text.split('\n\n'):
        if not block.strip():
            continue
        lines = block.strip().split('\n')
        q = opts = correct = explanation = ""
        opts_list = []
        for line in lines:
            line = line.strip()
            if line.startswith(('Q1:','Q2:','Q3:','Q4:','Q5:','Q:')):
                q = line.split(':', 1)[1].strip() if ':' in line else line
            elif line.startswith(('A)','B)','C)','D)')):
                opts_list.append(line)
            elif line.startswith('Correct:'):
                correct = line.split(':', 1)[1].strip().upper()
            elif line.startswith('Explanation:'):
                explanation = line.split(':', 1)[1].strip()
        if q and len(opts_list) == 4 and correct:
            questions.append({'question': q, 'options': opts_list,
                              'correct': correct, 'explanation': explanation})
    return questions

def parse_tf(text):
    questions = []
    for block in text.split('\n\n'):
        lines = block.strip().split('\n')
        q = a = explanation = ""
        for line in lines:
            if line.startswith('Q:'):
                q = line[2:].strip()
            elif line.startswith('A:'):
                a = line[2:].strip()
            elif line.startswith('Explanation:'):
                explanation = line.split(':', 1)[1].strip()
        if q and a:
            questions.append({'question': q, 'answer': a, 'explanation': explanation})
    return questions

def parse_fill(text):
    questions = []
    for block in text.split('\n\n'):
        lines = block.strip().split('\n')
        q = a = explanation = ""
        for line in lines:
            if line.startswith('Q:'):
                q = line[2:].strip()
            elif line.startswith('A:'):
                a = line[2:].strip()
            elif line.startswith('Explanation:'):
                explanation = line.split(':', 1)[1].strip()
        if q and a:
            questions.append({'question': q, 'answer': a, 'explanation': explanation})
    return questions

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/topics')
def get_topics():
    if not OUTPUT_DIR.exists():
        return jsonify([])
    topics = []
    for d in OUTPUT_DIR.iterdir():
        if d.is_dir():
            files = [f.name for f in d.glob('*.txt')]
            topics.append({'name': d.name, 'display': d.name.replace('_', ' ').title(), 'files': files})
    return jsonify(topics)

@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    topic = request.form.get('topic', '').strip().replace(' ', '_')
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDF files allowed'}), 400
    if not topic:
        return jsonify({'error': 'Topic name required'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Process in background
    thread = threading.Thread(target=process_pdf_task, args=(filepath, topic))
    thread.daemon = True
    thread.start()

    return jsonify({'message': 'Processing started', 'topic': topic})

processing_status = {}

def process_pdf_task(filepath, topic):
    processing_status[topic] = {'status': 'running', 'steps': [], 'error': None}
    try:
        topic_dir = OUTPUT_DIR / topic
        topic_dir.mkdir(parents=True, exist_ok=True)

        def log(msg):
            processing_status[topic]['steps'].append(msg)

        log('Extracting text from PDF...')
        text = extract_text_from_pdf(filepath)
        (topic_dir / 'raw.txt').write_text(text, encoding='utf-8')
        log('Text extracted successfully')

        tasks = [
            ('summary', 'Generating summary...', generate_summary),
            ('notes', 'Creating study notes...', generate_notes),
            ('flashcards', 'Building flashcards...', generate_flashcards),
            ('mcq_questions', 'Creating MCQ quiz...', generate_mcq),
            ('fill_blanks', 'Creating fill-in-the-blank...', generate_fill_blanks),
            ('true_false', 'Creating true/false quiz...', generate_true_false),
            ('qa_questions', 'Generating Q&A pairs...', generate_qa),
        ]

        for fname, msg, fn in tasks:
            log(msg)
            content = fn(text)
            (topic_dir / f'{fname}.txt').write_text(content, encoding='utf-8')
            log(f'✓ {fname.replace("_", " ").title()} done')

        processing_status[topic]['status'] = 'complete'
        log('All done!')

    except Exception as e:
        processing_status[topic]['status'] = 'error'
        processing_status[topic]['error'] = str(e)

@app.route('/api/status/<topic>')
def get_status(topic):
    return jsonify(processing_status.get(topic, {'status': 'unknown'}))

@app.route('/api/content/<topic>/<content_type>')
def get_content(topic, content_type):
    file_map = {
        'summary': 'summary.txt',
        'notes': 'notes.txt',
        'flashcards': 'flashcards.txt',
        'mcq': 'mcq_questions.txt',
        'fill': 'fill_blanks.txt',
        'tf': 'true_false.txt',
        'qa': 'qa_questions.txt',
    }
    filename = file_map.get(content_type)
    if not filename:
        return jsonify({'error': 'Unknown content type'}), 404

    path = OUTPUT_DIR / topic / filename
    if not path.exists():
        return jsonify({'error': 'Content not found'}), 404

    raw = path.read_text(encoding='utf-8')

    # Return parsed versions for quiz types
    if content_type == 'flashcards':
        return jsonify({'raw': raw, 'parsed': parse_flashcards(raw)})
    elif content_type == 'mcq':
        return jsonify({'raw': raw, 'parsed': parse_mcq(raw)})
    elif content_type == 'tf':
        return jsonify({'raw': raw, 'parsed': parse_tf(raw)})
    elif content_type == 'fill':
        return jsonify({'raw': raw, 'parsed': parse_fill(raw)})
    else:
        return jsonify({'raw': raw})

@app.route('/api/delete/<topic>', methods=['DELETE'])
def delete_topic(topic):
    import shutil
    topic_dir = OUTPUT_DIR / topic
    if topic_dir.exists():
        shutil.rmtree(topic_dir)
        return jsonify({'message': 'Deleted'})
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
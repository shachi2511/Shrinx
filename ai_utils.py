import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=API_KEY)

def generate_summary(text):
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        system="You are a helpful assistant that creates concise, well-structured summaries.",
        messages=[
            {"role": "user", "content": f"Create a comprehensive but concise summary of the following text. Include key points, main concepts, and important details:\n\n{text}"}
        ],
        max_tokens=800
    )
    return response.content[0].text.strip()

def generate_notes(text):
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        system="You are a helpful assistant that creates detailed study notes.",
        messages=[
            {"role": "user", "content": f"Create detailed study notes from the following text. Organize with clear headings, bullet points, and key concepts:\n\n{text}"}
        ],
        max_tokens=1000
    )
    return response.content[0].text.strip()

def generate_flashcards(text):
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        system="You are a helpful assistant that creates flashcards for studying.",
        messages=[
            {"role": "user", "content": f"Create 10 flashcards from the following text. Format each as 'Q: [question]\\nA: [answer]\\n---\\n':\n\n{text}"}
        ],
        max_tokens=1200
    )
    return response.content[0].text.strip()

def generate_mcq_questions(text):
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        system="You are a helpful assistant that creates multiple choice questions with explanations.",
        messages=[
            {"role": "user", "content": f"Create 5 multiple choice questions based on this text. For each question, provide:\n- The question\n- Four options (A-D)\n- The correct answer\n- A brief explanation\n\nFormat: Q1: [question]\\nA) [option]\\nB) [option]\\nC) [option]\\nD) [option]\\nCorrect: [letter]\\nExplanation: [explanation]\\n\\n{text}"}
        ],
        max_tokens=1500
    )
    return response.content[0].text.strip()

def generate_fill_blanks(text):
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        system="You are a helpful assistant that creates fill-in-the-blank questions.",
        messages=[
            {"role": "user", "content": f"Create 5 fill-in-the-blank questions from this text. Format each as:\\nQ: [question with ___ for blanks]\\nA: [answer]\\nExplanation: [brief explanation]\\n\\n{text}"}
        ],
        max_tokens=1000
    )
    return response.content[0].text.strip()

def generate_true_false(text):
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        system="You are a helpful assistant that creates true/false questions.",
        messages=[
            {"role": "user", "content": f"Create 5 true/false questions from this text. Format each as:\\nQ: [statement]\\nA: [True/False]\\nExplanation: [explanation]\\n\\n{text}"}
        ],
        max_tokens=1000
    )
    return response.content[0].text.strip()

def generate_qa_questions(text):
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        system="You are a helpful assistant that creates question-answer pairs.",
        messages=[
            {"role": "user", "content": f"Create 5 detailed question-answer pairs from this text. Format each as:\\nQ: [question]\\nA: [detailed answer]\\n\\n{text}"}
        ],
        max_tokens=1500
    )
    return response.content[0].text.strip()
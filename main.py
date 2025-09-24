#!/usr/bin/env python3
"""
Shrinx Terminal Version - Minimal Working Version
"""

import os
from pathlib import Path

# Try to import AI modules, create dummies if not available
try:
    from dotenv import load_dotenv
    import anthropic
    load_dotenv()
    
    API_KEY = os.getenv("ANTHROPIC_API_KEY")
    if API_KEY:
        client = anthropic.Anthropic(api_key=API_KEY)
        AI_AVAILABLE = True
    else:
        AI_AVAILABLE = False
        print("⚠️  No API key found in .env file")
        
except ImportError:
    AI_AVAILABLE = False
    print("⚠️  AI modules not available (anthropic/dotenv not installed)")

# Try to import PDF modules
try:
    import PyPDF2
    PDF_AVAILABLE = True
    def extract_text_from_pdf(pdf_path):
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
except ImportError:
    PDF_AVAILABLE = False
    def extract_text_from_pdf(pdf_path):
        return "Sample text from PDF (PyPDF2 not installed for real extraction)"

# AI generation functions
def generate_summary(text):
    if not AI_AVAILABLE:
        return "Sample summary: This is a brief overview of the content. (AI not available)"
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            system="You are a helpful assistant that creates concise summaries.",
            messages=[
                {"role": "user", "content": f"Create a brief summary of this text:\n\n{text[:2000]}"}
            ],
            max_tokens=500
        )
        return response.content[0].text.strip()
    except Exception as e:
        return f"Error generating summary: {e}"

def generate_notes(text):
    if not AI_AVAILABLE:
        return "Sample notes:\n• Key point 1\n• Key point 2\n• Key point 3\n(AI not available)"
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            system="You are a helpful assistant that creates detailed study notes.",
            messages=[
                {"role": "user", "content": f"Create detailed study notes from this text:\n\n{text[:2000]}"}
            ],
            max_tokens=800
        )
        return response.content[0].text.strip()
    except Exception as e:
        return f"Error generating notes: {e}"

def generate_questions(text):
    if not AI_AVAILABLE:
        return "Sample Questions:\n\nQ1: What is the main topic?\nA) Option A\nB) Option B\nC) Option C\nD) Option D\nCorrect: A\n(AI not available)"
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            system="You are a helpful assistant that creates multiple choice questions.",
            messages=[
                {"role": "user", "content": f"Create 3 multiple choice questions from this text:\n\n{text[:2000]}"}
            ],
            max_tokens=600
        )
        return response.content[0].text.strip()
    except Exception as e:
        return f"Error generating questions: {e}"

# Main application
OUTPUT_DIR = Path("output")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("\n" + "="*60)
    print("🧠 SHRINX - AI Study Assistant")
    print("SHRINK THE STUDYING, EXPAND THE LEARNING!")
    print("="*60)

def list_topics():
    """List all available topics"""
    if not OUTPUT_DIR.exists():
        print("No topics found yet.")
        return []
    
    topics = [d.name for d in OUTPUT_DIR.iterdir() if d.is_dir()]
    if not topics:
        print("No topics found yet.")
        return []
    
    print("\n📚 Available Topics:")
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic.replace('_', ' ')}")
    
    return topics

def view_topic(topic_name):
    """View a specific topic"""
    topic_dir = OUTPUT_DIR / topic_name
    if not topic_dir.exists():
        print("❌ Topic not found.")
        return
    
    while True:
        clear_screen()
        print_header()
        print(f"\n📖 Topic: {topic_name.replace('_', ' ')}")
        print("\n1. 📄 View Summary")
        print("2. 📝 View Notes") 
        print("3. ❓ View Questions")
        print("4. 📁 View All Files")
        print("5. ⬅️  Back to Main Menu")
        
        choice = input("\nChoose option (1-5): ").strip()
        
        if choice == "1":
            show_file_content(topic_dir / "summary.txt", "Summary")
        elif choice == "2":
            show_file_content(topic_dir / "notes.txt", "Notes")
        elif choice == "3":
            show_file_content(topic_dir / "questions.txt", "Questions")
        elif choice == "4":
            show_all_files(topic_dir)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")
            input("Press Enter to continue...")

def show_file_content(file_path, title):
    """Show content of a file"""
    clear_screen()
    print_header()
    print(f"\n📖 {title}")
    print("="*60)
    
    if file_path.exists():
        content = file_path.read_text(encoding='utf-8')
        print(content)
    else:
        print(f"No {title.lower()} found for this topic.")
    
    input("\nPress Enter to continue...")

def show_all_files(topic_dir):
    """Show all files in topic directory"""
    clear_screen()
    print_header()
    print(f"\n📁 All Files in {topic_dir.name}")
    print("="*60)
    
    files = list(topic_dir.glob("*.txt"))
    if not files:
        print("No files found.")
    else:
        for file in files:
            print(f"\n📄 {file.name}:")
            print("-" * 40)
            content = file.read_text(encoding='utf-8')
            # Show first 200 characters
            print(content[:200] + ("..." if len(content) > 200 else ""))
    
    input("\nPress Enter to continue...")

def add_new_pdf():
    """Add and process a new PDF"""
    clear_screen()
    print_header()
    print("\n📄 Add New PDF")
    print("="*60)
    
    # Get PDF path
    pdf_path = input("Enter path to PDF file: ").strip()
    if not os.path.isfile(pdf_path):
        print("❌ File not found.")
        input("Press Enter to continue...")
        return
    
    # Get topic name
    topic = input("Enter topic name (use underscores for spaces): ").strip()
    if not topic:
        print("❌ Topic name cannot be empty.")
        input("Press Enter to continue...")
        return
    
    # Create topic directory
    topic_dir = OUTPUT_DIR / topic
    topic_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🔄 Processing PDF...")
    
    try:
        # Extract text
        print("1. Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_path)
        
        # Save raw text
        raw_text_path = topic_dir / "raw.txt"
        raw_text_path.write_text(text, encoding="utf-8")
        print(f"✅ Text extracted ({len(text)} characters)")
        
        # Generate summary
        print("2. Generating summary...")
        summary = generate_summary(text)
        (topic_dir / "summary.txt").write_text(summary, encoding="utf-8")
        print("✅ Summary generated")
        
        # Generate notes
        print("3. Generating notes...")
        notes = generate_notes(text)
        (topic_dir / "notes.txt").write_text(notes, encoding="utf-8")
        print("✅ Notes generated")
        
        # Generate questions
        print("4. Generating questions...")
        questions = generate_questions(text)
        (topic_dir / "questions.txt").write_text(questions, encoding="utf-8")
        print("✅ Questions generated")
        
        print(f"\n🎉 Successfully processed '{topic}'!")
        print(f"📁 Files saved in: {topic_dir}")
        
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
    
    input("\nPress Enter to continue...")

def main():
    """Main application loop"""
    while True:
        clear_screen()
        print_header()
        
        # Show status
        print(f"\n📊 Status:")
        print(f"   AI Features: {'✅ Available' if AI_AVAILABLE else '❌ Disabled'}")
        print(f"   PDF Processing: {'✅ Available' if PDF_AVAILABLE else '⚠️  Limited'}")
        
        print(f"\n📋 Main Menu:")
        print("1. 📁 List Topics")
        print("2. 📖 View Topic")
        print("3. 📄 Add New PDF")
        print("4. ⚙️  Setup Info")
        print("5. 🚪 Exit")
        
        choice = input("\nChoose option (1-5): ").strip()
        
        if choice == "1":
            clear_screen()
            print_header()
            list_topics()
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            clear_screen()
            print_header()
            topics = list_topics()
            if topics:
                try:
                    topic_num = int(input(f"\nEnter topic number (1-{len(topics)}): "))
                    if 1 <= topic_num <= len(topics):
                        view_topic(topics[topic_num - 1])
                    else:
                        print("Invalid topic number.")
                        input("Press Enter to continue...")
                except ValueError:
                    print("Please enter a valid number.")
                    input("Press Enter to continue...")
            else:
                input("Press Enter to continue...")
                
        elif choice == "3":
            add_new_pdf()
            
        elif choice == "4":
            show_setup_info()
            
        elif choice == "5":
            print("\n👋 Thanks for using Shrinx! Happy studying!")
            break
            
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def show_setup_info():
    """Show setup information"""
    clear_screen()
    print_header()
    print("\n⚙️  Setup Information")
    print("="*60)
    
    print("📋 Required Dependencies:")
    
    modules = [
        ("anthropic", "AI text generation", AI_AVAILABLE),
        ("python-dotenv", "Environment variables", True),
        ("PyPDF2", "PDF text extraction", PDF_AVAILABLE),
    ]
    
    for module, description, available in modules:
        status = "✅ Available" if available else "❌ Missing"
        print(f"   {module:15} - {description:25} [{status}]")
    
    print(f"\n📁 Files:")
    files = [
        ("main.py", "This terminal application", os.path.exists("main.py")),
        (".env", "API key configuration", os.path.exists(".env")),
        ("output/", "Generated content directory", OUTPUT_DIR.exists()),
    ]
    
    for filename, description, exists in files:
        status = "✅ Found" if exists else "❌ Missing"
        print(f"   {filename:15} - {description:25} [{status}]")
    
    print(f"\n🔧 Installation Commands:")
    print("   pip install anthropic python-dotenv PyPDF2")
    print("   echo 'ANTHROPIC_API_KEY=your_key_here' > .env")
    
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
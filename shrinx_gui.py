import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from pathlib import Path
import threading

# Import your existing modules - make sure these files exist
try:
    from pdf_utils import extract_text_from_pdf
    from ai_utils import (
        generate_summary, generate_notes, generate_flashcards,
        generate_mcq_questions, generate_fill_blanks, 
        generate_true_false, generate_qa_questions
    )
    from quiz_system import QuizSystem
    from flashcard_system import FlashcardSystem
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")
    print("Make sure you have all the required files in the same directory.")
    
    # Create dummy functions for testing
    def extract_text_from_pdf(path):
        return "Sample text from PDF for testing purposes."
    
    def generate_summary(text):
        return "This is a sample summary of the text."
    
    def generate_notes(text):
        return "Sample detailed notes from the text."
    
    def generate_flashcards(text):
        return "Q: Sample question?\nA: Sample answer\n---\nQ: Another question?\nA: Another answer"
    
    def generate_mcq_questions(text):
        return "Q1: What is this?\nA) Option A\nB) Option B\nC) Option C\nD) Option D\nCorrect: A\nExplanation: This is the explanation."
    
    def generate_fill_blanks(text):
        return "Q: This is a ___ question.\nA: sample\nExplanation: Fill in the blank."
    
    def generate_true_false(text):
        return "Q: This is true.\nA: True\nExplanation: This statement is correct."
    
    def generate_qa_questions(text):
        return "Q: What is this about?\nA: This is about sample content."
    
    class QuizSystem:
        def parse_mcq_questions(self, text):
            return [{'question': 'Sample question?', 'options': ['A) Option A', 'B) Option B'], 'correct': 'A', 'explanation': 'Sample explanation'}]
        
        def parse_fill_blanks(self, text):
            return [{'question': 'Sample ___?', 'answer': 'blank', 'explanation': 'Sample explanation'}]
        
        def parse_true_false(self, text):
            return [{'question': 'This is true?', 'answer': 'True', 'explanation': 'Sample explanation'}]
    
    class FlashcardSystem:
        def parse_flashcards(self, text):
            return [{'question': 'Sample question?', 'answer': 'Sample answer'}]

class ShrinxGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🧠 ShrinX - AI Study Assistant")
        self.root.geometry("900x600")
        self.root.configure(bg='#f8fdff')
        
        # Colors matching your design
        self.colors = {
            'primary': '#2D9B9B',      # Main teal
            'primary_dark': '#1e6b6b', # Darker teal
            'secondary': '#FF5A5A',    # Red/orange
            'accent': '#4ECDC4',       # Light teal
            'purple': '#8B5FBF',       # Purple
            'yellow': '#F39C12',       # Orange-yellow
            'orange': '#FF9F43',       # Orange
            'bg': '#f8fdff',           # Light blue background
            'white': '#ffffff',
            'dark': '#2C3E50',
            'light_gray': '#ECF0F1',
            'border': '#BDC3C7'
        }
        
        self.output_dir = Path("output")
        self.quiz_system = QuizSystem()
        self.flashcard_system = FlashcardSystem()
        self.current_topic = None
        
        self.setup_fonts()
        self.create_main_screen()
    
    def setup_fonts(self):
        """Setup fonts for the application"""
        self.fonts = {
            'title': ('Arial', 24, 'bold'),
            'subtitle': ('Arial', 14),
            'heading': ('Arial', 18, 'bold'),
            'body': ('Arial', 12),
            'button': ('Arial', 11, 'bold'),
            'small': ('Arial', 10)
        }
    
    def create_main_screen(self):
        """Create the main welcome screen"""
        self.clear_screen()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Header with logo and title
        header_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 30))
        
        # Brain emoji as logo
        logo_label = tk.Label(header_frame, text="🧠", font=('Arial', 60), 
                             bg=self.colors['bg'])
        logo_label.pack()
        
        title_label = tk.Label(header_frame, text="ShrinX", 
                              font=self.fonts['title'],
                              fg=self.colors['primary'],
                              bg=self.colors['bg'])
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, 
                                 text="SHRINK THE STUDYING, EXPAND THE LEARNING!", 
                                 font=self.fonts['subtitle'],
                                 fg=self.colors['dark'],
                                 bg=self.colors['bg'])
        subtitle_label.pack()
        
        # Main buttons
        buttons_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        buttons_frame.pack(expand=True)
        
        # Upload PDF button
        upload_btn = tk.Button(buttons_frame, 
                              text="📄 Upload New PDF", 
                              font=self.fonts['heading'],
                              bg=self.colors['secondary'], 
                              fg='white',
                              padx=40, pady=20,
                              border=0,
                              cursor='hand2',
                              command=self.upload_pdf_screen)
        upload_btn.pack(pady=15)
        
        # Browse Topics button
        browse_btn = tk.Button(buttons_frame, 
                              text="📁 Browse Topics", 
                              font=self.fonts['heading'],
                              bg=self.colors['primary'], 
                              fg='white',
                              padx=40, pady=20,
                              border=0,
                              cursor='hand2',
                              command=self.browse_topics_screen)
        browse_btn.pack(pady=15)
        
        # Exit button
        exit_btn = tk.Button(buttons_frame, 
                            text="🚪 Exit", 
                            font=self.fonts['body'],
                            bg=self.colors['dark'], 
                            fg='white',
                            padx=30, pady=10,
                            border=0,
                            cursor='hand2',
                            command=self.root.quit)
        exit_btn.pack(pady=15)
    
    def upload_pdf_screen(self):
        """Screen for uploading and processing PDF"""
        self.clear_screen()
        
        # Header
        self.create_header("📄 Upload PDF", self.create_main_screen)
        
        # Main content
        content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # File selection
        file_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        file_frame.pack(fill='x', pady=20)
        
        tk.Label(file_frame, text="Select PDF File:", 
                font=self.fonts['body'], 
                bg=self.colors['bg'], 
                fg=self.colors['dark']).pack(anchor='w')
        
        file_path_frame = tk.Frame(file_frame, bg=self.colors['bg'])
        file_path_frame.pack(fill='x', pady=10)
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(file_path_frame, 
                             textvariable=self.file_path_var,
                             font=self.fonts['body'],
                             width=50)
        file_entry.pack(side='left', padx=(0, 10))
        
        browse_btn = tk.Button(file_path_frame, 
                              text="📁 Browse", 
                              font=self.fonts['button'],
                              bg=self.colors['accent'], 
                              fg='white',
                              border=0,
                              cursor='hand2',
                              command=self.browse_file)
        browse_btn.pack(side='left')
        
        # Topic name
        topic_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        topic_frame.pack(fill='x', pady=20)
        
        tk.Label(topic_frame, text="Topic Name:", 
                font=self.fonts['body'], 
                bg=self.colors['bg'], 
                fg=self.colors['dark']).pack(anchor='w')
        
        self.topic_var = tk.StringVar()
        topic_entry = tk.Entry(topic_frame, 
                              textvariable=self.topic_var,
                              font=self.fonts['body'],
                              width=30)
        topic_entry.pack(anchor='w', pady=10)
        
        # Process button
        process_btn = tk.Button(content_frame, 
                               text="🔄 Process PDF", 
                               font=self.fonts['button'],
                               bg=self.colors['primary'], 
                               fg='white',
                               padx=30, pady=15,
                               border=0,
                               cursor='hand2',
                               command=self.process_pdf)
        process_btn.pack(pady=30)
        
        # Progress area
        self.progress_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        self.progress_frame.pack(fill='x', pady=20)
        
        self.progress_text = scrolledtext.ScrolledText(self.progress_frame, 
                                                      height=8, 
                                                      width=80,
                                                      font=('Courier', 10),
                                                      bg='#2C3E50', 
                                                      fg='#ECF0F1',
                                                      insertbackground='white')
        self.progress_text.pack()
        self.progress_text.insert('1.0', "Ready to process PDF...\n")
    
    def browse_topics_screen(self):
        """Screen for browsing existing topics"""
        self.clear_screen()
        
        # Header
        self.create_header("📁 Browse Topics", self.create_main_screen)
        
        # Main content
        content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Get topics
        topics = self.get_topics()
        
        if not topics:
            no_topics_label = tk.Label(content_frame, 
                                      text="No topics found yet!\nUpload a PDF to get started.", 
                                      font=self.fonts['heading'], 
                                      bg=self.colors['bg'], 
                                      fg=self.colors['dark'],
                                      justify='center')
            no_topics_label.pack(expand=True)
            return
        
        # Topics grid
        topics_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        topics_frame.pack(fill='both', expand=True)
        
        # Create topic cards
        row = 0
        col = 0
        for topic in topics:
            self.create_topic_card(topics_frame, topic, row, col)
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1
    
    def create_topic_card(self, parent, topic, row, col):
        """Create a topic card button"""
        card_frame = tk.Frame(parent, bg='white', relief='raised', bd=2)
        card_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Folder icon
        folder_label = tk.Label(card_frame, text="📁", font=('Arial', 40), bg='white')
        folder_label.pack(pady=(20, 10))
        
        # Topic name
        topic_name = topic.replace('_', ' ').title()
        name_label = tk.Label(card_frame, text=topic_name, 
                             font=self.fonts['body'], 
                             bg='white', 
                             fg=self.colors['dark'])
        name_label.pack(pady=(0, 20))
        
        # Make clickable
        def on_click(event):
            self.topic_detail_screen(topic)
        
        card_frame.bind("<Button-1>", on_click)
        folder_label.bind("<Button-1>", on_click)
        name_label.bind("<Button-1>", on_click)
        
        # Hover effects
        def on_enter(e):
            card_frame.configure(bg=self.colors['accent'], cursor='hand2')
            folder_label.configure(bg=self.colors['accent'])
            name_label.configure(bg=self.colors['accent'])
        
        def on_leave(e):
            card_frame.configure(bg='white')
            folder_label.configure(bg='white')
            name_label.configure(bg='white')
        
        for widget in [card_frame, folder_label, name_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
    
    def topic_detail_screen(self, topic):
        """Screen showing topic details and options"""
        self.current_topic = topic
        self.clear_screen()
        
        # Header
        topic_display = topic.replace('_', ' ').title()
        self.create_header(f"📚 {topic_display}", self.browse_topics_screen)
        
        # Main content
        content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Options grid
        options_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        options_frame.pack(expand=True)
        
        # Define options with icons and colors
        options = [
            ("📖", "Summary", self.colors['yellow'], self.show_summary),
            ("📝", "Notes", self.colors['secondary'], self.show_notes),
            ("🃏", "Flashcards", self.colors['purple'], self.study_flashcards),
            ("🎯", "Quiz", self.colors['primary'], self.quiz_menu),
            ("❓", "Q&A", self.colors['accent'], self.show_qa)
        ]
        
        # Create option buttons in grid
        for i, (icon, text, color, command) in enumerate(options):
            row = i // 3
            col = i % 3
            
            option_btn = tk.Button(options_frame, 
                                  text=f"{icon}\n{text}", 
                                  font=self.fonts['body'],
                                  bg=color, 
                                  fg='white',
                                  width=12, height=4,
                                  border=0,
                                  cursor='hand2',
                                  command=command)
            option_btn.grid(row=row, column=col, padx=20, pady=20)
    
    def quiz_menu(self):
        """Quiz type selection menu"""
        self.clear_screen()
        
        # Header
        topic_display = self.current_topic.replace('_', ' ').title()
        self.create_header(f"🎯 Quiz - {topic_display}", 
                          lambda: self.topic_detail_screen(self.current_topic))
        
        # Main content
        content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Quiz options
        quiz_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        quiz_frame.pack(expand=True)
        
        quiz_types = [
            ("🎯", "Multiple Choice", self.colors['primary'], self.start_mcq_quiz),
            ("📝", "Fill in Blanks", self.colors['secondary'], self.start_fill_blanks_quiz),
            ("✓❌", "True/False", self.colors['purple'], self.start_true_false_quiz)
        ]
        
        for i, (icon, text, color, command) in enumerate(quiz_types):
            quiz_btn = tk.Button(quiz_frame, 
                                text=f"{icon}\n{text}", 
                                font=self.fonts['body'],
                                bg=color, 
                                fg='white',
                                width=15, height=4,
                                border=0,
                                cursor='hand2',
                                command=command)
            quiz_btn.pack(pady=20)
    
    def create_header(self, title, back_command):
        """Create a standard header with title and back button"""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Back button
        back_btn = tk.Button(header_frame, 
                            text="← Back", 
                            font=self.fonts['button'],
                            bg=self.colors['accent'], 
                            fg='white',
                            border=0,
                            cursor='hand2',
                            command=back_command)
        back_btn.pack(side='left', padx=20, pady=20)
        
        # Title
        title_label = tk.Label(header_frame, text=title, 
                              font=self.fonts['heading'], 
                              bg=self.colors['primary'], 
                              fg='white')
        title_label.pack(side='left', padx=20, pady=20)
    
    def clear_screen(self):
        """Clear all widgets from the screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def get_topics(self):
        """Get list of available topics"""
        if not self.output_dir.exists():
            return []
        return [d.name for d in self.output_dir.iterdir() if d.is_dir()]
    
    def browse_file(self):
        """Open file browser for PDF selection"""
        filename = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def process_pdf(self):
        """Process the selected PDF file"""
        file_path = self.file_path_var.get().strip()
        topic = self.topic_var.get().strip()
        
        if not file_path or not os.path.isfile(file_path):
            messagebox.showerror("Error", "Please select a valid PDF file.")
            return
        
        if not topic:
            messagebox.showerror("Error", "Please enter a topic name.")
            return
        
        # Clear progress text
        self.progress_text.delete('1.0', tk.END)
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self._process_pdf_thread, 
                                 args=(file_path, topic))
        thread.daemon = True
        thread.start()
    
    def _process_pdf_thread(self, file_path, topic):
        """Process PDF in a separate thread"""
        try:
            topic_dir = self.output_dir / topic
            topic_dir.mkdir(parents=True, exist_ok=True)
            
            self.update_progress("🔄 Extracting text from PDF...")
            text = extract_text_from_pdf(file_path)
            
            # Save raw text
            raw_text_path = topic_dir / "raw.txt"
            raw_text_path.write_text(text, encoding="utf-8")
            self.update_progress("✅ Text extracted and saved")
            
            # Generate all content
            content_types = [
                ("summary", "📖 Generating summary...", generate_summary),
                ("notes", "📝 Creating detailed notes...", generate_notes),
                ("flashcards", "🃏 Generating flashcards...", generate_flashcards),
                ("mcq_questions", "🎯 Creating MCQ questions...", generate_mcq_questions),
                ("fill_blanks", "📝 Generating fill-in-the-blank questions...", generate_fill_blanks),
                ("true_false", "✓❌ Creating true/false questions...", generate_true_false),
                ("qa_questions", "❓ Generating Q&A pairs...", generate_qa_questions)
            ]
            
            for filename, message, func in content_types:
                self.update_progress(message)
                content = func(text)
                (topic_dir / f"{filename}.txt").write_text(content, encoding="utf-8")
                self.update_progress(f"✅ {filename.replace('_', ' ').title()} completed")
            
            self.update_progress(f"\n🎉 Successfully processed '{topic}'!")
            self.update_progress(f"📁 All content saved in: {topic_dir}")
            
            # Show success message
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", 
                f"PDF processed successfully!\nTopic '{topic}' is ready for study."
            ))
            
        except Exception as e:
            self.update_progress(f"❌ Error: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to process PDF: {str(e)}"))
    
    def update_progress(self, message):
        """Update progress text (thread-safe)"""
        def _update():
            self.progress_text.insert(tk.END, message + "\n")
            self.progress_text.see(tk.END)
            self.root.update_idletasks()
        
        self.root.after(0, _update)
    
    def show_summary(self):
        """Show topic summary"""
        self.show_content("summary", "📖 Summary", "summary.txt")
    
    def show_notes(self):
        """Show topic notes"""
        self.show_content("notes", "📝 Notes", "notes.txt")
    
    def show_qa(self):
        """Show Q&A content"""
        self.show_content("qa", "❓ Q&A", "qa_questions.txt")
    
    def show_content(self, content_type, title, filename):
        """Generic function to show content"""
        self.clear_screen()
        
        # Header
        topic_display = self.current_topic.replace('_', ' ').title()
        self.create_header(f"{title} - {topic_display}", 
                          lambda: self.topic_detail_screen(self.current_topic))
        
        # Content
        content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Text area
        text_area = scrolledtext.ScrolledText(content_frame, 
                                             wrap=tk.WORD,
                                             font=('Georgia', 12),
                                             bg='white',
                                             fg=self.colors['dark'],
                                             padx=20, pady=20)
        text_area.pack(fill='both', expand=True)
        
        # Load and display content
        content_file = self.output_dir / self.current_topic / filename
        if content_file.exists():
            content = content_file.read_text(encoding='utf-8')
            text_area.insert('1.0', content)
        else:
            text_area.insert('1.0', f"No {content_type} found for this topic.")
        
        text_area.config(state='disabled')  # Make read-only
    
    def study_flashcards(self):
        """Start flashcard study session"""
        flashcards_file = self.output_dir / self.current_topic / "flashcards.txt"
        if not flashcards_file.exists():
            messagebox.showwarning("Warning", "No flashcards found for this topic.")
            return
        
        # For now, show in a simple dialog - can be enhanced later
        messagebox.showinfo("Flashcards", "Flashcard study feature will be implemented!\nFor now, use the terminal version.")
    
    def start_mcq_quiz(self):
        """Start MCQ quiz"""
        messagebox.showinfo("Quiz", "Quiz feature will be implemented!\nFor now, use the terminal version.")
    
    def start_fill_blanks_quiz(self):
        """Start fill-in-the-blanks quiz"""
        messagebox.showinfo("Quiz", "Quiz feature will be implemented!\nFor now, use the terminal version.")
    
    def start_true_false_quiz(self):
        """Start true/false quiz"""
        messagebox.showinfo("Quiz", "Quiz feature will be implemented!\nFor now, use the terminal version.")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main function to run the GUI"""
    try:
        app = ShrinxGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        print("Make sure you have tkinter installed and all required modules are available.")

if __name__ == "__main__":
    main()
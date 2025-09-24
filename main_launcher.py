#!/usr/bin/env python3
"""
Simple Shrinx Launcher - This should work!
"""

import sys
import os

def test_imports():
    """Test if we can import everything we need"""
    print("🔍 Testing imports...")
    
    # Test basic Python modules
    try:
        import tkinter as tk
        print("✅ tkinter - OK")
    except ImportError:
        print("❌ tkinter - MISSING")
        print("   Install: sudo apt-get install python3-tk (Ubuntu/Debian)")
        return False
    
    try:
        import threading
        print("✅ threading - OK")
    except ImportError:
        print("❌ threading - MISSING")
        return False
    
    # Test optional modules
    has_anthropic = False
    try:
        import anthropic
        print("✅ anthropic - OK")
        has_anthropic = True
    except ImportError:
        print("⚠️  anthropic - MISSING (AI features disabled)")
        print("   Install: pip install anthropic")
    
    has_dotenv = False
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv - OK")
        has_dotenv = True
    except ImportError:
        print("⚠️  python-dotenv - MISSING")
        print("   Install: pip install python-dotenv")
    
    has_pdf = False
    try:
        import PyPDF2
        print("✅ PyPDF2 - OK")
        has_pdf = True
    except ImportError:
        try:
            import pdfplumber
            print("✅ pdfplumber - OK")
            has_pdf = True
        except ImportError:
            print("⚠️  PDF libraries - MISSING")
            print("   Install: pip install PyPDF2")
    
    return True  # Continue even if some modules are missing

def create_simple_gui():
    """Create a simple GUI that definitely works"""
    import tkinter as tk
    from tkinter import messagebox, filedialog
    
    class SimpleShrinx:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("🧠 ShrinX - AI Study Assistant")
            self.root.geometry("600x400")
            self.root.configure(bg='#f0f8ff')
            
            # Colors
            self.colors = {
                'primary': '#2D9B9B',
                'secondary': '#FF5A5A',
                'bg': '#f0f8ff',
                'white': '#ffffff'
            }
            
            self.create_main_screen()
        
        def create_main_screen(self):
            """Create the main screen"""
            # Clear screen
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Main frame
            main_frame = tk.Frame(self.root, bg=self.colors['bg'])
            main_frame.pack(fill='both', expand=True, padx=40, pady=40)
            
            # Header
            header_frame = tk.Frame(main_frame, bg=self.colors['bg'])
            header_frame.pack(pady=(0, 30))
            
            # Logo and title
            logo_label = tk.Label(header_frame, text="🧠", font=('Arial', 48), bg=self.colors['bg'])
            logo_label.pack()
            
            title_label = tk.Label(header_frame, text="ShrinX", 
                                  font=('Arial', 24, 'bold'),
                                  fg=self.colors['primary'],
                                  bg=self.colors['bg'])
            title_label.pack(pady=10)
            
            subtitle_label = tk.Label(header_frame, 
                                     text="SHRINK THE STUDYING, EXPAND THE LEARNING!", 
                                     font=('Arial', 12),
                                     fg='#2C3E50',
                                     bg=self.colors['bg'])
            subtitle_label.pack()
            
            # Buttons
            buttons_frame = tk.Frame(main_frame, bg=self.colors['bg'])
            buttons_frame.pack(expand=True)
            
            # Upload button
            upload_btn = tk.Button(buttons_frame, 
                                  text="📄 Upload New PDF", 
                                  font=('Arial', 14, 'bold'),
                                  bg=self.colors['secondary'], 
                                  fg='white',
                                  padx=30, pady=15,
                                  border=0,
                                  cursor='hand2',
                                  command=self.upload_pdf)
            upload_btn.pack(pady=10)
            
            # Browse button
            browse_btn = tk.Button(buttons_frame, 
                                  text="📁 Browse Topics", 
                                  font=('Arial', 14, 'bold'),
                                  bg=self.colors['primary'], 
                                  fg='white',
                                  padx=30, pady=15,
                                  border=0,
                                  cursor='hand2',
                                  command=self.browse_topics)
            browse_btn.pack(pady=10)
            
            # Terminal button
            terminal_btn = tk.Button(buttons_frame, 
                                    text="💻 Use Terminal Version", 
                                    font=('Arial', 12),
                                    bg='#34495e', 
                                    fg='white',
                                    padx=30, pady=10,
                                    border=0,
                                    cursor='hand2',
                                    command=self.run_terminal)
            terminal_btn.pack(pady=10)
            
            # Exit button
            exit_btn = tk.Button(buttons_frame, 
                                text="🚪 Exit", 
                                font=('Arial', 12),
                                bg='#7f8c8d', 
                                fg='white',
                                padx=30, pady=10,
                                border=0,
                                cursor='hand2',
                                command=self.root.quit)
            exit_btn.pack(pady=10)
        
        def upload_pdf(self):
            """Handle PDF upload"""
            file_path = filedialog.askopenfilename(
                title="Select PDF File",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            
            if file_path:
                messagebox.showinfo("Success", f"Selected: {os.path.basename(file_path)}\n\nFull AI features coming soon!\nFor now, this demonstrates the GUI works.")
                # Here you would call your PDF processing function
                # self.process_pdf(file_path)
        
        def browse_topics(self):
            """Browse existing topics"""
            # Check if output directory exists
            output_dir = "output"
            if not os.path.exists(output_dir):
                messagebox.showinfo("No Topics", "No topics found yet!\nUpload a PDF to get started.")
                return
            
            # List existing topics
            topics = [d for d in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, d))]
            
            if not topics:
                messagebox.showinfo("No Topics", "No topics found yet!\nUpload a PDF to get started.")
            else:
                topic_list = "\n".join(f"• {topic.replace('_', ' ')}" for topic in topics)
                messagebox.showinfo("Available Topics", f"Found topics:\n\n{topic_list}\n\nFull topic browser coming soon!")
        
        def run_terminal(self):
            """Run terminal version"""
            messagebox.showinfo("Terminal Version", 
                               "To run the terminal version:\n\n" +
                               "1. Open your terminal/command prompt\n" +
                               "2. Navigate to this folder\n" +
                               "3. Run: python main.py\n\n" +
                               "Make sure you have all dependencies installed!")
        
        def run(self):
            """Start the GUI"""
            self.root.mainloop()
    
    return SimpleShrinx()

def main():
    """Main function"""
    print("🧠 ShrinX - AI Study Assistant")
    print("=" * 40)
    print(f"Python version: {sys.version}")
    print(f"Running from: {os.getcwd()}")
    print()
    
    # Test imports
    if not test_imports():
        print("\n❌ Critical imports failed. Cannot continue.")
        input("Press Enter to exit...")
        return
    
    print("\n✅ Basic requirements met!")
    print("\n🚀 Starting GUI...")
    
    try:
        # Try to import and run the full GUI
        try:
            from shrinx_gui import ShrinxGUI
            print("✅ Found full GUI - starting...")
            app = ShrinxGUI()
            app.run()
        except ImportError:
            print("⚠️  Full GUI not found, using simple version...")
            app = create_simple_gui()
            app.run()
            
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        print("\nTrying to run terminal version instead...")
        
        try:
            # Try terminal version
            if os.path.exists('main.py'):
                print("Found main.py - you can run: python main.py")
            else:
                print("No main.py found either.")
        except Exception as e2:
            print(f"Terminal version also failed: {e2}")
        
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
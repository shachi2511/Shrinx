"""
PDF utilities for extracting text from PDF files
"""

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False
    print("Warning: PyPDF2 not installed. Install with: pip install PyPDF2")

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using available libraries
    """
    if HAS_PDFPLUMBER:
        return extract_with_pdfplumber(pdf_path)
    elif HAS_PYPDF2:
        return extract_with_pypdf2(pdf_path)
    else:
        raise ImportError("No PDF library available. Install PyPDF2 or pdfplumber: pip install PyPDF2 pdfplumber")

def extract_with_pdfplumber(pdf_path):
    """Extract text using pdfplumber (recommended)"""
    import pdfplumber
    
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    return text.strip()

def extract_with_pypdf2(pdf_path):
    """Extract text using PyPDF2"""
    import PyPDF2
    
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
    
    return text.strip()

# Test function
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        try:
            text = extract_text_from_pdf(pdf_path)
            print(f"Extracted {len(text)} characters from {pdf_path}")
            print("First 500 characters:")
            print(text[:500])
        except Exception as e:
            print(f"Error extracting text: {e}")
    else:
        print("Usage: python pdf_utils.py <path_to_pdf>")
        print("Available libraries:")
        print(f"  PyPDF2: {'✓' if HAS_PYPDF2 else '✗'}")
        print(f"  pdfplumber: {'✓' if HAS_PDFPLUMBER else '✗'}")